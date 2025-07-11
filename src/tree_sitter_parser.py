import os
import re
import tree_sitter_c as ts_c
import tree_sitter_cpp as ts_cpp
from tree_sitter import Language, Parser
import argparse
import pprint as pp
from string_utils import extract_only_function_name


# Load the languages
# C_LANGUAGE = Language(ts_c.language(), 'c')
# CPP_LANGUAGE = Language(ts_cpp.language(), 'cpp')

C_LANGUAGE = Language(ts_c.language())
CPP_LANGUAGE = Language(ts_cpp.language())


def update_parent_with_func_def(classes_list, structs_list, func_name, function_body):
    # logic to check if the function is a member of a class or struct
    # print('IN UPDATE CONTAINERS FUNCTION:')
    container_name = func_name.split("::")[0]
    for class_obj in classes_list:
        if container_name == class_obj["name"]:
            # extend the body of the parent object with the function
            class_obj["body"] += "\n\n" + function_body + "\n"

    for struct_obj in structs_list:
        if container_name == struct_obj["name"]:
            # extend the body of the parent object with the function
            struct_obj["body"] += "\n\n" + function_body + "\n"


def get_body_with_template_declaration(node, source_code):
    # check if parent node is a template declaration
    offset = 0
    body = ""
    if node.parent.type == "template_declaration":
        # get the template declaration
        body = get_node_text(source_code, node.parent)
        offset = -1
    else:
        body = get_node_text(source_code, node)

    return body, offset


def read_source_code(filename):
    with open(filename, "r") as file:
        return file.read()


def get_pointers_ret_type_string(input_string):
    match = re.search("[_a-zA-Z]", input_string)
    if match:
        ret_type_part = input_string[: match.start()]
        # Normalize spaces around asterisks (*) and ampersands (&)
        # Ensure one space before * or &, and remove space after * or &
        ret_type_part = re.sub(r"\s*\*\s*", " *", ret_type_part)
        ret_type_part = re.sub(r"\s*&\s*", " &", ret_type_part)
        return ret_type_part.strip()
    else:
        return input_string.strip()


def get_only_func_name(input_string):
    match = re.search("[_a-zA-Z]", input_string)
    if match:
        return input_string[match.start() :].strip()
    else:
        return input_string.strip()


def get_node_text(source_code, node):
    lines = source_code.splitlines()
    start_line, start_char = node.start_point
    print('IN GET NODE TEXT FUNCTION:')
    print(node.start_point)
    end_line, end_char = node.end_point
    print(start_line, end_line)
    print(node.end_point)
    if start_line == end_line:
        return lines[start_line][start_char:end_char]
    else:
        return "\n".join(
            [lines[start_line][start_char:]]
            + lines[start_line + 1 : end_line]
            + [lines[end_line][:end_char]]
        )


def find_parameters_from_pointer_reference_declarator(node):
    # print(node)
    # Base case: If the node is a function_declarator, return its parameters
    if node.type == "function_declarator":
        return node.child_by_field_name("parameters")

    # Recursive case: If the node is a pointer_declarator, recurse on its declarator
    elif node.type == "pointer_declarator":
        return find_parameters_from_pointer_reference_declarator(
            node.child_by_field_name("declarator")
        )

    elif node.type == "reference_declarator":
        #print(node.children)
        return find_parameters_from_pointer_reference_declarator(node.children[1])

    # If the node is neither, handle accordingly (e.g., return None or raise an error)
    else:
        print("Node type not recognized:", node.type)
        return None  # Or raise an error


