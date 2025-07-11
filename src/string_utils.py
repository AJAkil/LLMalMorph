import re
import json


def escape_string_for_json(source_code):
    # Escape backslashes that are not already part of an escape sequence
    escaped_code = re.sub(r'(?<!\\)\\(?!\\)', r'\\\\', source_code)
    # Escape double quotes that are not already escaped
    escaped_code = re.sub(r'(?<!\\)(?:\\\\)*"', r'\\"', escaped_code)
    # Normalize newlines to be represented by \n only
    escaped_code = escaped_code.replace(
        "\\\\n", "\\n")  # replace any \\n with \n
    return escaped_code


def extract_only_function_name(str_to_search):
    print("the string to search is:", str_to_search)
    """
    Extracts the name of the function from a given string.

    Parameters:
    str_to_search (str): The string to search for function names.

    Returns:
    str: The name of the function.

    Example:
    >>> extract_only_function_name("void MyClass::myFunction(int)")
    'myFunction'
    """
    pattern = r'(?:(\w+)::)?(\w+|operator\S+)(?:<[^>]+>)?\('
    match = re.findall(pattern, str_to_search)
    print('the match is: ', match)
    return match[0][1]


def replace_function_name_custom(
    code_str, target_func_name, replacer_func_name, target_func_parameter_count
):
    def find_all_indices_of_target_function_name(code_str, target_func_name):
        return [
            i for i in range(len(code_str)) if code_str.startswith(target_func_name, i)
        ]

    def check_parenthesis(code_str, func_length, index):
        return code_str[index + func_length] == "("

    unchecked_indices = find_all_indices_of_target_function_name(
        code_str, target_func_name
    )
    func_length = len(target_func_name)
    selected_indices = list(
        filter(
            lambda index: check_parenthesis(code_str, func_length, index),
            unchecked_indices,
        )
    )

    updated_code_str = code_str
    offset_index = 0

    for name_start_index in selected_indices:
        bracket_counter = 0
        parameter_counter = 0
        name_end_index = name_start_index + func_length
        has_seen_non_space = False

        for i, char in enumerate(code_str[name_start_index + func_length:], start=name_start_index + func_length):
            if char == "(":
                bracket_counter += 1
                if bracket_counter == 1 and not has_seen_non_space:
                    # This handles a case with no parameters
                    parameter_counter = 0
            elif char == ")":
                bracket_counter -= 1
                if bracket_counter == 0:
                    # Correctly handle the case with a single parameter or nested calls
                    if has_seen_non_space:
                        parameter_counter = max(parameter_counter, 1)
                    break
            elif bracket_counter == 1:
                if char == ",":
                    parameter_counter += 1
                elif not char.isspace() and not has_seen_non_space:
                    # Found a non-space character inside the parentheses
                    has_seen_non_space = True
                    parameter_counter = 1

        # print('Parameter count:', parameter_counter)

        if parameter_counter == target_func_parameter_count:
            print(
                f'Replacing function name {target_func_name} with {replacer_func_name}')
            updated_code_str = (
                updated_code_str[: name_start_index + offset_index]
                + replacer_func_name
                + updated_code_str[name_end_index + offset_index:]
            )
            offset_index += len(replacer_func_name) - len(target_func_name)

    return updated_code_str


def replace_function_name(function_str, original_name, new_name, num_params):
    """
    Replaces the function name in the given function string with a new name,
    only if the function call matches the original name and the number of parameters.

    :param function_str: The string containing the function code.
    :param original_name: The original name of the function to replace.
    :param new_name: The new name to replace the original function name with.
    :param num_params: The number of parameters the original function takes.
    :return: The modified function string with the function name replaced.
    """
    # Regular expression to match function calls. It captures the function name and the parameter list.
    func_call_pattern = re.compile(
        r'(\b{}\b)\(([^)]*)\)'.format(original_name))

    def replacement(match):
        # Split the parameters by commas and filter out empty strings (to handle cases with no parameters correctly).
        params = [param for param in match.group(
            2).split(',') if param.strip()]

        # Replace the function name only if the number of parameters matches.
        if len(params) == num_params:
            return '{}({})'.format(new_name, match.group(2))
        else:
            # Return the original match if the number of parameters does not match.
            return match.group(0)

    # Replace the function calls in the function string.
    modified_function_str = func_call_pattern.sub(replacement, function_str)

    return modified_function_str


