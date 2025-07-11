import os
import time


from ollama_api import ollama_chat_api
from parse_llm_generated_code import parse_code

def get_llm_name_from_input(llm_input):
    llm_name_to_model_name = {
        "deepseek_33b": "deepseek-coder:33b-instruct",
        "deepseek_v2_16b": "deepseek-coder-v2:16b-lite-instruct-q4_0",
        "starcoder2": "starcoder2:instruct",
        "codestral": "codestral:latest",
        "codellama_7b": "codellama:7b-instruct",
        "codegemma_7b": "codegemma:7b-instruct",
        "codellama_13b": "codellama:13b-instruct",
        "llama3_8b": "llama3:8b-instruct-q4_0",
        "mistral": "mistral:7b-instruct",
    }

    return llm_name_to_model_name[llm_input]


def prepend_headers_globals(headers, globals):
    # add headers
    result = ""

    for header in headers:
        result += header + "\n"

    # add globals
    for global_ in globals:
        if type(global_) == dict:
            result += global_["body"] + "\n"
        else:
            result += global_ + "\n"

    return result


def prepend_function_def_with_batching(parsed_info, num_functions, batch_size):
    # combine headers, globals and a functions equal to num_functions into a single string
    headers, globals, functions, _, _ = parsed_info
    global_information = ""
    function_names = []
    function_param_count = []
    function_definitions = []
    function_objects = []

    global_information = prepend_headers_globals(headers, globals)

    temp_function_names = []
    temp_function_param_count = []
    temp_function_definitions = global_information
    temp_function_objects = []
    
    num_functions = min(num_functions, len(functions))

    for i in range(0, num_functions, batch_size):

        for j in range(i, min(i + batch_size, num_functions)):
            temp_function_objects.append(functions[j])
            temp_function_names.append(functions[j]["name_only"])
            temp_function_param_count.append(functions[j]["parameters_count"])
            temp_function_definitions += functions[j]["body"] + "\n"

        # add them to the main lists
        function_names.append(temp_function_names)
        function_definitions.append(temp_function_definitions)
        function_param_count.append(temp_function_param_count)
        function_objects.append(temp_function_objects)

        # clear the temporary list and re-add the global information
        temp_function_names = []
        temp_function_objects = []
        temp_function_definitions = global_information

    return function_definitions, function_objects,  len(functions), headers, globals


def prepend_function_defs(parsed_info, num_functions):
    # combine headers, globals and a functions equal to num_functions into a single string
    headers, globals, functions, _, _ = parsed_info
    result = ""
    function_names = []

    result = prepend_headers_globals(headers, globals)

    # add functions
    num_functions = min(num_functions, len(functions))

    for i in range(num_functions):
        function_names.append(functions[i]["name_with_params"])
        result += functions[i]["body"] + "\n"

    return result, function_names, len(functions)


def write_llm_response_to_file(output_dir, llm_response, file_name):
    #print(os.path.join(output_dir, file_name))
    with open(os.path.join(output_dir, file_name), "w") as f:
        f.write(llm_response)


def run_llm(llm_name, system_prompt, user_prompt, seed):
    start_time = time.time()
    # first call to warm up the model
    ollama_chat_api(llm_name, system_prompt, user_prompt, seed=seed)

    # second call to get the response time
    llm_response = ollama_chat_api(llm_name, system_prompt, user_prompt, seed=seed)
    end_time = time.time()
    model_response_time = end_time - start_time
    print(f"{llm_name} took {model_response_time} seconds")
    print("*" * 50)
    print("\n\n")

    return llm_response, model_response_time




def run_experiment_trial(
    llm,
    system_prompt,
    user_prompt,
    trial_no,
    llm_response_sub_dir_final,
    language_name,
    source_file_name,
    num_functions,
    seed,
    batch_num=-1,
    llm_responses_path=None,
):

    llm_response, model_response_time = run_llm(llm, system_prompt, user_prompt, seed)
    model_response_time_to_write = f"Response Time: {model_response_time} seconds\n\n"
    
    base_file_name = f"{source_file_name}_{num_functions}_trial_{trial_no+1}_batch_{batch_num}.txt"
    file_name = os.path.join(llm_response_sub_dir_final, base_file_name)

    print(f"\nWriting the LLM response to the file: {file_name}\n")
    write_llm_response_to_file(
        llm_response_sub_dir_final,
        model_response_time_to_write + language_name + llm_response,
        base_file_name,
    )
    
    if llm_responses_path is not None:
        llm_responses_path.add(file_name)

    return llm_response, model_response_time


def generate_code_from_llm_response(llm_response, language, headers, globals):

    llm_parsed_code = parse_code(llm_response, language=language)

    function_names = []
    llm_code_information = ""
    
    # adjust the headers with the original headers
    llm_gen_headers, llm_gen_globals, llm_gen_functions, _, _ = llm_parsed_code
    
    globals_no_dict = []
    llm_gen_globals_no_dict = []
    
    # This is to adjust the globals with the dictionaries such as structures and classes
    for global_ in globals:
        if type(global_) == dict:
            globals_no_dict.append(global_["body"])
        else:
            globals_no_dict.append(global_)
            
    for global_ in llm_gen_globals:
        if type(global_) == dict:
            llm_gen_globals_no_dict.append(global_["body"])
        else:
            llm_gen_globals_no_dict.append(global_)
    
    llm_gen_headers = list(set(headers).union(set(llm_gen_headers)))
    llm_gen_globals = list(set(globals_no_dict).union(set(llm_gen_globals_no_dict)))

    llm_code_information = prepend_headers_globals(llm_gen_headers, llm_gen_globals)
    # add functions
    llm_num_functions = len(
        llm_gen_functions
    )  # get the length of the generated functions

    for i in range(llm_num_functions):
        function_names.append(llm_gen_functions[i]["name_only"])
        llm_code_information += llm_gen_functions[i]["body"] + "\n"

    return llm_code_information, function_names, llm_num_functions




def verify_mapping_structure(mapping, error_message):
    """
    Checks if the mapping structure is correct and if so returns the mapping information.
    """
    
    target_func_name_from_mapping = None
    replacer_func_name_from_mapping = None
    
    try:
        '''
        assumes the mapping is in the format of 'original_func_name: replacer_variant_func_name|variant_func_name1|...|variant_func_nameN
        if available will work for 3,4 and 5 too. 
        '''
        mapping_list = mapping.split(":")
        
        if len(mapping_list) != 2:
            '''
            1. g|h|i|j|k
            2. g
            both cases may be possible
            '''
            print("Mapping information is not in the correct format!!!")
            return None
        
        '''
        if the mapping has f : g then it can have two cases
        1. f : g|h|i|j|k
        2. f : g
        both cases may be possible
        '''
        target_func_name_from_mapping = mapping_list[0]
        replacer_func_name_from_mapping = mapping_list[1].split("|")[0]        
    except:
        error_flag = True
        print(error_message)
        print("Mapping Information: ", mapping)
        print('\n')
    
    return target_func_name_from_mapping, replacer_func_name_from_mapping