def get_parameter_info_from_parameter_node(parameter_node, source_code):

    parameter_counter = 0
    parameter_type_list = []
    parameter_name_list = []

    for param_children in parameter_node.children:
        #print("----PARAMETER NODE CHILDREN:-----", param_children)

        if param_children.type == "parameter_declaration":
            parameter_counter += 1
            param_child_type = ""
            for children in param_children.children:
                

                # print("children: ", get_node_text(source_code, children).strip())
                # print("type: ", children.type)
                # print()

                if children.type == "identifier":
                    parameter_name_list.append(get_node_text(source_code, children).strip())
                    
                elif children.type in ("abstract_pointer_declarator", "abstract_reference_declarator"):
                    child_type_temp = get_node_text(source_code, children)
                    parameter_name_list.append(None)

                elif children.type not in (
                    "identifier",
                    "pointer_declarator",
                    "reference_declarator",
                ):
                    param_child_type += get_node_text(source_code, children) + " "

                elif children.type in ("pointer_declarator", "reference_declarator"):
                    child_type_temp = get_node_text(source_code, children)
                    param_child_type += get_pointers_ret_type_string(child_type_temp)
                    parameter_name_list.append(get_only_func_name(child_type_temp).strip())

            parameter_type_list.append(param_child_type.strip())
  
        elif param_children.type == "...":
            parameter_counter += 1
            parameter_type_list.append("...")
            parameter_name_list.append(None)

    return parameter_counter, parameter_type_list, parameter_name_list