def count_parameters(function_signature):
    # Extract the parameter list from the function signature
    param_list_match = re.search(r'\((.*?)\)', function_signature)
    if not param_list_match:
        return 0  # No parameters found

    param_list = param_list_match.group(1)

    # Handle the case of no parameters
    if not param_list.strip():
        return 0

    # Split the parameters by comma and count them
    parameters = param_list.split(',')
    return len(parameters)


def fix_single_backslashes(source_code):
    if not isinstance(source_code, str):
        #print(type(source_code))
        raise ValueError("source code must be a string")

    # This pattern aims to match single-quoted strings and escape sequences accurately
    # It also matches single backslashes not followed by another backslash outside these contexts
    # pattern = r"(?<!\\)'(?:\\.|[^'\\])*'|(\\+)"
    pattern = r"(?<!\\)'(?:\\.|[^'\\])*'|" + r'(?<!\\)"(?:\\.|[^"\\])*"|(\\+)'
    def replace(match):
        # If the match is a single backslash not part of a single-quoted string or escape sequence, replace it

        if match.group(1):
            matched_text = match.group(1)
            # If the sequence length is odd, add one backslash to make it even
            if len(matched_text) % 2 == 1:
                #print(matched_text)
                return matched_text + '\\'
            else:
                return matched_text
        # Otherwise, return the match as is (including single-quoted strings and escape sequences)
        return match.group(0)

    return re.sub(pattern, replace, source_code)


'''
def escape_string_for_json(source_code):
    # Function to escape individual JSON string values
    def escape_match(value):
        print('Inside escape match function')
        print(value)
        print('End of escape match function')
        # Escape backslashes that are not already part of an escape sequence
        escaped_value = re.sub(r'(?<!\\)\\(?!\\)', r'\\\\', value)
        # Escape double quotes that are not already escaped
        escaped_value = re.sub(r'(?<!\\)(?:\\\\)*"', r'\\"', escaped_value)
        # Normalize newlines to be represented by \n only
        escaped_value = escaped_value.replace("\r\n", "\\n").replace("\n", "\\n")
        return escaped_value

    # Match only JSON string values (naive approach, assuming no nested objects or arrays as values)
    pattern = r':\s*"(.*?)"(?=[,}])'
    escaped_code = re.sub(pattern, lambda m: ': "' + escape_match(m.group(1)) + '"', source_code)
    return escaped_code
'''


def fix_json_like_string(json_like_string):
    json_ready_code = escape_string_for_json(json_like_string)
    print(json_ready_code)

    json_ready_code = re.sub(r'\\"', '"', json_ready_code, count=3)

    # Find all occurrences of \" in the string
    escapes = list(re.finditer(r'\\"', json_ready_code))
    # print('escapes list: ', escapes)

    # List to hold positions of \" that should be unescaped
    positions_to_unescape = []

    for match in escapes:
        start_pos = match.start()
        end_pos = match.end()

        # print(start_pos, end_pos)

        # Check context before and after the match
        # This is a simplistic check; you might need more complex logic depending on your JSON structure
        before_context = json_ready_code[max(0, start_pos - 5):start_pos]
        after_context = json_ready_code[end_pos:min(
            len(json_ready_code), end_pos + 5)]

        # # Example condition: if \" is followed by a colon or comma, or preceded by a colon, it's likely part of a structure
        # if ':' and '\\"' in after_context or ':' and '\\"' in before_context:
        #     print('inside if')
        #     print(before_context, '<\\">', after_context)
        #     print('start pos: ', start_pos)
        #     print('end pos: ', end_pos)
        #     positions_to_unescape.append((start_pos, end_pos))

    # print('positions to unescape: ', positions_to_unescape)
    # print('json ready code: ', json_ready_code)

    if '\\"mapping\\":' and '\\"comments\\":' in json_ready_code:
        # add the last 5 positions to unescape list
        print('handling')
        temp_list = escapes[-9:]

        for i in temp_list:
            positions_to_unescape.append((i.start(), i.end()))

    elif '\\"mapping\\":' in json_ready_code and '\\"comments\\":' not in json_ready_code or \
            '\\"mapping\\":' not in json_ready_code and '\\"comments\\":' in json_ready_code:

        temp_list = escapes[-5:]

        for i in temp_list:
            positions_to_unescape.append((i.start(), i.end()))

    # Sort the positions to unescape
    positions_to_unescape.sort()
    seen = set()
    final_positiona_to_unescape = []
    for start_pos, end_pos in positions_to_unescape:

        position_tuple = (start_pos, end_pos)

        if position_tuple not in seen:
            seen.add(position_tuple)
            final_positiona_to_unescape.append(position_tuple)

    print(final_positiona_to_unescape)
    new_string_parts = []
    last_pos = 0

    for start_pos, end_pos in final_positiona_to_unescape:
        # Add everything up to the escape sequence
        # print(json_ready_code[last_pos:start_pos])
        # print('IIII')
        new_string_parts.append(json_ready_code[last_pos:start_pos])
        # Add the unescaped quote
        new_string_parts.append('"')
        # print('new string parts: ', new_string_parts)
        # print('\n\n\n')
        # Update the last position
        last_pos = end_pos

    # Add the remaining part of the string
    new_string_parts.append(json_ready_code[last_pos:])

    last_string = ''.join(new_string_parts)

    # pattern = r'(?<!\\)(\\\")(?=\s*[:\]})|\G(?<=:\s*)(\\\")'
    # # Replace the matched patterns with unescaped quotes
    # unescaped_json = re.sub(pattern, '"', json_ready_code)
    # print(unescaped_json)

    print(last_string)

    return last_string


