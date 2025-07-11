from string_utils import (
    extract_only_function_name,
    count_parameters,
    replace_function_name,
    replace_function_name_custom,
    fix_single_backslashes,
)
import itertools
import os
import re

from randomization import generate_random_func_sequences
random_seed = 0


def create_output_directory(parent_dir, sub_dir_name):

    joined_output_dir = os.path.join(parent_dir, sub_dir_name)

    if not os.path.exists(joined_output_dir):
        os.makedirs(joined_output_dir)

    return joined_output_dir


def prepend_headers_globals(headers, globals):
    # add headers
    result = ""

    print('GLOBAL')
    print(globals)

    for header in headers:
        result += header + "\n"

    # add globals
    for global_ in globals:
        if type(global_) == dict:
            result += global_["body"] + "\n"
        else:
            result += global_ + "\n"

    return result


def normalize_signature(signature):
    # Remove comments
    signature = re.sub(r"//.*", "", signature)
    # Normalize spacing around '*', '&', and commas
    signature = re.sub(r"\s*\*\s*", " * ", signature)
    signature = re.sub(r"\s*&\s*", " & ", signature)
    signature = re.sub(r"\s*,\s*", ", ", signature)
    # Remove parameter names, keeping only types (simple approach)
    signature = re.sub(
        r"\b(\w+)\s+\w+(\s*[\[\]]\s*)*(,|$)", r"\1\2\3", signature)
    # Normalize const usage
    signature = re.sub(r"\bconst\b\s*", "const ", signature)
    # Handle default parameters by removing them
    signature = re.sub(r"=\s*[^,)]+", "", signature)
    # Collapse multiple spaces to a single space
    signature = re.sub(r"\s+", " ", signature)
    return signature.strip()


def compare_signatures(sig1, sig2):
    normalized_sig1 = normalize_signature(sig1)
    normalized_sig2 = normalize_signature(sig2)
    # print(normalized_sig1)
    # print(normalized_sig2)
    return normalized_sig1 == normalized_sig2


# # Example usage
# signature1 = "int func(char* FPath, const char *BUFF = nullptr)"
# signature2 = "int func(char *FPath, const char* BUFF)"

# if compare_signatures(signature1, signature2):
#     print("The function signatures match.")
# else:
#     print("The function signatures do not match.")


def stitcher(trial_to_function_variant_obj_list_mapping, info_tuple, is_failed_llm_generation_list_trial, func_gen_scheme):

    for trial_no, (trial_key, trial_to_function_variant_obj_list) in enumerate(trial_to_function_variant_obj_list_mapping.items()):
        # Assuming is_failed_llm_generation_list_trial is a list with a boolean for each trial
        is_failed_llm_generation = is_failed_llm_generation_list_trial[trial_no]

        process_trial_to_variant_function_obj_list_with_scheme(trial_to_function_variant_obj_list,
                                                               info_tuple + (trial_key,), is_failed_llm_generation, func_gen_scheme)


def process_trial_to_variant_function_obj_list(trial_to_function_variant_obj_list, info_tuple, is_failed_llm_generation_list):

    (
        main_source_parsed_info,
        variant_source_code_sub_dir,
        source_file_name,
        num_functions,
        batch_num,
        num_functions_merge_back,
        trial_no,
    ) = info_tuple

    if num_functions_merge_back == 0:
        print("No functions to merge back. Exiting the Stitcher.\n")
        return

    total_num_target_functions = len(trial_to_function_variant_obj_list)
    index_list = list(range(total_num_target_functions))
    num_functions_merge_back = min(num_functions_merge_back, total_num_target_functions)

    # create a folder based on the number of functions to merge back if it does not exist
    variant_source_code_num_merge_back_sub_dir = create_output_directory(variant_source_code_sub_dir, str(num_functions_merge_back))

    # first create the required possible combinations of the variant functions
    # # Convert the resulting iterator to a list
    function_variant_combinations = list(itertools.combinations(index_list, num_functions_merge_back))

    # Print the list of combinations to the console
    print(f"Function Variant Combination to merge back: {function_variant_combinations}\n\n")

    # form the object tuples for the selected combinations
    for function_variant_combination in function_variant_combinations:

        # create a list of objects according to the indices in the combination
        variant_obj_combination_list = [
            trial_to_function_variant_obj_list[index] for index in function_variant_combination
        ]

        failed_llm_response_status_list = [
            is_failed_llm_generation_list[index] for index in function_variant_combination]

        # DEBUG [1,2] or [2,3]
        # [1,2,3] = [f,f,t]
        print(variant_obj_combination_list)  # [f,g]
        print(failed_llm_response_status_list)
        # [f,g] -> stitch_back_to_source_code(f,g)

        stitch_back_to_source_code(
            main_source_parsed_info,
            variant_obj_combination_list,
            variant_source_code_num_merge_back_sub_dir,
            source_file_name,
            num_functions,
            trial_no,
            function_variant_combination,
            num_functions_merge_back,
            failed_llm_response_status_list
        )