def extract_functions_globals_headers(source_code, tree):
    functions = []
    globals = []
    headers = []
    classes = []
    structs = []
    root_node = tree.root_node

    def visit(node):
        print('NODE TYPE:', node.type)
        if node.type == "function_definition":
            # print('------Function Definition Node: ------')
            # print(node)
            # print()
            # print(node.child_by_field_name('type').text)

            func_node_children = node.children
            # print('FUNCTION NODE CHILDREN:', func_node_children)
            func_return_type = ""
            function_body, offset = get_body_with_template_declaration(
                node, source_code
            )

            has_func_declarator = False
            declarator_index = -1
            parameter_node = None

            for index, child_node in enumerate(func_node_children):

                if child_node.type == "function_declarator":

                    parameter_node = child_node.child_by_field_name("parameters")

                    parameter_counter, parameter_type_list, parameter_name_list = (
                        get_parameter_info_from_parameter_node(
                            parameter_node, source_code
                        )
                    )

                    has_func_declarator = True
                    declarator_index = index
                    break

                elif (
                    child_node.type == "pointer_declarator"
                    or child_node.type == "reference_declarator"
                ):

                    #print("-----pointer_declarator node: -----")
                    parameter_node = find_parameters_from_pointer_reference_declarator(
                        child_node
                    )
                    #print("-----parameter node: -----")
                    #print(parameter_node)

                    parameter_counter, parameter_type_list, parameter_name_list = (
                        get_parameter_info_from_parameter_node(
                            parameter_node, source_code
                        )
                    )

                    declarator_index = index
                    break

            i = 0
            while i < declarator_index:
                func_return_type += (
                    get_node_text(source_code, func_node_children[i]) + " "
                )
                i += 1

            if not has_func_declarator:
                func_return_type += get_pointers_ret_type_string(
                    get_node_text(source_code, func_node_children[i])
                )

            #print("parameter type: ", parameter_type_list)
            # if len(func_node_children) > 2:
            #     print('FUNCTION NODE CHILDREN:', get_node_text(source_code, func_node_children[0]), get_node_text(source_code, func_node_children[1]), get_node_text(source_code, func_node_children[2]))
            # # logic to get node type
            # if len(func_node_children) > 0:
            #     if func_node_children[1].type == 'function_declarator':
            #         func_return_type = get_node_text(source_code, func_node_children[0])
            #     else:
            #         if func_node_children[0].type == 'primitive_type' and func_node_children[1].type in ('pointer_declarator','reference_declarator') :
            #             func_return_type = get_node_text(source_code, func_node_children[0]) + \
            #                 get_pointers_ret_type_string(get_node_text(source_code, func_node_children[1]))
            #         else:
            #             i = 0
            #             while func_node_children[i].type != 'function_declarator':
            #                 func_return_type += get_node_text(source_code, func_node_children[i]) + ' '
            #                 i += 1

            func_declarator_obj = node.child_by_field_name("declarator")
            func_name = func_declarator_obj.text.decode("utf-8")
            # print(func_declarator_obj.type)

            if func_declarator_obj.type in (
                "pointer_declarator",
                "reference_declarator",
            ):
                # remove * symbol from the name
                print('HERE!', func_name)
                func_name = get_only_func_name(func_name)

            start_line = node.start_point[0] + 1 + offset
            end_line = node.end_point[0] + 1
            print('FUNCTION NAME:', func_name)
            functions.append(
                {
                    "name_with_params": func_name,
                    "name_only": extract_only_function_name(func_name),
                    "return_type": func_return_type,
                    "start_line": start_line,
                    "end_line": end_line,
                    "body": function_body,
                    "parameters_count": parameter_counter,
                    "parameter_type_list": parameter_type_list,
                    "parameter_name_list": parameter_name_list,
                }
            )

            # print('ADDED FUNCTION: ', func_name, '\n\n')

            # check if the function is a member of a class or struct and update the parent object
            update_parent_with_func_def(classes, structs, func_name, function_body)

            # if parent_obj:
            #     print('PARENT OBJECT FOUND: ', parent_obj['body'])
            return

        elif node.type == "declaration" or node.type == "declaration_list":
            globals.append(get_node_text(source_code, node)) 
            return
        elif node.type == "preproc_include":
            headers.append(get_node_text(source_code, node))
        elif node.type == "preproc_def" or node.type == "preproc_function_def":
            globals.append(get_node_text(source_code, node))
        elif node.type == "constant":
            globals.append(get_node_text(source_code, node))
        elif node.type == "class_specifier":  # class

            class_node_body, offset = get_body_with_template_declaration(
                node, source_code
            )

            if class_node_body[-1] != ";":
                class_node_body += ";"

            # storing class name, body, start line and end line in a dictionary
            class_name = node.child_by_field_name("name").text
            start_line = node.start_point[0] + 1 + offset
            end_line = node.end_point[0] + 1

            classes_obj = {
                "name": class_name.decode("utf-8"),
                "body": class_node_body,
                "start_line": start_line,
                "end_line": end_line,
            }

            classes.append(classes_obj)
            globals.append(classes_obj)
            down_type = 'class_specifier'
            return  

        elif node.type == "struct_specifier":  # struct
            # print("Inside struct node")
            # print('STRUCT NODE:', node)
            structure_body = get_node_text(source_code, node)
            print('STRUCTURE BODY:', structure_body)
            if structure_body[-1] != ";":
                structure_body += ";"

            # storing struct name, body, start line and end line in a dictionary
            struct_name = node.child_by_field_name("name").text
            start_line = node.start_point[0] + 1
            end_line = node.end_point[0] + 1

            structure_obj = {
                "name": struct_name.decode("utf-8"),
                "body": structure_body,
                "start_line": start_line,
                "end_line": end_line,
            }

            structs.append(structure_obj)
            globals.append(structure_obj)
            return

        elif node.type == "type_definition":  # typedef
            globals.append(get_node_text(source_code, node))
            return
        elif node.type == "enum_specifier":
            enum_string = get_node_text(source_code, node)

            if enum_string[-1] != ";":
                enum_string += ";"
            globals.append(enum_string)
            return
        elif node.type == "union_specifier":
            globals.append(get_node_text(source_code, node))
            return
        elif node.type == "preproc_call":  # pragma
            globals.append(get_node_text(source_code, node))
        elif (
            node.type == "preproc_if"
            or node.type == "preproc_ifdef"
            or node.type == "preproc_ifndef"
        ):
            children = node.children
            # print('CHILDREN:', children)
            
            has_func_def_child = False

            for child in children:
                if child.type == 'function_definition':
                    has_func_def_child = True
                    break
            
            if not has_func_def_child:
                # if, ifdef, ifndef, else, elif, endif cases
                globals.append(get_node_text(source_code, node))
        elif node.type == "comment":
            globals.append(get_node_text(source_code, node))
        elif node.type == "parameter_pack_expansion":  # ...
            globals.append(get_node_text(source_code, node))
        elif node.type == "namespace_definition":
            globals.append(get_node_text(source_code, node))
            parent_type = 'namespace_definition'
            return
        elif node.type == 'using_declaration':
            globals.append(get_node_text(source_code, node))
            return

        # print('GLOBALS: ', globals)
        #print(node.children)
        
        for child in node.children:
            # print('Before visiting child node:', child.type)
            # print('GLOBAL OBJECTS:', globals)
            visit(child)
            # print('=>=>=>=>=>=>=>=> After visiting child node: =>=>=>=>=>=>=>=> ', child.type)
            # print('GLOBAL OBJECTS:', globals)

    visit(root_node)
    return (headers, globals, functions, classes, structs)


