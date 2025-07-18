'''
 python variant_source_generator.py \
    --num_functions_merge_back=2 \
    --source_code_file_path=/home/newdrive/makil/projects/GenAI_Malware_Repository/development_code/selected_samples/exeinfector/source_codes/exeinfector_changed.cpp \
    --cached_dir=/home/newdrive/makil/projects/GenAI_Malware_Repository/development_code/selected_samples/exeinfector/llm_generated_paper/strat_6/exeinfector_changed/codestral/4_functions
'''


import json
import argparse
import os


from stitcher_util import stitcher
import json
from parse_llm_generated_code import parse_code_any_format
from tree_sitter_parser import print_information
from wrapper_class import VariantFunction


def get_replacer_func_name(original_func_objs, variant_func_objs):
    """
    Get the replacer function name from the variant functions generated from the original function.
    Args:
        original_func_objs (list): A list of dictionaries containing the information of the original functions.
        variant_func_objs (list): A list of dictionaries containing the information of the variant functions generated by llm from the original functions.

    Returns:
        str: The name of the replacer function.
    """

    replacer_func_name = ""
    target_func_return_type = original_func_objs[0]["return_type"]
    target_func_param_count = original_func_objs[0]["parameters_count"]
    target_func_param_type_list = original_func_objs[0]["parameter_type_list"]

    # print("Target function parameter type list: ", target_func_param_type_list)
    # print(variant_func_objs)
    
    if len(variant_func_objs) == 1:
        replacer_func_name = variant_func_objs[0]["name_only"]
        return replacer_func_name

    for variant_func in variant_func_objs:
        variant_func_return_type = variant_func["return_type"]
        variant_func_parameter_count = variant_func["parameters_count"]
        variant_func_parameter_type_list = variant_func["parameter_type_list"]

        # print("Variant function parameter type list: ",
        #       variant_func_parameter_type_list)

        if target_func_return_type == variant_func_return_type and target_func_param_count == variant_func_parameter_count and target_func_param_type_list == variant_func_parameter_type_list:
            replacer_func_name = variant_func["name_only"]

    return original_func_objs[0]["name_only"] if replacer_func_name == "" else replacer_func_name


def generate_function_variant_obj_from_function_mapping(mapping, segmented_code, func_objs, variant_generation_strategy=None):
    """
    Generates a function variant object from the function mapping and segmented code.

    Args:
        mapping (str): The mapping information generated by the llm.
        segmented_code (tuple): A tuple containing the segmented code information.
        func_objs (list): A list of dictionaries containing the information of the original functions.

    Returns:
        VariantFunction: The variant function object with necessary information.

    Notes:
        This function assumes that the mapping information is generated for a single function variant by the llm.
    """

    variant_headers, variant_globals, variant_functions, _, _ = segmented_code
    print('Inside segmented code!')
    print(variant_functions)
    variant_function_names_from_parser = [
        variant_func['name_only'] for variant_func in variant_functions]
    variant_function_names = []
    error_message = "!!!!!!!!!Mapping information is not available or erronous!!!!!!!!!"
    error_flag = False

    # from parser assuming batch size of 1 dealing with a single function at a time
    orig_target_func_name = func_objs[0]['name_only']
    orig_target_func_param_count = func_objs[0]['parameters_count']
    variant_function_names = [variant_func['name_only']
                              for variant_func in variant_functions]
    #print(f"\n---Variant Function Names from Parser: {variant_function_names}----\n")

    replacer_func_name = get_replacer_func_name(func_objs, variant_functions)
    # variant_function_names = [replacer_func_name]

    # handle the case if the mapping information is erronous but there are multple functions generated from a single function
    # this will work with batch size of 1 and only if the name of the target func is kept the same as the replacer func
    '''
    if error_flag:
        print("Handling the case of multiple functions generated from a single function but mapping is erronous")

        if len(variant_functions) == 1:
            replacer_func_name = variant_functions[0]["name_only"]
            variant_function_names = [replacer_func_name]
        else:
            for generated_function in variant_functions:
                # this is for strategy 3
                if compare_signatures(
                    generated_function["name_only"], orig_target_func_name
                ):
                    replacer_func_name = generated_function["name_only"]

            variant_function_names.append(generated_function["name_only"])
    '''

    # ------ Debugging ------
    # print(f"Original Function Name: {orig_target_func_name}")
    # print(f"Replacer Function Name: {replacer_func_name}")
    # print(f"Variant Function Names: {variant_function_names}")

    variant_function_obj = VariantFunction(
        variant_headers=variant_headers,
        variant_globals=variant_globals,
        variant_functions=variant_functions,
        orig_target_func_name=orig_target_func_name,
        orig_target_func_param_count=orig_target_func_param_count,
        replacer_variant_func_name=replacer_func_name,
        variant_function_names=variant_function_names,
    )

    return variant_function_obj


