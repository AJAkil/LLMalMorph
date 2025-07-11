#  python call_api.py --source_file=selected_samples/exeinfector/exeinfector.cpp --num_func=2 --llm=codestral:latest

import argparse
import os

import json
import pprint as pp
import re
import random

# custom imports
from tree_sitter_parser import (
    initialize_parser,
    read_source_code,
    extract_functions_globals_headers,
)

from utility_prompt_library import (
    get_prompt,
    generate_simple_prompt,
)
from parse_llm_generated_code import (
    parse_code,
    parse_json_from_llm_response,
    parse_code_any_format,
)
from variant_source_generator import generate_function_variant_obj_from_function_mapping, call_stitcher

from stitcher_util import create_output_directory


from pipeline_util import run_experiment_trial, write_llm_response_to_file, generate_code_from_llm_response, get_llm_name_from_input, prepend_function_def_with_batching


strategy_prompt_dict = {}
strat_all_order = []

def process_arguments():
    arg_parser = argparse.ArgumentParser(description="Parse C/C++ source code")
    arg_parser.add_argument("--source_file_dir", type=str, default="/home/newdrive/makil/projects/GenAI_Malware_Repository/development_code/selected_samples/exeinfector/source_codes/exeinfector_changed.cpp", help="The source files to be parsed")
    arg_parser.add_argument("--num_func", type=int, default=1, help="The number of functions to generate")
    arg_parser.add_argument("--llm", type=str, default="codestral", help="The API to use for code completion")
    arg_parser.add_argument("--output_dir", type=str, default="/home/newdrive/makil/projects/GenAI_Malware_Repository/development_code/selected_samples/exeinfector/llm_generated", help="The directory to save the output files")
    arg_parser.add_argument("--strategy", type=str, default="strat_1", help="The strategy to generate code")
    arg_parser.add_argument("--prompt_type", type=str, default="detailed", help="The prompt to use for code completion")
    arg_parser.add_argument("--trials", type=int, default=1, help="To provoke llm once or more times")
    arg_parser.add_argument("--func_batch_size", type=int, default=1, help="The number of function to process in a single batch")
    arg_parser.add_argument("--skip_over", type=int, default=0, help="The number of functions to skip over")
    arg_parser.add_argument("--num_functions_merge_back", type=int, default=1, help="The number of functions to merge back to the source code")
    arg_parser.add_argument("--retry_generation_attempts", type=int, default=5, help="The number of attempts to retry the generation of the function variant object")
    arg_parser.add_argument("--source_code_response_format", type=str, default="backticks", help="The format of the source code response from the LLM model")
    arg_parser.add_argument("--func_gen_scheme", type=str, default="sequential", help="The scheme to generate the function variants")
    arg_parser.add_argument("--indicator_bahavior", type=str, default=None, help="Category of specific behavioral indicators")
    return arg_parser.parse_args()
    


def sort_llm_response_path_list(llm_responses_path_list):
    llm_responses_path_list = sorted(llm_responses_path_list, key = lambda x: int(x.split('_')[-1].split('.')[0]))
    return llm_responses_path_list