def process_trial_to_variant_function_obj_list_with_scheme(trial_to_function_variant_obj_list, info_tuple,
                                                           is_failed_llm_generation_list, func_gen_scheme):

    (
        main_source_parsed_info,
        variant_source_code_sub_dir,
        source_file_name,
        num_functions,
        batch_num,
        num_functions_merge_back,
        trial_no,
    ) = info_tuple

    if num_functions_merge_back == 0:
        print("No functions to merge back. Exiting the Stitcher.\n")
        return

    total_num_target_functions = len(trial_to_function_variant_obj_list)
    num_functions_merge_back = min(
        num_functions_merge_back, total_num_target_functions)

    if func_gen_scheme == "sequential":

        print("\n ------ Using Sequential function variant combination ------ \n")
        function_variant_combination = list(range(num_functions_merge_back))
        print(f"Function Variant Combination to merge back: {function_variant_combination}\n\n")
    elif func_gen_scheme == "randomized":
        print("\n ------ Using Randomized function variant combination ------ \n")
        function_variant_combination = generate_random_func_sequences(
            total_num_target_functions, source_file_name, random_seed)

    # Print the list of combinations to the console
    # print(f"Function Variant Combination to merge back: {function_variant_combination}\n\n")

    # create a list of objects according to the indices in the combination
    variant_obj_combination_list = [
        trial_to_function_variant_obj_list[index] for index in function_variant_combination
    ]

    failed_llm_response_status_list = [
        is_failed_llm_generation_list[index] for index in function_variant_combination]

    # print(variant_obj_combination_list)  # [f,g]
    # print(failed_llm_response_status_list)

    stitch_back_to_source_code(
        main_source_parsed_info,
        variant_obj_combination_list,
        variant_source_code_sub_dir,
        source_file_name,
        num_functions,
        trial_no,
        function_variant_combination,
        num_functions_merge_back,
        failed_llm_response_status_list
    )


def function_name_replacer(
    renamed_function_body,
    target_to_replacer_func_name_dict,
    orig_target_functions_num_params,
):
    for target, replacer, target_function_num_params in zip(
        target_to_replacer_func_name_dict.keys(),
        target_to_replacer_func_name_dict.values(),
        orig_target_functions_num_params,
    ):
        renamed_function_body = replace_function_name_custom(
            renamed_function_body, target, replacer, target_function_num_params)
    return renamed_function_body


# time to do the stitching!!!
def find_variant_function_index(original_func_names_from_llm_variants, function_name):
    print('Finding the variant function index')
    print(original_func_names_from_llm_variants)
    print(function_name)
    for i, name in enumerate(original_func_names_from_llm_variants):
        if compare_signatures(name.strip(), function_name.strip()):
            return i
    return -1


def get_variant_func_forward_declarations(variant_obj_combination_list, failed_llm_response_status_list):
    # create forward declarations strings for the variant functions
    forward_declaration_set = set()  # to avoid duplicates

    # [f,g]
    for i, variantFunction_obj in enumerate(variant_obj_combination_list):
        # [f,g] -> [[a,b], [c,d]]
        # list of functions objects
        llm_response_status_for_function = failed_llm_response_status_list[i]

        if llm_response_status_for_function:
            continue

        variant_functions_obj_list = variantFunction_obj.variant_functions

        # [a,b]
        for variant_function_obj in variant_functions_obj_list:
            return_type = variant_function_obj["return_type"]
            name_with_params = variant_function_obj["name_with_params"]
            name_only = variant_function_obj["name_only"]
            # print(f"Name only: {name_only}")
            target_func_name = variantFunction_obj.orig_target_func_name

            if name_only not in ('main', 'wmain', 'WinMain', 'wWinMain', 'DllMain', '_tWinMain', '_tmain', target_func_name):
                forward_declaration_set.add(
                    f"{return_type} {name_with_params};")

    return list(forward_declaration_set)