def store_func_variant_objects(segmented_code, mapping,
                               trial_to_function_variant_obj_list_mapping, trial_no,
                               func_obj, parsed_info, print_info=True):
    

    if segmented_code is None:
        print("-*-*-*-*-*-*\n\nSegmented code is None. Putting back the original code\n\n-*-*-*-*-*-*")
        segmented_code = parsed_info
    
    if print_info:
        print("*" * 50, "Parsed Code: ", "*" * 50)
        print_information(segmented_code)
    
    print("Generating the function variant object from the function mapping and segmented code")

    function_variant_obj = generate_function_variant_obj_from_function_mapping(
        mapping, segmented_code, func_obj
    )

    # storing the variant functions object for each trial

    # print("Storing the variant function object for each trial")
    # print(function_variant_obj.variant_functions)
    trial_to_function_variant_obj_list_mapping[trial_no].append(
        function_variant_obj)


def call_stitcher(parsed_info, source_code_output_dir, source_file_name, 
                  num_functions, batch_num, num_functions_merge_back,
                  trial_to_function_variant_obj_list_mapping, is_failed_llm_generation_list,
                  func_gen_scheme):

    #print("Sanity Check:")
    # for (trial, function_variant_obj_list) in trial_to_function_variant_obj_list_mapping.items():
    #     print(f"Trial Number: {trial+1}")
    #     for function_variant_obj in function_variant_obj_list:
    #         print(function_variant_obj.variant_functions)

    # create the information tuple for stitiching
    info_tuple = (
        parsed_info,
        source_code_output_dir,
        source_file_name,
        num_functions,
        batch_num,
        num_functions_merge_back,
    )

    print("\n\n")
    print("#" * 150)
    print("*" * 50, "Stitching the source code back together", "*" * 50)
    print("#" * 150)
    print("\n\n")
    stitcher(trial_to_function_variant_obj_list_mapping,
             info_tuple, is_failed_llm_generation_list, func_gen_scheme)


def read_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def generate_parsed_info(parsed_info_json):
    parsed_info_data = read_json_file(parsed_info_json)
    headers = parsed_info_data['headers']
    globals = parsed_info_data['globals']
    functions = parsed_info_data['functions']
    classes = parsed_info_data['classes']
    structs = parsed_info_data['structs']

    parsed_info = (headers, globals, functions, classes, structs)

    return parsed_info


def process_function_objects(func_objs_json_files_path_list):
    main_sample_func_objects = []
    for func_obj_file_path in func_objs_json_files_path_list:
        func_objs = read_json_file(func_obj_file_path)
        main_sample_func_objects.append(func_objs)
    return main_sample_func_objects


def read_llm_responses(llm_responses_path_list):
    llm_responses = []
    for llm_response in llm_responses_path_list:
        with open(llm_response, 'r') as file:
            llm_responses.append(file.read())
    return llm_responses