def fix_json_errors(json_str):

    print(json_str)
    while True:
        try:
            # Attempt to parse the JSON string
            parsed_json = json.loads(json_str)
            # If parsing is successful, break out of the loop
            break
        except json.JSONDecodeError as e:
            # Extract the error message
            error_message = str(e)
            print(error_message)
            error_pos = e.pos
            print(error_pos)
            print(json_str[error_pos])
            print(json_str[error_pos:])

            if "Invalid control character" in error_message:
                # For simplicity, assuming the control character is a newline
                # You might need a more sophisticated approach for other control characters
                json_str = json_str[:error_pos] + \
                    "\\n" + json_str[error_pos+1:]
                print(f'inside invalid correction: {json_str}')
            elif "Expecting ',' delimiter" in error_message or "Expecting property name enclosed in double quotes" in error_message:
                # Insert a backslash before the problematic character (assuming it's a quote)
                json_str = json_str[:error_pos-1] + \
                    '\\' + json_str[error_pos-1:]
                print(json_str)
                print('Inside delimeter correction')
            else:
                # If the error is not one of the handled types, re-raise the exception
                raise e
        except Exception as e:
            # Handle other exceptions
            raise e
    return parsed_json


def extract_modified_code(json_like_string):
    # Use regex to extract the content of "modified code"
    pattern = r'"modified code":\s*"(.*?)(?<!\\)"'
    match = re.search(pattern, json_like_string, re.DOTALL)

    if match:
        modified_code = match.group(1)
        # # Decode escape sequences
        # modified_code = modified_code.encode().decode('unicode_escape')
        return modified_code
    else:
        return None


if __name__ == "__main__":
    ill_formed_json = '''{ 
    "a" : " "a", "b\\" "
    }'''

    fix_json_errors(ill_formed_json)

# Example usage
# if __name__ == "__main__":
#     # source_code = r'''include<iostream>\n const char *registry_keys[] = {\"SOFTWARE\\Microsoft\Windows\CurrentVersion\Run"}; snprintf(Folder, MAX_PATH, \"%s\\*.*\", Data2.cFileName);
#     # '''
#     # source_code = '''{"modified code": "#include <windows.h>\\n#include <fstream>\\n#include <time.h>\\n\\nvoid process_files() {\\n    // Sleep for 5 seconds between each operation.\\n    Sleep(5000);\\n\\n const char *registry_keys[] = {"SOFTWARE\\Microsoft\Windows\CurrentVersion\Run"}; snprintf(Folder, MAX_PATH, \"%s\\*.*\", Data2.cFileName);}",
#     # "comments": "This function processes files in the following manner: it searches for and processes all .exe files in the current directory, copies a specified file to all logical drives, and deletes all files in all subdirectories. The original functionality is maintained while improving error handling and coding style.",
#     # "mapping": "func(inaat a) : func(int a)|read_files(int a)"
#     # }'''