def stitch_back_to_source_code(
    main_source_parsed_info,
    variant_obj_combination_list,
    source_code_output_dir,
    source_file_name,
    num_functions,
    trial_no,
    function_variant_comb_index_tuple,
    num_functions_merge_back,
    failed_llm_response_status_list
):

    # print('Stitching back to source code')
    updated_headers_list = []
    updated_source_code = ""

    main_source_headers, main_source_globals, main_source_functions, _, _ = (
        main_source_parsed_info
    )

    # if True in failed_llm_response_status_list:
    #     print("\n-------Failed to generate the LLM code. Stitching back the original source code-------\n")
    #     # create a new source code which is the same as the original source code
    #     updated_source_code = prepend_headers_globals(main_source_headers, main_source_globals)

    #     for function in main_source_functions:
    #         updated_source_code += function["body"] + "\n"
    # else:

    original_target_func_names = [
        variantFunction_obj.orig_target_func_name
        for variantFunction_obj in variant_obj_combination_list
    ]

    # print(original_target_func_names)

    # ------------------------ INFORMATION FOR NAME REPLACEMENT IF NEEDED LATER ------------------------

    # create a dictionary of target to replacer function names to replace names in the source code
    target_to_replacer_func_name_dict = {}
    orig_target_functions_num_params = []

    for variantFunction_obj in variant_obj_combination_list:
        target_to_replacer_func_name_dict[variantFunction_obj.orig_target_func_name.strip(
        )] = variantFunction_obj.replacer_variant_func_name.strip()

        orig_target_functions_num_params.append(
            variantFunction_obj.orig_target_func_param_count)

    # print(target_to_replacer_func_name_dict)
    # print(f'original target func num of params: {orig_target_functions_num_params}')

    # ------------------------ COMBINING INFORMATION FROM SOURCE AND VARIANTS ------------------------

    # create a new source code by combining information from the original source code and the generated code
    all_variant_headers = []

    print(f"\n\n------ Updating New Source Code with variant headers ( if any ) ------\n")
    for variantFunction_obj in variant_obj_combination_list:
        all_variant_headers.extend(variantFunction_obj.variant_headers)
        # print(variantFunction_obj.variant_functions)

    # First, create a set from main_source_headers for faster lookup

    # Then, create the updated list by including all items from main_source_headers
    # and only those items from all_variant_headers that are not in main_source_headers
    main_source_headers = [header.strip() for header in main_source_headers]
    all_variant_headers = [header.strip() for header in all_variant_headers]

    main_source_headers_set = set(main_source_headers)

    # print(f"Main source headers: {main_source_headers}")
    # print(f"All variant headers: {all_variant_headers}")

    updated_headers_list = main_source_headers + \
        [header for header in all_variant_headers if header not in main_source_headers_set]

    # updated_headers_list = list(set(main_source_headers).union(set(all_variant_headers)))

    # add the forward declarations to the updated headers list
    print(f"\n------ Updating New Source Code with new variant f() declarations ------\n")
    updated_headers_list.extend(get_variant_func_forward_declarations(variant_obj_combination_list, failed_llm_response_status_list))


    # first add the headers and globals
    updated_source_code = prepend_headers_globals(updated_headers_list, main_source_globals)

    ## LOOP THROUGH THE FUNCTIONS AND ADD THEM TO THE SOURCE CODE
    for function in main_source_functions:
        # print(f"Function name: {function['name_only']}")
        variant_index = find_variant_function_index(original_target_func_names, function["name_only"])

        if variant_index == -1:
            print(f"Working with non-variant/regular function: {function['name_with_params']}\n")
            # before adding the function body, replace the function names
            # renamed_function_body = function_name_replacer(
            #     function["body"], target_to_replacer_func_name_dict, orig_target_functions_num_params,)

            updated_source_code += function["body"] + "\n"
        else:
            print(f"Working with variant/LLM generated function: {function['name_with_params']}\n")
            # print(variant_obj_combination_list)
            # print('The index is: ', variant_index)
            required_variant_obj = variant_obj_combination_list[variant_index]

            # print('The required variant obj is: ', required_variant_obj.variant_functions)

            required_variant_obj_llm_response_status = failed_llm_response_status_list[variant_index]
            required_variant_obj_sub_variant_functions = required_variant_obj.variant_functions

            if required_variant_obj_llm_response_status:
                # print(f"Failed to generate the LLM code for the variant function: {function['name_with_params']}")
                # print("Updating the source code with the original function body\n")
                updated_source_code += function["body"] + "\n"
                continue

            # print(required_variant_obj.replacer_variant_func_name)
            print(required_variant_obj_sub_variant_functions)
            if len(required_variant_obj_sub_variant_functions) != 1:

                replacer_func_variant_body = ""

                for variant_function in required_variant_obj_sub_variant_functions:

                    '''
                    The following if-else condition handles the case of placing the replacer function at the end after placing 
                    all the sub-variant functions for that replacer function
                    '''

                    if not variant_function["name_only"].strip() == required_variant_obj.replacer_variant_func_name.strip():
                        updated_source_code += variant_function["body"] + "\n"
                    else:
                        replacer_func_variant_body = variant_function["body"] + "\n"

                updated_source_code += replacer_func_variant_body
            else:
                # print("updating the source code with the single variant function")
                # print(required_variant_obj_sub_variant_functions)

                updated_source_code += (
                    required_variant_obj_sub_variant_functions[0]["body"] + "\n"
                )

                print(updated_source_code)

    function_replaced_with_variant = "_".join(
        [
            str(function_index + 1)
            for function_index in function_variant_comb_index_tuple
        ]
    )

    source_file_extension = source_file_name.split(".")[-1]
    source_file_name_only = source_file_name.split(".")[0]
    # print(f"Function replaced with variant: {function_replaced_with_variant}")
    print(f"\n------ Creating the updated source code file: {source_file_name_only}_{num_functions}_trial_{trial_no+1}_func_{function_replaced_with_variant}.{source_file_extension} ------\n")
    # print(f"source code output dir: {source_code_output_dir}\n")
    # write the updated source code to a file
    with open(
        os.path.join(
            source_code_output_dir,
            f"{source_file_name_only}_{num_functions}_trial_{trial_no+1}_func_{function_replaced_with_variant}.{source_file_extension}"), "w",) as f:
        # fix the backslashes in the source code
        updated_source_code = fix_single_backslashes(updated_source_code)
        f.write(updated_source_code)