def parse_arguments_single_file_old():
    parser = argparse.ArgumentParser(
        description="Process input parameters for the script.")
    parser.add_argument("--file_path_list_json_path", default="/home/newdrive/makil/projects/GenAI_Malware_Repository/development_code/selected_samples/exeinfector/llm_generated/strat_1/4_functions/codestral/exeinfector_changed.cpp_generated_file_path_list.json")
    parser.add_argument("--parsed_info_json", default="/home/newdrive/makil/projects/GenAI_Malware_Repository/development_code/selected_samples/exeinfector/llm_generated/strat_1/4_functions/codestral/exeinfector_changed.cpp_parsed_info.json")
    parser.add_argument("--variant_source_code_sub_dir",
                        default="/home/newdrive/makil/projects/GenAI_Malware_Repository/development_code/selected_samples/exeinfector/llm_generated/strat_1/4_functions/codestral")
    parser.add_argument("--file_extension", default="cpp")
    parser.add_argument("--source_code_response_format", default="backticks")
    parser.add_argument("--num_functions", type=int, default=4)
    parser.add_argument("--batch_num", type=int, default=1)
    parser.add_argument("--num_functions_merge_back", type=int, default=4)
    parser.add_argument("--source_file_name",
                        default="exeinfector_changed.cpp")
    parser.add_argument("--experiment_trial_no", type=int, default=1)

    return parser.parse_args()


def parse_arguments_multifile():
    parser = argparse.ArgumentParser(description="Process input parameters for the script.")

    parser.add_argument(
        "--source_code_dir", default="/home/newdrive/makil/projects/GenAI_Malware_Repository/development_code/selected_samples/Hidden_VNC_BOT/hiddenvnc_code_files")
    parser.add_argument("--cached_dir", default="/home/newdrive/makil/projects/GenAI_Malware_Repository/development_code/selected_samples/Hidden_VNC_BOT/hiddenvnc_code_files/llm_generated/strat_3/5_functions/codestral")
    parser.add_argument("--num_functions_merge_back", type=int, default=4)

    return parser.parse_args()

def parse_arguments_single_file():
    parser = argparse.ArgumentParser(description="Process input parameters for the script.")

    parser.add_argument(
        "--source_code_file_path", default="/home/newdrive/makil/projects/GenAI_Malware_Repository/development_code/selected_samples/exeinfector/source_codes/exeinfector_changed.cpp")
    parser.add_argument("--cached_dir", default="/home/newdrive/makil/projects/GenAI_Malware_Repository/development_code/selected_samples/exeinfector/llm_generated_paper/strat_6/exeinfector_changed/codestral/4_functions")
    parser.add_argument("--num_functions_merge_back", type=int, default=2)
    parser.add_argument("--func_gen_scheme", default="sequential")

    return parser.parse_args()


def generate_variant_single_file_old(file_path_list_json_path, parsed_info_json, llm_sub_dir_final, file_extension, source_code_response_format, num_functions, batch_num, num_functions_merge_back, source_file_name, experiment_trial_no):
    # Load JSON file paths
    file_path_list_dict = read_json_file(file_path_list_json_path)
    llm_responses_path_list = file_path_list_dict['llm_responses_path_list']
    func_objs_json_files_path_list = file_path_list_dict['variant_function_objects_file_path']

    # Process function objects
    main_sample_func_objects = process_function_objects(
        func_objs_json_files_path_list)

    # Read LLM responses
    llm_responses = read_llm_responses(llm_responses_path_list)
    parsed_info = generate_parsed_info(parsed_info_json)

    # Perform assertions
    assert len(main_sample_func_objects) == len(
        llm_responses), "The number of function objects and llm responses do not match"

    # Initialize mapping for trial to function variant object list
    trial_to_function_variant_obj_list_mapping = {
        trial_no: [] for trial_no in range(experiment_trial_no)}
    
    print(f"LLM Responses: {llm_responses}")

    # Process each function object and LLM response
    for i, func_obj in enumerate(main_sample_func_objects):
        for trial_no in range(experiment_trial_no):
            # Assuming store_func_variant_objects is a function that processes each function object and LLM response
            
            segmented_code, mapping = parse_code_any_format
            (
            llm_responses[i],
            file_extension,
            source_code_response_format
            )
            
            store_func_variant_objects(
                segmented_code,
                mapping,
                trial_to_function_variant_obj_list_mapping,
                trial_no,
                func_obj,
                parsed_info
            )

    # Call stitcher function
    # Assuming parsed_info is loaded from parsed_info_json and call_stitcher is a defined function
    call_stitcher(parsed_info, llm_sub_dir_final, source_file_name, num_functions,
                  batch_num, num_functions_merge_back, trial_to_function_variant_obj_list_mapping)