def print_information(information_tuple):
    headers, globals, functions, classes, structs = information_tuple

    # Print the results
    print("Header Files:")
    for header in headers:
        print(header)

    print("\nGlobal Definitions:")
    for global_obj in globals:
        if type(global_obj) == dict:
            print(global_obj["name"])
            print(global_obj["body"])

        else:
            print(global_obj)
        print()

    print("\nFunction Definitions:")

    for func in functions:
        print(f"Function: {func['name_with_params']}")
        print(f"Function Name: {func['name_only']}")
        print(f"Return Type: {func['return_type']}")
        print(f"Parameters Count: {func['parameters_count']}")
        print(f"Parameter Type List: {func['parameter_type_list']}")
        print(f"Parameter Name List: {func['parameter_name_list']}")
        print(f"Start Line: {func['start_line']}")
        print(f"End Line: {func['end_line']}")
        print(func["body"])
        print("\n" + "-" * 80 + "\n")

    print("\nClass Definitions:")
    for class_ in classes:
        print(f"Class: {class_['name']}")
        print(f"Start Line: {class_['start_line']}")
        print(f"End Line: {class_['end_line']}")
        print(class_["body"])
        print("\n" + "-" * 80 + "\n")

    print("\nStruct Definitions:")
    for struct in structs:
        print(f"Struct: {struct['name']}")
        print(f"Start Line: {struct['start_line']}")
        print(f"End Line: {struct['end_line']}")
        print("THE BODY OF THE STRUCTURE:-----------------> ")
        print(struct["body"])
        print("\n" + "-" * 80 + "\n")


# def initialize_parser(source_file):
#     parser = Parser()
#     file_extension = os.path.splitext(source_file)[1]
#     if file_extension in ['.c']:
#         parser.set_language(C_LANGUAGE)
#     elif file_extension in ['.cpp', '.cxx', '.cc', '.h', '.hpp']:
#         parser.set_language(CPP_LANGUAGE)
#     else:
#         raise ValueError(f"Unsupported file extension: {file_extension}")

#     return parser


def initialize_parser(source_file):
    file_extension = os.path.splitext(source_file)[1]
    if file_extension in [".c"]:
        parser = Parser(C_LANGUAGE)
    elif file_extension in [".cpp", ".cxx", ".cc", ".h", ".hpp"]:
        parser = Parser(CPP_LANGUAGE)
    else:
        print(f"Unsupported file extension: {file_extension}")

    return parser


def main():

    arg_parser = argparse.ArgumentParser(description="Parse C/C++ source code")
    arg_parser.add_argument("source_file", type=str, help="The source file to parse")
    args = arg_parser.parse_args()

    print(f"Parsing {args.source_file}")

    # Set the language based on the file extension
    source_file = args.source_file
    parser = initialize_parser(source_file)

    # Read the source code
    source_code = read_source_code(source_file)
    tree = parser.parse(bytes(source_code, "utf8"))

    # Extract functions, globals, and headers
    parsed_info = extract_functions_globals_headers(source_code, tree)
    print_information(parsed_info)


if __name__ == "__main__":
    main()