def main():
    
    initial_seed = 42
    seed = initial_seed

    random.seed(seed)
    
    args = process_arguments()

    # based on the strategy, check if the output directory exists, if not create it

    variant_generation_strategy = args.strategy
    experiment_trial_no = args.trials
    func_batch_size = args.func_batch_size
    num_functions_merge_back = args.num_functions_merge_back
    retry_attempts = args.retry_generation_attempts
    source_code_response_format = args.source_code_response_format
    indicator_behavior = args.indicator_bahavior
    
    if indicator_behavior is None:
        strategy_sub_dir = create_output_directory(args.output_dir, variant_generation_strategy)
    else:
        strategy_sub_dir = create_output_directory(args.output_dir, f"{indicator_behavior}")
        



    num_functions = args.num_func
    llm = get_llm_name_from_input(args.llm)
    is_source_file_dir = os.path.isdir(args.source_file_dir)

    if not is_source_file_dir:
        source_files = [args.source_file_dir]
    else:
        # iterate the source file directory and get all the source files with root directory
        source_files = os.listdir(args.source_file_dir)
        
        # remove the foldres from the list
        source_files = [source_file for source_file in source_files if os.path.isfile(os.path.join(args.source_file_dir, source_file))]


    # ------------------- PROCESSING SOURCE FILES -------------------

    for source_file in source_files:
        
        # These two lists store the path of the llm responses and the variant function objects
        llm_responses_path_list = set()
        variant_function_objects_file_path = []
        is_failed_llm_generation_list = [] # this would have a list of list based on number of trials
        lines_of_code_generated_per_func = []
        seeds_per_func_per_trial = [] # this would have a list of list of seeds for each function based on number of trials
        llm_reponse_time_per_func = [] # this would have a list of list of response time for each function based on number of trials
        
        source_file_path = os.path.join(args.source_file_dir, source_file) if is_source_file_dir else source_file 
            
        # create a subdirectory for each source file
        
        source_file_sub_dir = create_output_directory(strategy_sub_dir, os.path.splitext(source_file.split("/")[-1])[0])    
        llm_sub_dir_final = create_output_directory(source_file_sub_dir, args.llm)
        num_func_sub_dir = create_output_directory(llm_sub_dir_final, f"{args.num_func}_functions")
        
        func_objs_sub_dir = create_output_directory(num_func_sub_dir, "function_variant_objects")
        
        llm_responses_sub_dir = create_output_directory(num_func_sub_dir, "llm_responses")
        
        variant_source_code_sub_dir = create_output_directory(num_func_sub_dir, "variant_source_code")
        variant_source_code_scheme_sub_dir = create_output_directory(variant_source_code_sub_dir, args.func_gen_scheme)
        
        is_failed_llm_generation = False
        

        """
        parser = initialize_parser(source_file_path)

        # get the name of the source file
        source_file_name = source_file.split("/")[-1]

        print(f"Processing source file: {source_file_name}")

        # get the source file extension
        file_extension = source_file.split(".")[-1]
        language_name = f"Language: {file_extension}\n"

        # Read the source code
        source_code = read_source_code(
            source_file_path
        )  # the original source code of the file in question
        tree = parser.parse(bytes(source_code, "utf8"))
        """
        
        # get the name of the source file
        source_file_name = source_file.split("/")[-1]
        
        # get the source file extension
        file_extension = source_file.split(".")[-1]
        language_name = f"Language: {file_extension}\n"
        print(f"\n\n------ Processing Source File: {source_file_name} ------\n\n")
        
        # ------------------- PARSING SOURCE CODE -------------------
        # parse the source code if it's already not parsed and saved to a file
        # parsed_info: headers, globals, functions, classes, structs of the source code
        
        try:
            with open(os.path.join(num_func_sub_dir, f"{source_file_name}_parsed_info.json"), "r") as f:
                parsed_info_data = json.load(f)
            
            print('------ Using the parsed info from the file ------')
                
            headers = parsed_info_data['headers']
            globals = parsed_info_data['globals']
            functions = parsed_info_data['functions']
            classes = parsed_info_data['classes']
            structs = parsed_info_data['structs']

            parsed_info = (headers, globals, functions, classes, structs)
            
        except:
            
            parser = initialize_parser(source_file_path)

            # Read the source code
            source_code = read_source_code(
                source_file_path
            )  # the original source code of the file in question
            tree = parser.parse(bytes(source_code, "utf8"))

            
            print(f"\n\n------ Parsing the Source Code: {source_file_name} ------\n\n")
            
            parsed_info = extract_functions_globals_headers(source_code, tree)
            
            headers, globals, functions, classes, structs = parsed_info
            print(globals)

            # ------------------- SAVING PARSED INFO -------------------
            # Prepare the data for serialization
            data_to_store = {
                "headers": headers,
                "globals": globals,
                "functions": functions,
                "classes": classes,
                "structs": structs
            }

            print(f"\n\n------ Saving Parsed Info for later usage ------\n\n")
            with open(os.path.join(num_func_sub_dir, f"{source_file_name}_parsed_info.json"), "w") as f:
                json.dump(data_to_store, f)    
            # ------------------- SAVING PARSED INFO -------------------


        # Extract functions, globals, and headers
        # parsed_info = extract_functions_globals_headers(source_code, tree)
        # # function_defs, function_names, total_source_file_functions = prepend_function_defs(parsed_info, num_functions)
        
        func_batch_size = (
            num_functions if func_batch_size == -1 else func_batch_size
        )  # adjust the batch size if it is -1

        (
            batch_function_defs,
            batch_function_objects,
            total_source_file_functions,
            headers,
            globals,
        ) = prepend_function_def_with_batching(
            parsed_info, num_functions, func_batch_size
        )

        # print(f"batch_function_defs: {batch_function_defs}")
        #print(f"batch_function_names: {batch_function_names}")

        print(f"\n\nTotal functions in source file: {total_source_file_functions}")
        print(f"Total Selected functions to modify: {num_functions}")
        # print(f"Selected functions: {function_names}")
        print(f"Transformation Strategy: {variant_generation_strategy}\n\n")

        # get the strategy number
        strategy_number = (
            1
            if variant_generation_strategy == "strat_all"
            else int(variant_generation_strategy.split("_")[1])
        )
        #print(f"Strategy Number: {strategy_number}")

        # print(function_defs)

        # create the prompt
        system_prompt = "You are an intelligent coding assistant who is expert in writing, editing, refactoring and debugging code. You listen to exact instructions and specialize in systems programming and use of C, C++ and C# languages with Windows platforms"
        #strategy_prompt = strategy_prompt_dict[variant_generation_strategy]
        
        code_supply_prompt = "Here is the code : \n"


        # wrap the logic below with the batch size

        skip_over = args.skip_over
        if skip_over > 0:
            print(f"Skipping over {skip_over} functions")
            batch_function_defs = batch_function_defs[skip_over:]
            batch_function_objects = batch_function_objects[skip_over:]
            total_source_file_functions -= skip_over

        trial_to_function_variant_obj_list_mapping = {} # this will store the variant functions object generated for each trial

        # create an empty list of variant function objects for each trial
        for trial_no in range(experiment_trial_no):
            trial_to_function_variant_obj_list_mapping[trial_no] = []
            is_failed_llm_generation_list.append([])
            lines_of_code_generated_per_func.append([])
            llm_reponse_time_per_func.append([])
            seeds_per_func_per_trial.append([])
            
        # store the function variant objects to use later in JSON format
        

        for func_defs, func_objs in zip(batch_function_defs, batch_function_objects):
            
            func_names = [func_obj['name_with_params'] for func_obj in func_objs]
            
            print(f"\n\n----------- Processing Function: {func_names} -----------\n\n")
            
            
            if args.prompt_type == "detailed":
                prefix_prompt = get_prompt(
                    len(func_names),
                    func_names,
                    variant_generation_strategy,
                    strategy_number,
                    language_name=file_extension,
                    is_json_prompt=False,
                    behavior=indicator_behavior
                )
            else:
                prefix_prompt = generate_simple_prompt(
                    len(func_objs),
                    func_names,
                    variant_generation_strategy,
                    strategy_number,
                    is_targetted_prompt=args.is_targetted_prompt,
                    language_name=file_extension,
                )

            user_prompt = prefix_prompt + "\n" + code_supply_prompt + func_defs
            batch_num = batch_function_objects.index(func_objs) + 1

            # DEBUG
            print("\n\n")
            print("-" * 20)
            print("*" * 20)
            print(f"System Prompt: {system_prompt}\n\n")
            print(f"User Prompt: {user_prompt} \n\n")
            print("*" * 20)
            print("-" * 20)
            print("\n\n")
            
            
            # ------------------- SAVING ORIGINAL FUNC VARIANT OBJS -------------------
            json_variant_obj_file_path = os.path.join(func_objs_sub_dir, f"{source_file_name}_orig_function_variant_objects_{func_objs[0]['name_only']}.json")
            variant_function_objects_file_path.append(json_variant_obj_file_path)
            
            if not os.path.exists(json_variant_obj_file_path):
            
                with open(json_variant_obj_file_path, "w") as f:
                    json.dump(func_objs, f)
                
            # ------------------- SAVING FUNC VARIANT OBJS -------------------
            

            if variant_generation_strategy == "strat_all":

                for trial_no in range(experiment_trial_no):  
                    
                    i = 0
                    
                    while True: # this loop handles the strategies
                        
                        try_again = 0
                            
                        while try_again < retry_attempts: # this loop handles the LLM generation retries

                            print("Trial Number:", trial_no + 1)
                            
                            llm_response, llm_response_time = run_experiment_trial(
                                llm,
                                system_prompt,
                                user_prompt,
                                trial_no,
                                llm_responses_sub_dir,
                                language_name,
                                source_file_name,
                                num_functions,
                                seed,
                                batch_num=batch_num,
                                llm_responses_path=llm_responses_path_list
                            )
                            
                            print("\n\n-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-")
                            print("-*-*-*-*-*-LLM Response: -*-*-*-*-*-*-*-*")
                            print(llm_response)
                            print("-*-*-*-*-*-LLM Response: -*-*-*-*-*-")
                            print("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-\n\n")
                            
                            # check if the LLM response has code blocks
                            code_blocks = re.findall(r'```(.*?)```', llm_response, re.DOTALL)
                            
                            if len(code_blocks) == 0:
                                print("-x-x-x-x-x-x-x- No code blocks found in the LLM response. Trying Again. -x-x-x-x-x-x-x-")
                                try_again += 1
                            else:
                                try_again = retry_attempts
                                
                        # create proxy LLM response with old function when the LLM generation fails after retries
                        if try_again == retry_attempts and len(code_blocks) == 0:
                            llm_response = f"```{file_extension}\n{func_defs}```"

                        if i == len(strat_all_order):
                            print("All strategies have been exhausted")
                            break

                        llm_generated_code, llm_function_names, llm_num_functions = generate_code_from_llm_response(llm_response, file_extension, headers, globals)
                        next_strategy = strat_all_order[i]
                        
                        print(f"\n\n======The next strategy is: {next_strategy}\n")

                        next_prefix_prompt = get_prompt(
                            llm_num_functions,
                            llm_function_names,
                            strategy_prompt_dict[next_strategy],
                            int(next_strategy.split("_")[1]),
                            language_name=file_extension,
                        )

                        next_user_prompt = (
                            next_prefix_prompt + "\n" + code_supply_prompt + llm_generated_code
                        )

                        print("\n\n=*=*=*=*=*=*=*=*Next User Prompt: =*=*=*=*=*=*=*=*\n\n")
                        print(next_user_prompt)

                        user_prompt = next_user_prompt

                        i += 1

                    print("Generated With All Strategies")

                    segmented_code, lines_of_code_generated, mapping = parse_code_any_format(
                        llm_response, language=file_extension, source_code_response_format=source_code_response_format
                    )
                    
                    # only processing segmented_code for now
                    if segmented_code is None:
                        print("Error in parsing Generated LLM Code, Trying Again")
                        try_again += 1
                        
                        seed = random.randint(0, 1000) # trying with a new seed for the next attempt
                        
                    else:
                        try_again = retry_attempts
                    
                    # print("*" * 50, "Parsed Code: ", "*" * 50)
                    # print_information(segmented_code)
                    # print("*" * 50, "Mapping: ", "*" * 50)
                    # print(mapping)
                    
                    seed = initial_seed # reset the seed to the initial seed
                    
                    if segmented_code is None:
                        print("-*-*-*-*-*-*\n\nSegmented code is still None. Putting back the original code\n\n-*-*-*-*-*-*")
                        segmented_code = parsed_info
                        is_failed_llm_generation = True
                        lines_of_code_generated = 0
                        seed = initial_seed # reset the seed to the initial seed

                    print("\n\nGenerating the function variant object from the function mapping and segmented code\n")
                    
                    function_variant_obj = generate_function_variant_obj_from_function_mapping(mapping, segmented_code, func_objs, variant_generation_strategy)
                    

                    # storing the variant functions object for each trial

                    print("Storing the variant function object for each trial")
                    trial_to_function_variant_obj_list_mapping[trial_no].append(function_variant_obj)
                    
                    print("Storing the LLM failed generation status for each trial")
                    is_failed_llm_generation_list[trial_no].append(is_failed_llm_generation)
                    lines_of_code_generated_per_func[trial_no].append(lines_of_code_generated)
                    seeds_per_func_per_trial[trial_no].append(seed)
                    is_failed_llm_generation = False

            else:
                #print("For a single strategy")
                
                for trial_no in range(experiment_trial_no):
                    
                    #print("Trial Number:", trial_no + 1)
                    try_again = 0
                    
                    while try_again < retry_attempts:
                        
                        llm_response, llm_response_time = run_experiment_trial(
                            llm,
                            system_prompt,
                            user_prompt,
                            trial_no,
                            llm_responses_sub_dir,
                            language_name,
                            source_file_name,
                            num_functions,
                            seed,
                            batch_num=batch_num,
                            llm_responses_path=llm_responses_path_list
                        )

                        print('RAW LLM Response: ')
                        # print(type(llm_response))
                        print(llm_response)

                        segmented_code, lines_of_code_generated, mapping = parse_code_any_format(
                            llm_response,
                            language=file_extension,
                            source_code_response_format=source_code_response_format,
                        )

                        # if segmented_code is None or mapping is None:
                        #     print("Error in parsing Generated LLM Code, Trying Again")
                        # else:
                        #     try_again = False
                        
                        # only processing segmented_code for now
                        if segmented_code is None:
                            print("\n\nError in parsing Generated LLM Code or LLM Code did not generate. Trying Again\n\n")
                            try_again += 1
                            
                            seed = random.randint(0, 10000) # trying with a new seed for the next attempt
                            
                        else:
                            try_again = retry_attempts

                    # print("*" * 50, "Parsed Code: ", "*" * 50)
                    # print_information(segmented_code)
                    # print("*" * 50, "Mapping: ", "*" * 50)
                    # print(mapping)
                    
                    seeds_per_func_per_trial[trial_no].append(seed)
                    seed = initial_seed # reset the seed to the initial seed
                    
                    if segmented_code is None:
                        print("-*-*-*-*-*-*\n\nSegmented code is still None. Putting back the original code\n\n-*-*-*-*-*-*")
                        segmented_code = parsed_info
                        is_failed_llm_generation = True
                        lines_of_code_generated = 0
                        
                        
                    print("\n\nGenerating the function variant object from segmented LLM code\n")
                    
                    function_variant_obj = generate_function_variant_obj_from_function_mapping(
                        mapping, segmented_code, func_objs, variant_generation_strategy)
                    

                    # storing the variant functions object for each trial

                    print("\n\nStoring the variant function objects ")
                    trial_to_function_variant_obj_list_mapping[trial_no].append(function_variant_obj)
                    
                    print("Storing the LLM failed generation status\n\n")
                    is_failed_llm_generation_list[trial_no].append(is_failed_llm_generation)
                    lines_of_code_generated_per_func[trial_no].append(lines_of_code_generated)
                    is_failed_llm_generation = False
                    llm_reponse_time_per_func[trial_no].append(round(float(llm_response_time), 3))

        # ------------------- SAVING PATH INFO -------------------
        
        # if not os.path.exists(os.path.join(num_func_sub_dir, f"{source_file_name}_llm_responses_path.json")):
            
        file_path_dict = {
            'llm_responses_path_list' : sort_llm_response_path_list(list(llm_responses_path_list)),
            'variant_function_objects_file_path': variant_function_objects_file_path,
            'num_functions': num_functions,
            'experiment_trial_no': experiment_trial_no,
            'func_batch_size': func_batch_size,
            'source_code_response_format': source_code_response_format,
            'is_failed_llm_generation_list': is_failed_llm_generation_list,
            'lines_of_code_generated_per_func': lines_of_code_generated_per_func,
            'llm_reponse_time_per_func': llm_reponse_time_per_func,
            'seeds_per_func_per_trial': seeds_per_func_per_trial
        }
        
        # print(file_path_dict)
        print(f"\n\n------ Saving useful file/folder path and other information for later usage ------\n\n")
        with open(os.path.join(num_func_sub_dir, f"{source_file_name}_llm_responses_path.json"), "w") as f:
            json.dump(file_path_dict, f)


            # print("\n\n")
            # print("-" * 20)
            # print("*" * 20)
            # print(f"Processed Batch {batch_num + 1} \n\n")
            # print("*" * 20)
            # print("-" * 20)
            # print("\n\n")

        # call the stitcher function to stitch the source code back together
        call_stitcher(parsed_info, variant_source_code_scheme_sub_dir, source_file_name,
                      num_functions, batch_num, num_functions_merge_back, 
                      trial_to_function_variant_obj_list_mapping, is_failed_llm_generation_list,
                      args.func_gen_scheme)

     
        '''
        print(user_prompt)

        for trial_no in range(experiment_trial_no):
            print('Trial Number:', trial_no+1)
            run_experiment_trial(llm, system_prompt, user_prompt, trial_no, llm_sub_dir_final, language_name, source_file_name, num_functions)

        elif llm == 'all':

            models = ['codellama:7b-instruct', 'codegemma:7b-instruct', 'deepseek-coder:6.7b-instruct', 'llama3:8b-instruct-q4_0']
            model_names = ['codellama_7b', 'codegemma_7b', 'deepseek-coder_6.7b', 'llama3_8b']
            model_response_time = 0

            for model, model_name in zip(models, model_names):
                start_time = time.time()
                llm_response = ollama_chat_api(model, system_prompt, user_prompt)
                end_time = time.time()

                model_response_time = f'Response Time: {end_time - start_time} seconds\n\n'
                print(f"{model} {model_response_time}")
                write_llm_response_to_file(model_response_time + language_name + llm_response, f'{model_name}_response.txt')

        if llm != 'all':
            model_response_time = f'Response Time: {model_response_time} seconds\n\n'
            write_llm_response_to_file(model_response_time + language_name + llm_response, f'{llm}_response.txt')
        print(completion)
        '''
        
        print("*" * 50)
        print("----------- Done processing source file -----------")
        print("*" * 50)
        print("\n\n")


if __name__ == "__main__":
    main()