def generate_variant(file_path_list_json_path, parsed_info_json, variant_source_code_sub_dir, source_file_extension,
                    num_functions_merge_back, source_file_name, func_gen_scheme):
    # Load JSON file paths
    print(f"\n\n-*-*-*-*-*- Reading File Path and necessary information -*-*-*-*-*-\n\n")
    file_path_list_dict = read_json_file(file_path_list_json_path)
    llm_responses_path_list = file_path_list_dict['llm_responses_path_list']
    func_objs_json_files_path_list = file_path_list_dict['variant_function_objects_file_path']
    
    num_functions = file_path_list_dict['num_functions']
    batch_num = file_path_list_dict['func_batch_size']
    source_code_response_format = file_path_list_dict['source_code_response_format']
    experiment_trial_no = file_path_list_dict['experiment_trial_no']
    is_failed_llm_generation_list = file_path_list_dict['is_failed_llm_generation_list']
    

    # Process function objects
    main_sample_func_objects = process_function_objects(
        func_objs_json_files_path_list)

    # Read LLM responses
    print(f"\n\n-*-*-*-*-*- Read LLM Responses and Saved main source code parsed information  -*-*-*-*-*-\n\n")
    llm_responses = read_llm_responses(llm_responses_path_list)
    parsed_info = generate_parsed_info(parsed_info_json)
    
    
    #print(f"LLM Responses path list: {llm_responses_path_list}")

    # Perform assertions
    assert len(main_sample_func_objects) * experiment_trial_no ==  len(llm_responses), f"The number of function objects {len(main_sample_func_objects)} and llm responses {experiment_trial_no * len(llm_responses)} do not match"

    # Initialize mapping for trial to function variant object list
    trial_to_function_variant_obj_list_mapping = {
        trial_no: [] for trial_no in range(experiment_trial_no)}

    # Process each function object and LLM response
    for i, func_obj in enumerate(main_sample_func_objects):
        for trial_no in range(experiment_trial_no):
            # Assuming store_func_variant_objects is a function that processes each function object and LLM response
            #pp.pprint(llm_responses[i])
            print('pop ??? ', func_obj[0]['name_only'])
            
            segmented_code, _ , mapping = parse_code_any_format(
            llm_responses[i],
            source_file_extension,
            source_code_response_format
            )
            
            store_func_variant_objects(
                segmented_code,
                mapping,
                trial_to_function_variant_obj_list_mapping,
                trial_no,
                func_obj,
                parsed_info
            )

    # Call stitcher function
    # Assuming parsed_info is loaded from parsed_info_json and call_stitcher is a defined function

    call_stitcher(parsed_info, variant_source_code_sub_dir, source_file_name, num_functions,
                  batch_num, num_functions_merge_back, trial_to_function_variant_obj_list_mapping,
                  is_failed_llm_generation_list, func_gen_scheme)