#     # source_code = '''```json
#     # {
#     # "modified code": "#include <fstream>\n#include <cstring>\n\nint func(char *FPath, char *BUFF) {\n    std::ifstream file(FPath, std::ios::binary | std::ios::ate);\n    int size = file.tellg();\n    file.seekg(0, std::ios::beg);\n\n    std::string buffer(size, '\\0');\n    file.read(&buffer[0], size);\n\n    if (buffer.find(\"*B*\") == std::string::npos) {\n        std::ofstream outfile(FPath, std::ios::binary);\n        outfile.write(BUFF, 464834);\n        outfile.write(inf, strlen(inf));\n        outfile.write(&buffer[0], size);\n    }\n\n    return 0;\n}",
#     # "comments": "The function is optimized by using std::string for buffer handling and C++ standard library functions for file operations. The string search operation is more efficient than looping through the characters manually."
#     # }
#     # ```'''
#     # print("PARSING LLM RESPOPNSE")
#     # result_json_object = parse_json_from_llm_response(source_code, 'cpp')


#     for match in escapes:
#         start_pos = match.start()
#         end_pos = match.end()

#         #print(start_pos, end_pos)

#         # Check context before and after the match
#         # This is a simplistic check; you might need more complex logic depending on your JSON structure
#         before_context = json_ready_code[max(0, start_pos - 5):start_pos]
#         after_context = json_ready_code[end_pos:min(len(json_ready_code), end_pos + 5)]

#         print(before_context, '--', after_context)

#         # Example condition: if \" is followed by a colon or comma, or preceded by a colon, it's likely part of a structure
#         if ':' and '\\"' in after_context or ':' and '\\"' in before_context:
#             # print('inside if')
#             # print(before_context, '<\\">', after_context)
#             positions_to_unescape.append((start_pos, end_pos))

#     print('positions to unescape: ', positions_to_unescape)
#     print('json ready code: ', json_ready_code)

#     if '\\"mapping\\":' and '\\"comments\\":' in json_ready_code:
#         # add the last 5 positions to unescape list
#         print('handling')
#         temp_list = escapes[-9:]

#         for i in temp_list:
#             positions_to_unescape.append((i.start(), i.end()))


#     elif '\\"mapping\\":' in json_ready_code and '\\"comments\\":' not in json_ready_code or \
#         '\\"mapping\\":' not in json_ready_code and '\\"comments\\":' in json_ready_code:

#         temp_list = escapes[-5:]

#         for i in temp_list:
#             positions_to_unescape.append((i.start(), i.end()))

#     # Sort the positions to unescape
#     positions_to_unescape.sort()
#     seen = set()
#     final_positiona_to_unescape = []
#     for start_pos, end_pos in positions_to_unescape:

#         position_tuple = (start_pos, end_pos)

#         if position_tuple not in seen:
#             seen.add(position_tuple)
#             final_positiona_to_unescape.append(position_tuple)

#     # add the last position to unescape
#     # positions_to_unescape.append((escapes[-1].start(), escapes[-1].end()))

#     # convert the list to a set to remove duplicates

#     # Unescape selected positions
#     # This requires creating a new string, as strings are immutable in Python
#     print(final_positiona_to_unescape)
#     new_string_parts = []
#     last_pos = 0

#     for start_pos, end_pos in final_positiona_to_unescape:
#         # Add everything up to the escape sequence
#         # print(json_ready_code[last_pos:start_pos])
#         # print('IIII')
#         new_string_parts.append(json_ready_code[last_pos:start_pos])
#         # Add the unescaped quote
#         new_string_parts.append('"')
#         # print('new string parts: ', new_string_parts)
#         # print('\n\n\n')
#         # Update the last position
#         last_pos = end_pos

#     # Add the remaining part of the string
#     new_string_parts.append(json_ready_code[last_pos:])

#     last_string  =''.join(new_string_parts)


#     # pattern = r'(?<!\\)(\\\")(?=\s*[:\]})|\G(?<=:\s*)(\\\")'
#     # # Replace the matched patterns with unescaped quotes
#     # unescaped_json = re.sub(pattern, '"', json_ready_code)
#     # print(unescaped_json)


#     print(last_string)

#    # Attempt to load the JSON
#     try:
#         json_ready_code = json.loads(last_string)
#         print(json_ready_code['modified code'])
#     except json.decoder.JSONDecodeError as e:
#         print("Failed to decode JSON:", e)