def generate_variants_multifile():
    args = parse_arguments_multifile()

    source_code_dir = args.source_code_dir
    num_functions_merge_back = args.num_functions_merge_back
    cached_dir = args.cached_dir

    # get all the files in the source code directory which are files
    source_code_files = [f for f in os.listdir(
        source_code_dir) if os.path.isfile(os.path.join(source_code_dir, f))]

    # get all the files in the cached directory which are directories
    cached_dirs = [f for f in os.listdir(
        cached_dir) if os.path.isdir(os.path.join(cached_dir, f))]

    assert len(source_code_files) == len(
        cached_dirs), f"The number of source code files({len(source_code_files)}) and cached directories({len(cached_dirs)}) do not match"
    
    source_code_files.sort()
    cached_dirs.sort()
    
    print(f"Source Code Files: {source_code_files}")
    print(f"Cached Directories: {cached_dirs}")

    for file, file_dir in zip(source_code_files, cached_dirs):
        print(f"Processing file: {file}")
        # get the file extension
        file_extension = file.split('.')[-1]

        # get the file path
        file_path = os.path.join(source_code_dir, file)

        # get the file name
        source_file_name = file.split('/')[-1]
        
        # get the json files in the cached directory
        cached_files_and_dirs = os.listdir(os.path.join(cached_dir, file_dir))
        
        print(cached_files_and_dirs)
        
        for f in cached_files_and_dirs:
            if 'llm_responses_path.json' in f:
                file_path_list_json_path = os.path.join(cached_dir, file_dir, f)
            
            elif 'parsed_info.json' in f:
                parsed_info_json = os.path.join(cached_dir, file_dir, f)
            
            elif 'variant_source_code' in f:
                variant_source_code_sub_dir = os.path.join(cached_dir, file_dir, f)
    
        # generate the variant
        generate_variant(file_path_list_json_path, parsed_info_json, variant_source_code_sub_dir, 
                         file_extension, num_functions_merge_back, source_file_name)

        print(f"\n\n-*-*-*-*-*-Processing of file: {file} is complete-*-*-*-*-*-\n\n")


def generate_variants_single_file():
    args = parse_arguments_single_file()

    source_code_file_path = args.source_code_file_path
    num_functions_merge_back = args.num_functions_merge_back
    cached_dir_path = args.cached_dir
    func_gen_scheme = args.func_gen_scheme


    # get all the files in the cached directory which are directories
    cached_dirs = [f for f in os.listdir(cached_dir_path) if os.path.isdir(os.path.join(cached_dir_path, f))]
    
    # get the name of the desired directory
    source_file_name_with_ext = source_code_file_path.split('/')[-1]
    source_file_name = source_file_name_with_ext.split('.')[0]
    source_file_extension = source_file_name_with_ext.split('.')[-1]
    
    # source_file_cache_dir = None
    
    # for dir in cached_dirs:
    #     if source_file_name == dir:
    #         source_file_cache_dir = dir
    #         break
    
    # assert source_file_cache_dir is not None, f"The desired directory for the source file {source_file_name} is not found in the cached directories"

    print(f"\n\n-*-*-*-*-*- Processing file: {source_file_name} -*-*-*-*-*-\n\n")
    
    # get the json files in the cached directory
    cached_files_and_dirs = os.listdir(cached_dir_path)
    
    #print(cached_files_and_dirs)
    
    for f in cached_files_and_dirs:
        if f'llm_responses_path.json' in f:
            file_path_list_json_path = os.path.join(cached_dir_path, f)
        
        elif 'parsed_info.json' in f:
            parsed_info_json = os.path.join(cached_dir_path, f)
        
        elif 'variant_source_code' in f:
            variant_source_code_sub_dir = os.path.join(cached_dir_path, f)
            
            variant_source_code_sub_dirs = os.listdir(variant_source_code_sub_dir)
            
            found = False
            for dir in variant_source_code_sub_dirs:
                if func_gen_scheme == dir:
                    found = True
                    break 
            
            if found:
                 variant_source_code_output_dir = os.path.join(variant_source_code_sub_dir, func_gen_scheme)
            else:
                # create the scheme directory first and then join
                os.mkdir(os.path.join(variant_source_code_sub_dir, func_gen_scheme))
                variant_source_code_output_dir = os.path.join(variant_source_code_sub_dir, func_gen_scheme)
            
            #print(f"Variant Source Code Output Directory: {variant_source_code_output_dir}")

    # generate the variant
    generate_variant(file_path_list_json_path, parsed_info_json, variant_source_code_output_dir, 
                        source_file_extension, num_functions_merge_back, source_file_name_with_ext, func_gen_scheme)

    print(f"\n\n-*-*-*-*-*- Processing of file: {source_file_name} is complete -*-*-*-*-*-\n\n")

if __name__ == "__main__":
    generate_variants_single_file()
    
