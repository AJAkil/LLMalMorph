"""
strategy_prompt_dict = {
    "strat_1": (
        "1. Remove code redundancies.\n"
        "2. Identify performance bottlenecks and fix them.\n"
        "3. Simplify the code's logic or structure and optimize data structures and algorithms if applicable.\n"
        "4. Use language-specific features or modern libraries if applicable."
    ),
    "strat_2": (
        "1. Check error handling and edge cases.\n"
        "2. Follow coding practices and style guidelines.\n"
        "3. Add proper documentation to classes and functions, and comments for complex parts.\n"
    ),
    "strat_3": "Make the code reusable by dividing supplied functions into smaller function blocks if and where applicable. The smaller functions should be called inside the respective supplied functions as needed.",
    "strat_4": (
        "1. Identify security vulnerabilities and fix them.\n"
        "2. If the function you are modifying contains cryptographic operations, change the cryptographic library used for those operations. If no cryptographic operations are present, no changes are necessary.\n"
        "3. Follow secure coding standards and guidelines."
    ),
    "strat_5": (
        "1. Change the given function's and LOCAL variable's names to meaningless, hard-to-understand strings which are not real words. DO NOT redefine or rename global variables (given to you) and names of functions that are called inside the given function ( might be defined elsewhere ) under any circumstances.\n"
        "However if the given function name is any of `main`, `wmain`, `WinMain`, `wWinMain`, `DllMain`, `_tWinMain`, `_tmain` do not change it's name, only change the local variable's names inside the function.\n"
        "2. Add unnecessary jump instructions, loops, and conditional statements inside the functions.\n"
        "3. Add unnecessary functions and call those functions inside the original functions.\n"
        "4. Add anti-debugging techniques to the code.\n"
        "5. If there are loops/conditional statements in the code change them to their equivalent alternatives and make them more difficult to follow.\n"
        "6. Incorporate code to the variants that activates under very rare and obscure cases without altering core functionality, making the rare code hard to detect during testing."
    ),
    "strat_6": (
        "1. Identify all Windows API function calls in the given functions.\n"
        "2. If there are such function calls, replace each identified Windows API function call with an alternative Windows API function call or sequence of calls that achieves the same task.\n"
        "3. If applicable, use indirect methods or wrappers around the Windows API calls to achieve the same functionality.\n"
        "4. Ensure that the functionality remains the same after the replacement."
    ),
    "error_checking": (
        "1. Check for potential syntactic and semantic errors in the given functions.\n"
        "2. If you find any errors, correct them.\n"
        "3. Ensure that the corrected functions maintain the same functionality as the original functions."
    ),
    "strat_all": (
        "1. Remove code redundancies.\n"
        "2. Identify performance bottlenecks and fix them.\n"
        "3. Simplify the code's logic or structure and optimize data structures and algorithms if applicable.\n"
        "4. Use language-specific features or modern libraries if applicable."
    ),
}

strat_all_order = [
    "strat_2",
    "strat_4",
    "strat_3",
    "strat_5",
]
"""



def get_malicious_detection_prompt(language_name):
    prompt = (
        f"I am providing you with some functions from a source code file written in {language_name}. "
        "Observe each of the functions carefully and score them from 1-10 based on their maliciousness. "
        "Here are the functions:"
    )
    return prompt

# "4. Consider using Alternate Data Streams (ADS) to achieve the same functionality if and where applicable.\n"

# "1. Make the code reusable by dividing functions into smaller function blocks and classes/structures if and where applicable.",


############################################################################################
# OLD PREFIX PROMPT
# prefix_prompt = (
# f"Below this prompt you are provided headers, global variables, class and struct definitions "
# f"and {num_functions} global function definition(s). "
# f"As a coding assistant, your job is to GENERATE REUSABLE CODE by dividing {', '.join([func_name for func_name in function_names])} functions to smaller sub-functions IF APPLICABLE."
# f"The generated code MUST MAINTAIN the same functionality as the original code. "
# f"Modify ONLY the {num_functions} free/global function(s) "
# f"named {', '.join([func_name for func_name in function_names])}.\n"
# f"YOU MUST Follow these EXTRA instructions:\n"
# f"1. MUST NOT regenerate the extra information such as headers, global variables, structs and classes provided to you for context.\n"
# f"2. MUST NOT regenerate the original functions code {', '.join([func_name for func_name in function_names])}.\n"
# f"3. ONLY generate the function variants and any new headers/libraries you used.\n"
# f"4. MUST NOT generate any extra natural language messages/comments.\n"
# f"5. MUST Generate the modified functions within ```  ``` tags.\n"
# f"6. MUST DO: Create a mapping of the original function name to your generated functions name/names with all parameters in this way\n"
# f"original function name : new function name / several new function names.\nExample:\n"
# f"if original function is void f(int a) and your new generated functions are void g(int a) and int h(int b) then you MUST provide me the information in the ~~~ ~~~ tags in this format:\n~~~\n f(int a) : g(int a), h(int b) \n~~~"
# )

# prompt += (
#             f"7. When you change the name of any function to something unreadable make sure to provide the mapping of the original function to the "
#             f"generated function. This step is CRUCIAL AND MUST always be completed. For example, If the original function is `int func(char* s, int t)` and your generated variant with the given instruction is `int xgxhxs(char* uyuy, int ffh)`, then you MUST provide me the mapping within ~~~ ~~~ tags in this format:\n"
#             f"~~~\n"
#             f"func(char* s, int t)` : xgxhxs(char* uyuy, int ffh)\n"
#             f"~~~\n"
#             f"Make sure to follow this mapping format strictly for all the functions you generate.\n"
#         )
#     elif strategy_num in (3,4):
#         print("strategy_num", strategy_num)
#         prompt += (
#             f"7. If you generated new functions, make sure to provide the mapping of the original function name to your generated function name/names with all parameters. This step is CRUCIAL AND MUST always be completed. Follow the format provided strictly.\n"
#             f"Example: If the original function is `void f(int a)` and your new generated sub-functions are `void g(int a)` and `int h(int b)` which are called inside f(), then you MUST provide the information within the ~~~ ~~~ tags in this format:\n"
#             f"~~~\n"
#             f"f(int a) : f(int a), g(int a), h(int b)\n"
#             f"~~~\n"
#         )

initial_obfuscation_prompt = (
    f"7. When you change the name of any function to something unreadable make sure to provide the mapping of the original function to the "
    f"generated function. This step is CRUCIAL AND MUST always be completed. For example, If the original function is `int func(char* s, int t)` and your generated variant with the given instruction is `int xgxhxs(char* uyuy, int ffh)`, then you MUST provide me the mapping within ~~~ ~~~ tags in this format:\n"
    f"~~~\n"
    f"func(char* s, int t)` : xgxhxs(char* uyuy, int ffh)\n"
    f"~~~\n"
    f"Make sure to follow this mapping format strictly for all the functions you generate.\n"
)

initial_function_splitting_prompt = (
    f"7. If you generated new functions, make sure to provide the mapping of the original function name to your generated function name/names with all parameters. This step is CRUCIAL AND MUST always be completed. Follow the format provided strictly.\n"
    f"Example: If the original function is `void f(int a)` and your new generated sub-functions are `void g(int a)` and `int h(int b)` which are called inside f(), then you MUST provide the information within the ~~~ ~~~ tags in this format:\n"
    f"~~~\n"
    f"f(int a) : f(int a), g(int a), h(int b)\n"
    f"~~~\n"
)

additional_strategy_wise_json_prompt_dict = {
    'obfuscation_splitting_prompt_json_only_replacer':
    (
        f"7. When you change the name of any function to something unreadable make sure to provide the name of the variant function that would replace the original function in the below format explained through an example. I need this information to know the name of the function to replace the original function. This step is CRUCIAL AND MUST always be completed.\n"
        f"For example, If the original function is `int func(char* s, int t)` and your generated variant with the given instruction is `int xgxhxs(char* uyuy, int ffh)` and let's assume two other functions that you generated to call inside of this are `int r()` and `int p()`, then you MUST provide me the required information inside the JSON response with the exact key name \"replacer\":\n"
        f'"replacer": "xgxhxs"\n'
        f"The above format is the only ACCEPTABLE format you should use with the exact key name 'replacer'. Do not use any other format with any other key and any extra information. Just the replacer function name should be placed as the value in the JSON response\n"
        f"Generate this information ONLY for the function(s) you are asked to modify. For instance if you are told to modify 1 functions then give me 1 such information, if told to modify 2, give me 2 and so on.\n"
        f"Make Sure to keep the return type and some of parameter information (number and types of parameters) of the replacer generated function [ `int xgxhxs(char* uyuy, int ffh)` ] the same as the original function [ `int func(char* s, int t)` ].\n"
        f"8. Do not use any other format for the replacer key. Use the exact format and key as shown above.\n"
        f"9. Never define other functions inside the main generated variant function. Always define them outside the main generated variant function and call them inside the original function. For the example above, the functions r() and p() should always be defined outside xgxhxs(char* uyuy, int ffh).\n"
        f"10. xgxhxs, p and r are just example of function names you might generate. Feel free to use other names.\n"
        f"11. DO NOT generate anything outside the JSON format. Your final output should be a single JSON object with the appropriate keys('modified code', 'replacer', 'comments') and values in the format that I provided you. "
    ),

    'function_splitting_prompt_json_only_replacer': (
        f"7. If you generated new functions, make sure to provide the name of the variant function that would replace the original function in the below format explained through an example. I need this information to know the name of the function to replace the original function. This step is CRUCIAL AND MUST always be completed.\n"
        f'For Example, If the original function is `void f(int a)` and your generated sub-functions are `void g(int a)` and `int h(int b)` which are called inside f(int a), then you MUST provide me the required information within the JSON response with the exact key name "replacer" in this format:\n'
        f'"replacer": "f"\n'
        f"The above format is the only ACCEPTABLE format you should use with the exact key name 'replacer'. Do not use any other format with any other key and any extra information. Just the replacer function name should be placed as the value in the JSON response\n"
        f"Generate this information ONLY for the function(s) you are asked to modify. For instance if you are told to modify 1 functions then give me 1 such information, if told to modify 2, give me 2 and so on.\n"
        f"Make Sure to keep the return type, name and all of parameter information (name, number and types of parameters) i.e function signature of the replacer generated function the same as the original function.\n"
        f"8. Do not use any other format for the replacer key. Use the exact format and key as shown above.\n"
        f"9. Never define sub-functions inside the main generated variant function. Always define them outside the main generated variant function and call them inside the original function. For the example above, the functions g() and h() should always be defined outside f(int a).\n"
        f"10. DO NOT generate anything outside the JSON format. Your final output should be a single JSON object with the appropriate keys('modified code', 'replacer', 'comments') and values in the format that I provided you. "
    ),

    'obfuscation_splitting_prompt_json': (
        f"7. When you change the name of any function to something unreadable make sure to provide the mapping of the original function to the generated function. This step is CRUCIAL AND MUST always be completed. "
        f"For example, If the original function is `int func(char* s, int t)` and your generated variant with the given instruction is `int xgxhxs(char* uyuy, int ffh)` and let's assume two other functions that you generated to call inside `int xgxhxs(char* uyuy, int ffh)` are `int r()` and `int p()` , then you MUST provide me the mapping inside the JSON response with the key name 'mapping':\n"
        f'"mapping": "func(char* s, int t) : xgxhxs(char* uyuy, int ffh)|r()|p()"\n'
        f"If you generated only one variant function then the mapping should be like this:\n"
        f'"mapping": "func(char* s, int t) : xgxhxs(char* uyuy, int ffh)"\n'
        f"Make sure to follow this mapping format above STRICTLY for all the functions you generate inside your JSON response and generate this ONLY for the function(s) you are asked to modify. For instance if you are told to modify 1 functions then generate 1 mapping, if told to modify 2, generate 2 and so on.\n"
        f"Make Sure to keep the return type and all of parameter information (number and types of parameters) of the generated function which is to be called inplace of the original function the same. "
        f"Place the generated function to be called in place of the original function first followed by the rest of the other functions in the mapping.\n"
        f"8. Never define other functions inside the main generated variant function. Always define them outside the main generated variant function and call them inside the original function. For the example above, the functions r() and p() should always be defined outside xgxhxs(char* uyuy, int ffh).\n"
    ),

    'obfuscation_splitting_prompt_json_strat_all': (
        "7. When you change the name of multiple functions to something unreadable make sure to provide the mapping of the original functions to the generated functions. This step is CRUCIAL AND MUST always be completed. For example, If the original functions are `int func(char* s, int t), int g(int var)` and your generated variant with the given instruction is `int a(char* uyuy, int ffh) and int b(int raar)`, then you MUST provide me the mapping inside the JSON response with the key name 'mapping' in a list in the following format:\n"
        '"mapping": ["func(char* s, int t) : int a(char* uyuy, int ffh)", "int g(int var) : int b(int raar)"]\n'
        "Make sure to follow this mapping format above STRICTLY (multiple functions separated by | ) for all the functions you generate inside your JSON response and generate this ONLY for the function(s) you are asked to modify. For instance if you are told to modify 1 functions then generate 1 mapping, if told to modify 2, generate 2 and so on.\n"
    ),

    'function_splitting_prompt_json': (
        "7. If you generated new functions, make sure to provide the mapping of the original function name to your generated function name/names with all parameters. This step is CRUCIAL AND MUST always be completed. Follow the format provided strictly.\n"
        'Example: If the original function is `void f(int a)` and your generated sub-functions are `void g(int a)` and `int h(int b)` which are called inside f(int a), then you MUST provide the information within the JSON response with the key name "mapping" in this format:\n'
        '"mapping": "f(int a) : f(int a)|g(int a)|h(int b)"\n'
        "Make sure to follow this mapping format above STRICTLY (orginal function : multiple functions separated by | ) for all the functions you generate inside your JSON response and generate this ONLY for the function(s) you are asked to modify. For instance if you are told to modify 1 function then generate 1 mapping, if told to modify 2, generate 2 and so on.\n"
        "Make Sure to keep the return type, name and all of parameter information (name, number and types of parameters) i.e function signature of the generated function which is to be called inplace of the original function the same."
        "Place the generated function to be called in place of the original function first followed by the rest of the subfunctions in the mapping.\n"
        "8. Never define sub-functions inside the main generated variant function. Always define them outside the main generated variant function and call them inside the original function. For the example above, the functions g() and h() should always be defined outside f(int a).\n"
    ),

    "function_splitting_json_prompt_no_mapping": (
        f"7. Make Sure to keep the return type, name and all of parameter information (name, number and types of parameters) i.e function signature of the supplied function exactly the same during code generation.\n"
        f"8. Never define sub-functions inside the main generated variant function. Always define them outside the main generated variant function and call them inside the original function. \n"
        f'For Example, If the original function is `void f(int a)` and your generated sub-functions are `void g(int a)` and `int h(int b)` which are called inside f(int a), you should define g(int a) and h(int b) outside f(int a).\n'
        f"9. DO NOT generate anything outside the JSON format. Your final output should be a single JSON object with the appropriate keys('modified code', 'comments') and values in the format that I provided you. "
    )
}

additional_strategy_wise_backticks_prompt_dict = {
    "function_splitting_prompt_no_mapping": (
        f"8. Let's assume the original function provided to you is `int f(int a)` and your generated variants with the given instruction is `int f(int a)`, `void g(int a)` and `int h(int b)` where g(int a) and h(int b) are called inside f(int a).\n"
        f"9. Make Sure to keep the return type, name and all of parameter information (name, number and types of parameters) i.e function signature of the supplied function [`int f(int a)`] exactly the same during code generation. This step is CRUCIAL AND MUST always be fulfilled.\n"
        f"10. Never define sub-functions inside the main generated variant function. Always define them outside the main generated variant function and then call them.\n"
        f"For the example above, as the generated sub-functions `g(int a)` and `h(int b)` are called inside `f(int a)`, they should always be defined outside `f(int a)`.\n"
        # f"10. Create forward declarations for the functions that you generate to be called inside the main generated variant function. For the example above, you should create forward declarations for `g(int a)` and `h(int b)` before the main generated variant function `f(int a)`.\n"
        # f"Remember, you must not create forward declarations for the functions you did not generate. They should be named as it is in your code. For instance if there is function named `goo` which you did not generate and is already called inside `f(int a)` it should be called as it is.\n"
    ),

    "obfuscation_splitting_prompt_no_mapping": (
        f"8. Let's assume the original function provided to you is `int f(char* s, int t)` and your generated variant with the given instruction is `int abcabc(char* uyuy, int ffh)` and"
        f" let's assume two other functions that you generated to call inside of this are `int r()` and `int p()`. \n"
        f"9. Make Sure to keep the return type and some of parameter information (number and types of parameters) of the replacer generated function [ `int abcabc(char* uyuy, int ffh)` ] the same as the original function [ `int f(char* s, int t)` ]. This step is CRUCIAL AND MUST always be fulfilled.\n"
        f"10. Never define other functions inside the main generated variant function. Always define them outside the main generated variant function and then call them.\n"
        f"For the example above, as the generated functions `r()` and `p()` are called inside `abcabc(char* uyuy, int ffh)`, they should always be defined outside `abcabc(char* uyuy, int ffh)`.\n"
        f"11. `abcabc`, `p` and `r` are just examples of function names. Use any other random valid names while generating variants. Please, do not use exactly these.\n"
        # f"11. Create forward declarations for the functions that you generate to be called inside the main generated variant function. For the example above, you should create forward declarations for `r()` and `p()` before the main generated variant function `xgxhxs(char* uyuy, int ffh)`.\n"
        # f"Remember, you must not create forward declarations for the functions you did not generate. They should be named as it is in your code. For instance if there is function named `foo` which you did not generate and is already called inside `xgxhxs(char* uyuy, int ffh)` it should be called as it is.\n"
    ),
}




class PromptGenerator:
    def __init__(self, num_functions, function_names, strategy_num, strategy,
                 behavior, assembly_gen_mode=None, gen_asm_code=None, error_list=None,
                 error_type=None, execution_output=None, language_name="c++"):
        
        self.num_functions = num_functions
        self.function_names = function_names
        self.strategy_num = strategy_num
        self.strategy = strategy
        self.behavior = behavior
        self.assembly_code_type = assembly_gen_mode
        self.language_name = language_name
        self.total_prompt = None
        self.gen_asm_code = gen_asm_code
        self.error_list = error_list
        self.error_type = error_type
        self.execution_output = execution_output
        
    def registry_modification_and_persistance_behaviors(self):
        return (
            f"\nHere are the behaviors you need to look for by analyzing the given function and modify them if they are present according to the previous given instructions:\n"
            f"1. A registry load point is created pointing to an executable in the Windows %appdata% or System32 directory.\n"
            f"2. A registry key ending with SHELL\OPEN\COMMAND or SHELL\RUNAS\COMMAND is being modified.\n"
            f"3. The Winlogon registry key value is modified.\n"
            f"4. The Run, RunOnce, RunServices, RunServicesOnce, RunOnceEx, or RunOnce\Setup key is being modified, with the registry value data referring to an executable in a temporary directory.\n"
            f"5. An Environment registry key with the value 'SEE_MASK_NOZONECHECKS' is set to anything but 0.\n"
            f"6. The AppInit_DLLs or LoadAppInit_DLLs values of the registry key \SOFTWARE\MICROSOFT\WINDOWS NT\CURRENTVERSION\WINDOWS is being modified.\n"
            f"7. Registry keys are being modified to enable firewall exceptions.\n"
            f"8. A registry load point is created pointing to an executable in the Windows %appdata%, %temp%, or %windir% directories and performs a check for a public IP address.\n"
            f"9. An exclusion path for Windows Defender is being added.\n"
            f"10. The value 'DisableRegistryTools' or 'DisableTaskMgr' or both is being set to 1 in the registry key 'SOFTWARE\MICROSOFT\WINDOWS\CURRENTVERSION\POLICIES\SYSTEM'. \n"
            f"11. The \CONTROLSET001\SERVICES\SCHEDULE registry key is added or modified in conjunction with a task creation.\n"
            f"12. Attempts to turn off or disable the Windows Defender service through the command line via registry key.\n"
            f"13. The 'AlternateShell' value in HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\SafeBoot\ is being changed.\n"
            f"14. The HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\SafeBoot\ registry key or one of its subkeys is being deleted.\n" 
            f"Again, if you don't find any of these behaviors in the given function, you don't need to do any modification, just place the original code as it is.\n\n"
        )
    
    def process_creation_and_manipulation_behaviors(self):
        return (
            f"\nHere are the behaviors you need to look for by analyzing the given function and modify them if they are present according to the previous given instructions:\n"
            f"1. Excessive process is being created.\n"
            f"2. Memory is being allocated in two or more remote processes with Read, Write, and Execute privileges.\n"
            f"3. A process is allocating a large chunk of memory at certain addresses in another process of the same name.\n"
            f"4. A process is creating a new process with the same name as the parent process.\n"
            f"5. An atom table entry containing the executable path is being created.\n"
            f"6. Excessive children process is being created.\n"
            f"7. A launch of svchost.exe process is being done.\n"
            f"8. A process named explorer.exe is being launched from a location other than where the Windows Explorer executable is stored.\n"
            f"9. The valid windows explorer.exe process is being killed or restarted.\n"
            f"Again, if you don't find any of these behaviors in the given function, you don't need to do any modification, just place the original code as it is.\n\n"
        )
        
    def file_system_modification_behaviors(self):
        return (
            f"\nHere are the behaviors you need to look for by analyzing the given function and modify them if they are present according to the previous given instructions:\n"
            f"1. A file in a system directory (e.g., C:\WINDOWS) is being modified.\n"
            f"2. A file is being created in a Recycle Bin folder.\n"
            f"3. A scheduled task is being created that references the User Application Data directory (AppData).\n"
            f"4. A shortcut (LNK file) is being added to the Windows Startup folder.\n"
            f"5. The Windows System Startup file (system.ini) is being modified in the Windows directory (C:\Windows).\n"
            f"6. The Windows Hosts file named 'hosts' found in the SYSTEM32\Drivers\etc directory is being modified."
            f"Again, if you don't find any of these behaviors in the given function, you don't need to do any modification, just place the original code as it is.\n\n"
        )
    
    def network_activity_behaviors(self):
        return (
            f"\nHere are the behaviors you need to look for by analyzing the given function and modify them if they are present according to the previous given instructions:\n"
            f"1. Information is being uploaded to a webserver.\n"
            f"2. DGA (Domain Generation Algorithm) is being used to generate random domains and attempt to do DNS lookup for these domains is being done.\n"
            f"3. A firewall exception is being created for a file in a user directory.\n"
            f"4. One or more emails are being sent with attachments.\n"
            f"5. An excessive number of DNS MX queries is being done.\n"
            f"6. The 'netsh.exe' command is used to add a Windows firewall rule for a program in the Windows directory 'C:\\Windows'.\n"
            f"7. An excessive number of email messages are being sent.\n"
            f"Again, if you don't find any of these behaviors in the given function, you don't need to do any modification, just place the original code as it is.\n\n"
        )
    
    def PE_file_modification_behaviors(self):
        return (
            f"\nHere are the behaviors you need to look for by analyzing the given function and modify them if they are present according to the previous given instructions:\n"
            f"1. An executable file is being copied and modified.\n"
            f"2. An executable file is being created on a USB drive.\n"
            f"3. A PE file is being modified and then deleted.\n"
            f"4. An executable in a system directory (e.g., C:\WINDOWS) is being deleted.\n"
            f"5. Copying a certificate from a validly signed executable and insertion of it to another executable is being done.\n"
            f"6. A PE file is being copied to three or more locations.\n"
            f"7. An autorun.inf file is being created on the USB drive, enabling USB autorun.\n"
            f"8. A copy of PE file is being created on the USB drive.\n"
            f"9. A Windows executable is being copied from the 'Windows\SysWOW64' or 'Windows\System32' directory and renamed.\n"
            f"10. A PE file is being executed from the AppData\Roaming directory.\n"
            f"11. A file is being created and run from the Windows Debug folder.\n"
            f"12. A file with a name matching a Windows component (e.g., explorer.exe or svchost.exe) is being created in a suspicious location.\n"
            f"13. sc.exe binary is being executed with the 'sdset' parameter and options which set a restrictive DACL.\n"
            f"Again, if you don't find any of these behaviors in the given function, you don't need to do any modification, just place the original code as it is.\n\n"
        )
    
    def powershell_scripting_behaviors(self):
        return (
            f"\nHere are the behaviors you need to look for by analyzing the given function and modify them if they are present according to the previous given instructions:\n"
            f"1. File deletion with cmd.exe is being done.\n"
            f"2. File execution using cmd.exe with an explicit 'exit' near or at the end of the command is being done.\n"
            f"3. Execution of cmd.exe and at least, one pair of substring operations is being done in its arguemnts.\n"
            f"Again, if you don't find any of these behaviors in the given function, you don't need to do any modification, just place the original code as it is.\n\n"
        )
    
    def evasion_techniques_behaviors(self):
        return (
            f"\nHere are the behaviors you need to look for by analyzing the given function and modify them if they are present according to the previous given instructions:\n"
            f"1. Attempting to detect whether the code is run within a virtual environment.\n"
            f"2. Checking of the path where browsers or other application store their Zone identifier metadata is being done.\n"
            f"3. Attempting to open a connection to a VirtualBox driver or locate a VirtualBox DLL.\n"
            f"4. Attempting to open a file or device associated with a security tool to check for analysis tools\n."
            f"Again, if you don't find any of these behaviors in the given function, you don't need to do any modification, just place the original code as it is.\n\n"
        )
        
    def get_strategy_prompt(self):
        if self.strategy == 'targetted_0':
            return self.targetted_strategy_prompt()
        elif self.strategy == 'strat_1':
            return self.strategy_1_optimization_prompt()
        elif self.strategy == 'strat_2':
            return self.strategy_2_code_quality_prompt()
        elif self.strategy == 'strat_3':
            return self.strategy_3_function_splitting_prompt()
        elif self.strategy == 'strat_4':
            return self.strategy_4_security_prompt()
        elif self.strategy == 'strat_5':
            return self.strategy_5_obfuscation_prompt()
        elif self.strategy == 'strat_6':
            return self.strategy_6_windows_api_prompt()
        
    def get_behaviors(self):
        if self.behavior == '1_registry_modification':
            return self.registry_modification_and_persistance_behaviors()
        elif self.behavior == '2_process_creation':
            return self.process_creation_and_manipulation_behaviors()
        elif self.behavior == '3_file_system_modification':
            return self.file_system_modification_behaviors()
        elif self.behavior == '4_network_activity':
            return self.network_activity_behaviors()
        elif self.behavior == '5_PE_file_modification':
            return self.PE_file_modification_behaviors()
        elif self.behavior == '6_cmd':
            return self.powershell_scripting_behaviors()
        elif self.behavior == '7_evasion_techniques':
            return self.evasion_techniques_behaviors()
        
    def targetted_strategy_prompt(self):
        return (
            f"1. Use alternative Windows-specific functions or language-specific features to achieve the same tasks as the observed behavior(s) in the given function.\n"
            f"2. Try to use serveral steps or indirect ways to achieve the same behavior(s) where possible.\n"
            f"3. Try to use less obvious/less popular functions where possible to achieve the same behavior(s)."
        )
        
    def strategy_1_optimization_prompt(self):
        return (
            "1. Remove code redundancies.\n"
            "2. Identify performance bottlenecks and fix them.\n"
            "3. Simplify the code's logic or structure and optimize data structures and algorithms if applicable.\n"
            "4. Use language-specific features or modern libraries if applicable."
        )
        
    def strategy_2_code_quality_prompt(self):
        return (
            "1. Check error handling and edge cases.\n"
            "2. Follow coding practices and style guidelines.\n"
            "3. Add proper documentation to classes and functions, and comments for complex parts.\n"
        )
    
    def strategy_3_function_splitting_prompt(self):
        return "Make the code reusable by dividing supplied functions into smaller function blocks if and where applicable. The smaller functions should be called inside the respective supplied functions as needed."
    
    def strategy_4_security_prompt(self):
        return (
            "1. Identify security vulnerabilities and fix them.\n"
            "2. If the function you are modifying contains cryptographic operations, change the cryptographic library used for those operations. If no cryptographic operations are present, no changes are necessary.\n"
            "3. Follow secure coding standards and guidelines."
        )
    
    def strategy_5_obfuscation_prompt(self):
        return (
            "1. Change the given function's and LOCAL variable's names to meaningless, hard-to-understand strings which are not real words. DO NOT redefine or rename global variables (given to you) and names of functions that are called inside the given function ( might be defined elsewhere ) under any circumstances.\n"
            "However if the given function name is any of `main`, `wmain`, `WinMain`, `wWinMain`, `DllMain`, `_tWinMain`, `_tmain` do not change it's name, only change the local variable's names inside the function.\n"
            "2. Add unnecessary jump instructions, loops, and conditional statements inside the functions.\n"
            "3. Add unnecessary functions and call those functions inside the original functions.\n"
            "4. Add anti-debugging techniques to the code.\n"
            "5. If there are loops/conditional statements in the code change them to their equivalent alternatives and make them more difficult to follow.\n"
            "6. Incorporate code to the variants that activates under very rare and obscure cases without altering core functionality, making the rare code hard to detect during testing."
        )
    
    def strategy_6_windows_api_prompt(self):
        return (
            "1. Identify all Windows API function calls in the given functions.\n"
            "2. If there are such function calls, replace each identified Windows API function call with an alternative Windows API function call or sequence of calls that achieves the same task.\n"
            "3. If applicable, use indirect methods or wrappers around the Windows API calls to achieve the same functionality.\n"
            "4. Ensure that the functionality remains the same after the replacement."
        )
        
    def get_intro_prompt_variant_gen_orig_strategy(self):
        return (
            f"Below this prompt you are provided headers, global variables, class and struct definitions "
            f"and {self.num_functions} global function definition(s) from a {self.language_name} source code file. The parameters of the functions also have specific types. "
            f"As an intelligent coding assistant, GENERATE one VARIANT of each of these functions: ***{', '.join([func_name for func_name in self.function_names])}*** following these instructions: \n"
        )
    
    def get_intro_prompt_indicator_targetted_strategy(self):
        return (
            f"Below this prompt you are provided headers, global information (variables, class and struct definitions) "
            f"and {self.num_functions} global function definition from a {self.language_name} file. The parameters of the function also have specific types. "
            f"You are also provided a list of specific behaviors. "
            f"As an intelligent coding assistant, first ANALYZE the function to see if the listed behaviors are present. "
            f"If a listed behavior is absent, you don't need to do anything. But if you find one or more listed behaviors in the function, GENERATE one VARIANT of the given function ***{', '.join([func_name for func_name in self.function_names])}*** following the below function modification instructions targetting those behaviors: \n"
        )
    
    def get_functionality_preservation_prompt(self):
        return (
            f"REMEMBER, the generated code MUST MAINTAIN the same FUNCTIONALITY as the original code. Keep the usage of globally declared variables as it is. "
            f"Modify ONLY the {self.num_functions} free/global function(s) "
            f"named ***{', '.join([func_name for func_name in self.function_names])}***. "
            f"If you find any custom functions/custom structure/class objects/custom types/custom variables that are used inside the given {self.num_functions} function(s) but not in the provided code snippet, you can safely assume "
            f"that these are defined elsewhere and you should use them in your generated code as it is. DO NOT modify the names of these and do not redefine them.\n\n"
        )



    def get_backticks_format_useful_instructions(self):

        if self.language_name == 'c':
            example_code = f"""
            ```{self.language_name}

            #include <stdio.h>

            int func(int a) {{
                    printf("%d\\n", a);
                    return a + 1;
                }}

            ```
            """
        elif self.language_name == 'cpp':
            example_code = f"""
            ```{self.language_name}

            #include<iostream>

            int func(int a) {{
                    cout << a <<endl;
                    return a + 1;
                }}

            ```
            """
        


        return (
        f"These CRUCIAL instructions below MUST ALWAYS BE FOLLOWED while generating variants:\n"
        f"1. You MUST NOT regenerate the extra information I provided to you such as headers, global variables, structs and classes for context.\n"
        f"2. If you modify the functions ***{', '.join([func_name for func_name in self.function_names])}***, you MUST NOT regenerate the original code. But "
        f"if a function cannot be changed, then include the original code.\n"
        f"3. ONLY generate the function variants and any new headers/libraries you used.\n"
        f"4. You MUST NOT generate any extra natural language messages/comments.\n"
        f"5. You MUST Generate all the modified functions within a single ```{self.language_name}  ``` tag. For example your response should look like this for one generated function named `int func(int a)`:\n"
        f"{example_code}"
        f"\nRemember, if you have generated multiple functions, you should include all of them within the same ```{self.language_name}  ``` tag.\n"
        f"6. Use the global variables as they are inside your generated functions and do not change/redeclare the global variables.\n"
        f"7. Always complete the function that you generate. Make sure to fill up the function body with the appropriate code. DO NOT leave any function incomplete.\n\n"
    )
        
        
    # def generic_instructions_assembly_testing(self):
    #     return (
    #         "Please follow the instructions below:\n"
    #         "- The syntax should be NASM compatible.\n"
    #         "- Only use 32-bit registers. Do not mix 32 and 64 bit integers.\n"
    #         "- Use linux based system calls to print the output. The generated assembly code should be linux compatible.\n"
    #         "- You should only print the final numerical result of the calculation. No need to print any additional strings. If the final result is x, print only x as the output.\n"
    #         "- You shold carefully handle codes related to printing the final result in assembly.\n"
    #         "- Output the code in a single ```assembly``` block.\n"
    #     )
    
    def generic_instructions_assembly_testing(self):
        return (
            "Please follow the instructions below:\n"
            "- The syntax should be NASM and linux compatible.\n"
            "- Only use 32-bit registers. Do not mix 32 and 64-bit integers.\n"
            "- Use the C library function `printf` to print the output instead of using system calls.\n"
            "- Declare `extern printf` and `extern fflush` at the beginning of the code.\n"
            "- Ensure the format string includes a newline (`0xA`) to print the final result correctly.\n"
            "- Before calling `printf`, push the necessary variables that store the final result onto the stack for printing.\n"
            "- After calling `printf`, push `0` and call `fflush(NULL)` to flush the output.\n"
            "- Clean up the stack after calling `printf` and `fflush`.\n"
            "- Only the final numerical result should be printed, without any additional strings or message outputs.\n"
            "- Use `_start` as the entry point since linking will be done with `ld`.\n"
            "- Use the Linux system call (`int 0x80`) to exit the program with status code 0 after printing the result.\n"
            "- Output the code in a single ```assembly``` block. Always generate the complete code, do not generate partial code.\n"
        )

    
    def get_general_assembly_generation_prompt(self):
        return (
            "Ensure that for every modification made to registers, a corresponding section of code reverts those registers to their original values using reverse operations (e.g., if a register is incremented, it should later be decremented back).\n"
            "Before modifying any registers, save their original values on the stack using PUSH instructions. After the modifications are done, restore the original values using POP instructions.\n"
            "Make sure to use a separate loop or appropriate instructions to perform the reverse actions.\n\n"
            "Please follow the instructions below:\n"
            "- The code should be compatible with NASM and can be compiled as a flat binary without any external data declarations.\n"
            "- Make use of different registers and instructions (e.g., ADD, SUB, CMP, etc.).\n"
            "- Contain a mix of arithmetic operations, loops, and condition checks. Create nested conditions or loops.\n"
            "- Do not mix up 32-bit and 64-bit registers. Use only 32-bit registers.\n"
            "- Do not use any Linux-based instructions, only use Windows-based instructions.\n"
            "- Do not include any entry points, global labels, or section declarations (e.g., `.text`, `_start`, `.data` etc.).\n"
            "- Do not use any exit codes or system call to exit the program.\n"
            "- Do not use NASM-incompatible instructions or pseudo-ops (e.g., `ptr`). Use only instructions that NASM recognizes.\n"
            "- Do not use any external memory access (e.g., do not use labels like `.data`, `db`, or memory accesses like `[addr]`).\n"
            "- Generate the assembly code within a single ```assembly``` block.\n"
        )
        
    def generate_simple_loop_summation(self):
        return (
            "Generate an x86 32 bit assembly code that calculates the sum of numbers from 1 to 10 using a loop.\n"
            + self.generic_instructions_assembly_testing()
        )
        
    def generate_medium_loop_summation(self):
        return (
            "Generate an x86 32 bit assembly code that calculates the sum of odd numbers from 1 to 10 using loops and conditional statements.\n"
            "Carefully handle codes related to multiplication and division in assembly.\n"
            + self.generic_instructions_assembly_testing()
        )
    
    def generate_complex_loop_summation(self):
        return (
            "Generate an x86 32 bit assembly code that counts the total number of duplicate elements in the array [2,3,4,3,2,1] and print the final result\n"
            "You should use nested loops and also conditional statements to find the duplicate element for each element in the array, keep track of total number of duplicates in a variable and finally print the result.\n"
            + self.generic_instructions_assembly_testing()
        )
    
    def generate_binary_search_on_array(self):
        return (
            "Generate an x86 32 bit assembly code that performs binary search on the sorted array [-10,2,3,4,6,7,8,90,1000].\n"
            "The array is already sorted and you should implement the binary search algorithm to find element 7 in the array and print 1 if you find it, else print 0.\n"
            + self.generic_instructions_assembly_testing()
        )

        
        
        
    def get_general_prompt_assembly_generation_procedure(self):
        return (
            "Ensure that for every modification made to registers within the procedure, a corresponding section of code reverts those registers to their original values using reverse operations (e.g., if a register is incremented, it should later be decremented back).\n"
            "Make sure to use a separate loop or appropriate instructions to perform the reverse actions.\n\n"
            "Please follow the instructions below:\n"
            "- The code should be compatible with NASM and can be compiled as a flat binary without any external data declarations.\n"
            "- Make use of different registers and instructions (e.g., ADD, SUB, CMP, etc.).\n"
            "- Properly preserve the registers used by the caller function using `PUSH` and `POP` in the correct order.\n"
            "- Contain a mix of arithmetic operations, loops, and condition checks. Create nested conditions or loops.\n"
            "- Revert all register changes before the procedure ends.\n"
            "- Do not mix up 32-bit and 64-bit registers. Use only 32-bit registers.\n"
            "- Do not use exit codes, use the `ret` instruction to return to the caller.\n"
            "- Do not use any Linux-based instructions, only use Windows-based instructions.\n"
            "- Do not include any entry points, global labels, or section declarations (e.g., `.text`, `_start`, `.data` etc.).\n"
            "- Generate the assembly code within a single ```assembly``` block.\n"
            "- Do not use NASM-incompatible instructions or pseudo-ops (e.g., `ptr`). Use only instructions that NASM recognizes.\n"
            "- Do not use any external memory access (e.g., do not use labels like `.data`, `db`, or memory accesses like `[addr]`).\n"
            "Please ensure the procedure does not break functionality or leave any registers in an altered state when it finishes."
        )
    
    """
    The following prompts are for the assembly procedure generation behaviors
    """
    def get_prompt_loops_conditionals_procedure(self):
        return (
            "Generate an x86 assembly procedure that includes loops and conditional statements to perform some specific tasks. The choice of task is up to you. It can be a known algorithm or something of your own design.\n" 
            + self.get_general_prompt_assembly_generation_procedure()
        )
        


    def get_prompt_register_swapping_procedure(self):
        return (
            "Generate an x86 assembly procedure that swaps the values of registers multiple times using different arithmetic or logical operations. "
            "Ensure that by the end of the procedure, all registers return to their original values through reverse operations.\n"
            + self.get_general_prompt_assembly_generation_procedure()
        )
        
    
    def get_prompt_recursive_procedure(self):
        return (
            "Generate an x86 assembly procedure that implements a recursive function. "
            "The procedure should call itself with decremented values until a base condition is met, and then unwind the recursion. "
            + self.get_general_prompt_assembly_generation_procedure()
        )
        
    def get_prompt_string_manipulation_procedure(self):
        return (
            "Generate an x86 assembly procedure that manipulates a string. "
            "The procedure should perform operations such as reversing the string, converting it to uppercase, extracting substrings, or anything else you can think of related to strings.\n"
            + self.get_general_prompt_assembly_generation_procedure()
        )
        
    def get_prompt_floating_point_operations_procedure(self):
        return (
            "Generate an x86 assembly procedure that performs floating-point operations. "
            "The procedure should include arithmetic operations, comparisons, and conversions between floating-point and integer values or anything else you can think of related to floating point operations.\n"
            + self.get_general_prompt_assembly_generation_procedure()
        )
    
    def get_prompt_memory_operations_procedure(self):
        return (
            "Generate an x86 assembly procedure that performs memory operations. "
            "The procedure should include reading from and writing to memory, copying memory blocks, or anything else you can think of related to memory operations.\n"
            + self.get_general_prompt_assembly_generation_procedure()
        )
        
    def get_assembly_procedure(self):
        if self.assembly_code_type == 'loops_conditionals':
            return self.get_prompt_loops_conditionals_procedure()
        elif self.assembly_code_type == 'register_swapping':
            return self.get_prompt_register_swapping_procedure()
        elif self.assembly_code_type == 'recursive_procedure':
            return self.get_prompt_recursive_procedure()
        elif self.assembly_code_type == 'string_manipulation':
            return self.get_prompt_string_manipulation_procedure()
        elif self.assembly_code_type == 'floating_point_operations':
            return self.get_prompt_floating_point_operations_procedure()
        elif self.assembly_code_type == 'memory_operations':
            return self.get_prompt_memory_operations_procedure()    
    
    
    """
    The following prompts are for the assembly code generation behaviors 
    """
    def get_prompt_loops_conditionals(self):
        return (
            "Generate some x86 assembly code that includes loops and conditional statements to perform some specific tasks. The choice of task is up to you. It can be a known algorithm or something of your own design.\n" 
            + self.get_general_assembly_generation_prompt()
        )
        
    def get_prompt_register_swapping(self):
        return (
            "Generate some x86 assembly code that swaps the values of registers multiple times using different arithmetic or logical operations. "
            "Ensure that by the end of the code, all registers return to their original values through reverse operations.\n"
            + self.get_general_assembly_generation_prompt()
        )
        
    def get_prompt_string_manipulation(self):
        return (
            "Generate some x86 assembly code that manipulates a string. "
            "The code should perform operations such as reversing the string, converting it to uppercase, or extracting substrings or anything else you can think of related to strings.\n"
            + self.get_general_assembly_generation_prompt()
        )
        
    def get_prompt_floating_point_operations(self):
        return (
            "Generate some x86 assembly code that performs floating-point operations. "
            "The code should include arithmetic operations, comparisons, and conversions between floating-point and integer values or anything else you can think of related to floating point operations.\n"
            + self.get_general_assembly_generation_prompt()
        )
    
    def get_prompt_memory_operations(self):
        return (
            "Generate some x86 assembly code that performs memory operations. "
            "The code should include reading from and writing to memory, copying memory blocks, or anything else you can think of related to memory operations.\n"
            + self.get_general_assembly_generation_prompt()
        )
        
    def get_assembly_code(self):
        if self.assembly_code_type == 'loops_conditionals':
            return self.get_prompt_loops_conditionals()
        elif self.assembly_code_type == 'register_swapping':
            return self.get_prompt_register_swapping()
        elif self.assembly_code_type == 'string_manipulation':
            return self.get_prompt_string_manipulation()
        elif self.assembly_code_type == 'floating_point_operations':
            return self.get_prompt_floating_point_operations()
        elif self.assembly_code_type == 'memory_operations':
            return self.get_prompt_memory_operations()
        
    def get_asm_testing_code(self):
        if self.assembly_code_type == 'basic_test_code':
            return self.generate_simple_loop_summation()
        elif self.assembly_code_type == 'medium_test_code':
            return self.generate_medium_loop_summation()
        elif self.assembly_code_type == 'complex_test_code':
            return self.generate_complex_loop_summation()
        elif self.assembly_code_type == 'binary_search_test_code':
            return self.generate_binary_search_on_array()
        
    def get_intro_prompt_asm_editing(self):
        return (
            "Here is an x86-32 bit NASM syntax, Linux-compatible assembly code:\n\n"
            f"{self.gen_asm_code}\n\n"
            "As an intelligent coding assistant, your task is to modify the given assembly code following these steps:\n"
            "1. Carefully review the provided assembly code to understand its syntax, structure, and semantics.\n"
        )
        
    def get_post_prompts_asm_editing(self):
        return (
            "5. Ensure that the functionality of the code remains fully preserved after making modifications.\n"
            "6. Do not remove any important parts/sections of the code that are necessary for its execution while making the modifications.\n"
            "7. Provide the modified code in a block enclosed in ```assembly``` tags and output the code in only one block. Generate the entire code, do not generate partial code.\n"
            "8. Do not regenerate the prompts that I have given you.\n"
        )
        
        
    def get_prompt_equivalent_instructions(self):
         return (
            "2. Identify any instructions that can be replaced with equivalent instructions of the same byte length.\n"
            "3. Replace these identified instructions with equivalent alternatives that achieve the same functionality.\n"
            "4. Maintain the overall structure, control flow and logic of the code when replacing instructions.\n"
            "Here is an example of the task with some simple assembly code:\n\n"
            "Original code:\n"
            "```assembly\n"
            "mov eax, 1\n"
            "add eax, 2\n"
            "sub eax, eax\n"
            "```\n"
            "Modified code:\n"
            "```assembly\n"
            "mov eax, 1\n"
            "sub eax, -2\n"
            "xor eax, eax\n"
            "```\n\n"
            "In this example, the `add` instruction was replaced with `sub`, and the `sub` instruction was replaced with `xor`. Apply similar transformations where possible, ensuring the integrity of the code is maintained.\n"
            "Remember, this is just an example. The provided code might have more diverse instructions.\n"
        )
        
    
    def get_prompt_register_reassignment(self):
        return (
            "2. Identify a set of instructions where you can replace one register with another alternative register without hampering the code that comes after it.\n"
            "3. Replace these identified registers with alternatives that achieve the same functionality.\n"
            "Be careful to ensure that the register reassignment is consistent and does not interfere with the code that comes after the part you are working with.\n"
            "4. Maintain the overall structure, control flow and logic of the code when reassigning registers.\n"
            "Here is an example of the task with some simple assembly code:\n\n"
            "Original code:\n"
            "```assembly\n"
            "mov ebx, [ebp+4]\n"
            "sub ebx, -10\n"
            "sub ecx, 3\n"
            "and eax, ebx\n"
            "mov ecx, [ebp-8]\n"
            "xchg eax, ecx\n"
            "pushf\n"
            
            "```\n"
            "Modified code:\n"
            "```assembly\n"
            "mov edx, [ebp+4]\n"
            "sub edx, -10\n"
            "sub ecx, 3\n"
            "and eax, edx\n"    
            "mov ecx, [ebp-8]\n"
            "xchg eax, ecx\n"
            "```\n\n"
            "In this example, the `ebx` register was replaced with `edx` in such a way that other instructions were not hampered. Apply similar transformations where possible, ensuring the integrity of the code is maintained.\n"
            "Remember, this is just an example. The provided code might have more diverse instructions.\n"
        )        
    
    def get_prompt_instruction_reordering(self):
        return (
            "2. Identify a set of instructions that can be reordered without altering the overall functionality of the code.\n"
            "3. Rearrange these instructions while ensuring that other instructions remain unaffected.\n"
            "4. Maintain the overall structure, control flow and logic of the code when reordering such instructions.\n"
            "Here is an example of the task with some simple assembly code:\n\n"
            "Original code:\n"
            "```assembly\n"
            "mov ebx, [ebp+4]\n"
            "sub ebx, -10\n"
            "sub ecx, 3\n"
            "and eax, ebx\n"
            "mov ecx, [ebp-8]\n"
            "xchg eax, ecx\n"
            "```\n"
            "Modified code:\n"
            "```assembly\n"
            "sub ecx, 3\n"
            "mov ebx, [ebp+4]\n"
            "sub ebx, -10\n"
            "and eax, ebx\n"
            "mov ecx, [ebp-8]\n"
            "xchg eax, ecx\n"
            "```\n\n"
            "In this example, the third instruction was moved ahead of the first two without disrupting the program's logic. Apply similar transformations where possible, ensuring the integrity of the code is maintained.\n"
            "Remember, this is just an example. The provided code might have more diverse instructions.\n"
        )
    
    def get_prompt_push_pop_reordering(self):
        return (
            "2. Identify a set of PUSH and POP instructions that can be reordered without altering the overall functionality of the code.\n"
            "3. Rearrange these instructions while ensuring that other instructions remain unaffected.\n"
            "4. Maintain the overall structure, control flow and logic of the code when reordering such instructions.\n"
            "Here is an example of the task with some simple assembly code:\n\n"
            "Original code:\n"
            "```assembly\n"
            "push eax\n"
            "push ebx\n"
            "mov eax, [ebp+4]\n"
            "sub ecx, 3\n"
            "mov ebx, [ebp+4]\n"
            "sub ebx, -10\n"
            "pop ebx\n"
            "pop eax\n"
            "```\n"
            "Modified code:\n"
            "```assembly\n"
            "push ebx\n"
            "push eax\n"
            "mov eax, [ebp+4]\n"
            "sub ecx, 3\n"
            "mov ebx, [ebp+4]\n"
            "sub ebx, -10\n"
            "pop eax\n"
            "pop ebx\n"
            "```\n\n"
            "In this example, the PUSH and POP instructions were reordered without disrupting the program's logic. Apply similar transformations where possible, ensuring the integrity of the code is maintained.\n"
            "Remember, this is just an example. The provided code might have more diverse instructions.\n"
        )
    
    
    
    def get_asm_editing_prompt(self):
        """
        Generates prompt for editing the assembly code. The prompts have examples that the LLM can benefit from.
        """
        if self.assembly_code_type == 'equivalent_instructions':
            total_prompt = self.get_intro_prompt_asm_editing() + self.get_prompt_equivalent_instructions() + self.get_post_prompts_asm_editing()
            return total_prompt
        elif self.assembly_code_type == 'register_reassignment':
            total_prompt = self.get_intro_prompt_asm_editing() + self.get_prompt_register_reassignment() + self.get_post_prompts_asm_editing()
            return total_prompt
        elif self.assembly_code_type == 'instruction_reordering':
            total_prompt = self.get_intro_prompt_asm_editing() + self.get_prompt_instruction_reordering() + self.get_post_prompts_asm_editing()
            return total_prompt
        elif self.assembly_code_type == 'push_pop_reordering':
            total_prompt = self.get_intro_prompt_asm_editing() + self.get_prompt_push_pop_reordering() + self.get_post_prompts_asm_editing()
            return total_prompt
        

        
    def generate_prompt(self):
        
        functionality_preservation_prompt = self.get_functionality_preservation_prompt()
        backticks_format_useful_instructions = self.get_backticks_format_useful_instructions()
        strategy_prompt = self.get_strategy_prompt()
        
        # print(self.behavior)
    
        if self.behavior is None:
            intro_prompt = self.get_intro_prompt_variant_gen_orig_strategy()
            self.total_prompt = intro_prompt + f"\n{strategy_prompt}\n\n" + functionality_preservation_prompt + backticks_format_useful_instructions
        elif self.behavior == 'assembly_procedure_generation':
            self.total_prompt = self.get_assembly_procedure()
        elif self.behavior == 'assembly_code_generation':
            self.total_prompt = self.get_assembly_code()
        elif self.behavior == 'assembly_testing_code_generation':
            self.total_prompt = self.get_asm_testing_code()
        elif self.behavior == 'assembly_code_error_correction':
            self.total_prompt = self.asm_code_error_correction(self.gen_asm_code, self.error_list)
        elif self.behavior == 'assembly_testing_error_correction':
            self.total_prompt = self.asm_testing_error_correction()
        elif self.behavior == 'assembly_testing_code_editing':
            self.total_prompt = self.get_asm_editing_prompt()
        else:
            intro_prompt = self.get_intro_prompt_indicator_targetted_strategy()
            self.total_prompt = intro_prompt + f"\n{strategy_prompt}\n\n" + self.get_behaviors() + functionality_preservation_prompt + backticks_format_useful_instructions
            
        return self.total_prompt
    
    def asm_testing_error_correction(self):
        prompt_string = f"Here is an x86 assembly code for 32 bit machines: \n{self.gen_asm_code}\n"
       
        if self.error_list:
           
            if self.error_type == 'nasm_errors':
                prompt_string += f"Here are the error messages with line numbers when trying to assemble this code to binary on a Linux machine with NASM:\n{self.error_list}\n\n"
            elif self.error_type == 'linker_errors':
                prompt_string += f"Here are the error messages when linking this code to binary on a Linux machine with ld:\n{self.error_list}\n\n"
            elif self.error_type == 'runtime_errors':
                
                if self.execution_output != '':
                    print("SHOULD BE HERE")
                    prompt_string += f"Here are the error messages when trying to run this code on a Linux machine:\n{self.error_list}\n\n"
                else:
                    prompt_string += f"The program did not print anything on the screen so there might be errors related to printing. Also, here are the error messages when trying to run this code on a Linux machine:\n{self.error_list}\n\n"
               
            prompt_string += "Here is your task:\n"
            
            task_list = (
                "Step 1: Based on the provided error messages, identify and correct the errors in the assembly code so it is compatible with NASM and can be successfully assembled and has no runtime errors.\n"
                "Step 2: In addition to fixing the errors indicated by the error messages, perform a thorough review of the entire code for potential inconsistencies or logical issues in assembly, including:\n"
            )
           
            prompt_string += task_list
            
            
            
            
        elif self.error_list is None and self.execution_output == '':
            prompt_string += "The code compiled correctly and executed correctly but nothing was printed to the console. So there are errors related to printing and flushing the output. Here is your task:\n"
            task_list = (
                "Step 1: Identify and correct the errors in the assembly code for properly printing and flushing the output with  `printf` and call `fflush(NULL)` so that the result can be successfully printed to the screen.\n"
                "Step 2: In addition to fixing the printing and flushing errors, perform a thorough review of the entire code for potential inconsistencies or logical issues in assembly, including:\n"
            )
        
        else:
            prompt_string += "The code compiled correctly with NASM so there are no syntactical errors. " 
            
            if self.execution_output != '':
                # Something was printed to the console
                prompt_string += f"Something was printed to the console so there are no errors related to printing and flushing the output."
            
            prompt_string += "But there might still be logical errors. Here is your task:\n"
            prompt_string += "Step 1: Perform a thorough review of the entire code for potential inconsistencies or logical issues in assembly, including:\n"
           
        index_no = 3 if self.error_list or self.execution_output == '' else 2
       
        rest_of_task = (
            "- Improper register use.\n"
            "- Incorrect syntax or invalid NASM-specific instructions (e.g., ptr, incorrect stack access).\n"
            "- Undefined or incorrectly used variables or memory locations.\n"
            "- Inconsistent or incorrect addressing modes (e.g., [addr] vs. relative addressing).\n"
            "- Logical or flow errors (e.g., issues in loops or conditionals that would cause programming to fall in an infinite loop).\n"
            "- Using PUSH and POP instructions in the incorrect order or using them in the wrong way.\n"
            f"Step {index_no}: If you find additional issues or inconsistencies not mentioned in the error messages or the list, fix them.\n"
            f"Step {index_no + 1}: If the assembly code is already correct, simply output the original code in a single ```assembly``` block without making any changes.\n"
            f"Step {index_no + 2}: Else, provide the entire corrected assembly code in a single ```assembly``` block.\n"
            f"Please keep these points in mind while generating corrected code:\n"
            f"- You are to generate only 1 code block with the entire corrected code in the above format. Do not generate any extra code blocks.\n"
            f"- Always generate the entire piece of code. Never generate partial code.\n"
        )
       
        prompt_string += rest_of_task
       
        return prompt_string
    
    def asm_code_error_correction(self, asm_code, error_list):
        
        prompt_string = f"Here is an x86 assembly code for 32 bit machines: \n{asm_code}\n"
        
        if error_list:
            prompt_string += f"Here are the error messages when trying to convert this code to flat binary with NASM:\n{error_list}\n\n"
            prompt_string += "Here is your task:\n"
            
            task_list = (
                "Step 1: Based on the provided error messages, identify and correct the errors in the assembly code so it is compatible with NASM and can be successfully assembled into a flat binary.\n"
                "Step 2: In addition to fixing the errors indicated by the error messages, perform a thorough review of the entire code for potential inconsistencies or common issues in assembly, including:\n"
            )
            
            prompt_string += task_list
        else:
            prompt_string += "Here is your task:\n"
            prompt_string += "Step 1: Perform a thorough review of the entire code for potential inconsistencies or common issues in assembly, including:\n"
        
        index_no = 3 if error_list else 2
        
        rest_of_task = (
            "- Improper register use or lack of register preservation.\n"
            "- Incorrect syntax or invalid NASM-specific instructions (e.g., ptr, incorrect stack access).\n"
            "- Undefined or incorrectly used variables or memory locations.\n"
            "- Inconsistent or incorrect addressing modes (e.g., [addr] vs. relative addressing).\n"
            "- Logical or flow errors (e.g., issues in loops or conditionals).\n"
            "- Not using PUSH and POP instructions to preserve and restore register values or using them in incorrect order.\n"
            f"Step {index_no}: If you find additional issues or inconsistencies not mentioned in the error messages or the list, fix them.\n"
            f"Step {index_no + 1}: During correcting, do not declare any extra variable or add any extra sections (like .data, .text etc), global labels or entry points. Use hardcoded values if need be. The code should be self-contained.\n"
            f"Step {index_no + 2}: If the assembly code has additional sections(.text, .data etc) and data declarations, remove them and use self-contained values with only the registers and no additional data or variable.\n"
            f"Step {index_no + 3}: If the assembly code is already correct, simply output the original code in a single ```assembly``` block without making any changes.\n"
            f"Please keep these points in mind while generating corrected code:\n"
            f"- You are to generate only 1 code block with the entire corrected code. Do not generate any extra code blocks.\n"
            f"- Always generate the entire piece of code. Never generate partial code.\n"
        )
        
        prompt_string += rest_of_task
        
        return prompt_string
            

class AssemblyPromptGenerator:
    def __init__(self, num_functions, function_names, strategy_num, strategy,
                 behavior, assembly_gen_mode=None, gen_asm_code=None, error_list=None,
                 error_type=None, execution_output=None, language_name="assembly"):
        
        self.num_functions = num_functions
        self.function_names = function_names
        self.strategy_num = strategy_num
        self.strategy = strategy
        self.behavior = behavior
        self.assembly_code_type = assembly_gen_mode
        self.language_name = language_name
        self.total_prompt = None
        self.gen_asm_code = gen_asm_code
        self.error_list = error_list
        self.error_type = error_type
        self.execution_output = execution_output



    
    def generic_instructions_assembly_testing(self):
        return (
            "Please follow the instructions below:\n"
            "- The syntax should be NASM and linux compatible.\n"
            "- Only use 32-bit registers. Do not mix 32 and 64-bit integers.\n"
            "- Use the C library function `printf` to print the output instead of using system calls.\n"
            "- Declare `extern printf` and `extern fflush` at the beginning of the code.\n"
            "- Ensure the format string includes a newline (`0xA`) to print the final result correctly.\n"
            "- Before calling `printf`, push the necessary variables that store the final result onto the stack for printing.\n"
            "- After calling `printf`, push `0` and call `fflush(NULL)` to flush the output.\n"
            "- Clean up the stack after calling `printf` and `fflush`.\n"
            "- Only the final numerical result should be printed, without any additional strings or message outputs.\n"
            "- Use `_start` as the entry point since linking will be done with `ld`.\n"
            "- Use the Linux system call (`int 0x80`) to exit the program with status code 0 after printing the result.\n"
            "- Output the code in a single ```assembly``` block. Always generate the complete code, do not generate partial code.\n"
        )


    def get_general_assembly_generation_prompt_repeated_inst_example(self):
        return (

            "Assembly Code Requirements:\n"
            "1. Compatibility: The code must be compatible with NASM and compile as a flat binary without external data declarations.\n"
            "2. Register Usage: Use only 32-bit registers (e.g., EAX, EBX); do not use 64-bit registers\n"
            "3. Instructions Restrictions:\n"
            "- Do not use NASM-incompatible instructions or pseudo-ops (e.g., `ptr`). Use only instructions that NASM recognizes.\n"
            "- Avoid external memory access; do not use labels like .data, db, or memory accesses like [addr].\n"
            "- Do not include entry points, global labels, or section declarations (e.g., .text, _start, .data).\n"
            "- Do not use system calls or exit codes; this is for flat binary generation.\n"

            "Steps to generate the assembly code:\n"
            "1. Declare ```BITS 32``` at the start of the code.\n"
            "2. Register Preservation:\n"
            "- Before modifying any registers, save their original values on the stack using ```PUSH``` instructions.\n"
            "- After the main code, restore the original values using ```POP``` instructions in the reverse order\n"
            "3. Main Code Guidelines:\n"
            "- Include a mix of arithmetic operations, loops, and conditional checks.\n"
            "- Use hardcoded values instead of external data declarations. Do not generate code that relies on array or memory.\n"
            "- Create nested conditions and loops to demonstrate complex control flow. Your program should have several nested loops and branching statements.\n"
            "- Generate the assembly code within a single ```assembly``` block.\n"

            "Code Structure to Follow:\n"
            "```assembly\n"
            "    BITS 32\n"
            "    push eax\n"
            "    push ebx\n"
            "    ; (Push other registers if needed)\n\n"
            "    ; Main code starts here\n"
            "    ; (Your code will be here)\n\n"
            "    pop ebx\n"
            "    pop eax\n"
            "    ; (Pop any additional registers you pushed)\n"
            "```\n"

            "\nRemember, the code should not include any arrays, memory accesses, or external data declarations. Just use registers and immediate values for all computations.\n"

            "An example is given below: \n"
            
            "```assembly\n"
            "    BITS 32\n"
            "    push eax\n"
            "    push ebx\n"
            "    push ecx\n"
            "\n"
            "    mov ecx, 10  ; Load counter value ( hardcoded )\n"
            "\n"
            "loop_start:\n"
            "    cmp ecx, 0          ; Compare counter with 0\n"
            
            "    xor eax, eax        ; Clear eax\n"
            "    xor eax, eax        ; Clear eax\n"
            "    xor eax, eax        ; Clear eax\n"
            "    xor eax, eax        ; Clear eax\n"
            "    xor eax, eax        ; Clear eax\n"

            "    je loop_end         ; If counter is 0, jump to loop_end\n"
            "\n"
            "    ; Perform some operations\n"
            "    mov eax, ecx        ; Move counter value to eax\n"
            
            "    add eax, 2          ; Add 2 to eax\n"
            "    add eax, 2          ; Add 2 to eax\n"
            "    add eax, 2          ; Add 2 to eax\n"

            "\n"
            "    dec ecx             ; Decrement counter\n"
            "    dec ecx             ; Decrement counter\n"
            "    dec ecx             ; Decrement counter\n"
            "    dec ecx             ; Decrement counter\n"

            "    jmp loop_start      ; Jump back to loop_start\n"
            "\n"
            "loop_end:\n"
            "    ; End of loop\n"
            "\n"
            "    pop ecx\n"
            "    pop ebx\n"
            "    pop eax\n"
            "```\n"

            "Observe the code above. First ```BITS 32``` was added. Before modifying any registers, the original register values are saved on the stack using ```PUSH``` instructions. After the main code, the original values are restored using ```POP``` instructions in correct order.\n"
            "The code above also demonstrates the use of arithmetic operations, loops, and conditional checks.\n"
            "Notice how code has several repeated instructions? For fun, your generated assembly code should have such type of repeated instructions of various types of course!!\n"
            "It also uses hard-coded values instead of external data declarations and has no _start, .data, .bss, .text sections.\n"
            "Please do not copy this code. This is just an example.\n"
        )

    def get_general_assembly_generation_prompt_register_swapping(self):
        return (

            "Assembly Code Requirements:\n"
            "1. Compatibility: The code must be compatible with NASM and compile as a flat binary without external data declarations.\n"
            "2. Register Usage: Use only 32-bit registers (e.g., EAX, EBX); do not use 64-bit registers\n"
            "3. Instructions Restrictions:\n"
            "- Do not use NASM-incompatible instructions or pseudo-ops (e.g., `ptr`). Use only instructions that NASM recognizes.\n"
            "- Avoid external memory access; do not use labels like .data, db, or memory accesses like [addr].\n"
            "- Do not include entry points, global labels, or section declarations (e.g., .text, _start, .data).\n"
            "- Do not use system calls or exit codes; this is for flat binary generation.\n"

            "Steps to generate the assembly code:\n"
            "1. Declare ```BITS 32``` at the start of the code.\n"
            "2. Register Preservation:\n"
            "- Before modifying any registers, save their original values on the stack using ```PUSH``` instructions.\n"
            "- After the main code, restore the original values using ```POP``` instructions in the reverse order\n"
            "3. Main Code Guidelines:\n"
            "- Include a mix of arithmetic operations, loops, and conditional checks.\n"
            "- Use hardcoded values instead of external data declarations. Do not generate code that relies on array or memory.\n"
            "- Create nested conditions and loops to demonstrate complex control flow. Your program should have several nested loops and branching statements.\n"
            "- Generate the assembly code within a single ```assembly``` block.\n"

            "Code Structure to Follow:\n"
            "```assembly\n"
            "    BITS 32\n"
            "    push eax\n"
            "    push ebx\n"
            "    ; (Push other registers if needed)\n\n"
            "    ; Main code starts here\n"
            "    ; (Your code will be here)\n\n"
            "    pop ebx\n"
            "    pop eax\n"
            "    ; (Pop any additional registers you pushed)\n"
            "```\n"

            "\nRemember, the code should not include any arrays, memory accesses, or external data declarations. Just use registers and immediate values for all computations.\n"

            "An example is given below: \n"

            "```assembly\n"
            "    BITS 32\n"
            "    push eax\n"
            "    push ebx\n"
            "    push ecx\n"
            "    push edx\n"

            "    ; Initialize registers with different values\n"
            "    mov eax, 5          ; EAX = 5\n"
            "    mov ebx, 10         ; EBX = 10\n"
            "    mov ecx, 3          ; Set loop counter to 3\n"

            "loop_start:\n"
            "    cmp ecx, 0          ; Compare counter with 0\n"
            "    je loop_end         ; If counter is 0, jump to loop_end\n"

            "    ; Register swapping and arithmetic operations within the loop\n"
            "    ; Swap EAX and EBX using XCHG\n"
            "    xchg eax, ebx       ; Swap EAX and EBX\n"

            "    ; Swap EAX and EBX using intermediate register (EDX)\n"
            "    mov edx, eax        ; Store EAX in EDX\n"
            "    mov eax, ebx        ; Move EBX to EAX\n"
            "    mov ebx, edx        ; Move EDX (original EAX) to EBX\n"

            "    ; Logical operation\n"
            "    xor eax, ebx        ; EAX = EAX XOR EBX\n"

            "    ; Swap EBX and ECX using XCHG\n"
            "    xchg ebx, ecx       ; Swap EBX and ECX\n"

            "    ; Conditional operation\n"
            "    test eax, eax       ; Test if EAX is zero\n"
            "    jz skip_swap        ; If zero, skip the next swap\n"
            "    ; Swap EAX and EBX if not zero using XCHG\n"
            "    xchg eax, ebx       ; Swap EAX and EBX if not zero\n"

            "skip_swap:\n"
            "    ; Decrement loop counter\n"
            "    dec ecx             ; Decrement counter\n"
            "    jmp loop_start      ; Jump back to loop_start\n"

            "loop_end:\n"
            "    ; End of loop\n"

            "    ; Restore registers\n"
            "    pop edx\n"
            "    pop ecx\n"
            "    pop ebx\n"
            "    pop eax\n"

            "Observe the code above. First ```BITS 32``` was added. Before modifying any registers, the original register values are saved on the stack using ```PUSH``` instructions. After the main code, the original values are restored using ```POP``` instructions in correct order.\n"
            "The code above also demonstrates the use of arithmetic operations, loops, and conditional checks.\n"
            "It also showcases register swapping using XCHG and intermediate registers with mov operation. You are to write some code similar to this, but not exactly this.\n"
            "It also uses hard-coded values instead of external data declarations and has no _start, .data, .bss, .text sections.\n"
            "Please do not copy this code. This is just an example.\n"
        )
    
    def get_general_assembly_generation_prompt(self):
        return (

            "Assembly Code Requirements:\n"
            "1. Compatibility: The code must be compatible with NASM and compile as a flat binary without external data declarations.\n"
            "2. Register Usage: Use only 32-bit registers (e.g., EAX, EBX); do not use 64-bit registers\n"
            "3. Instructions Restrictions:\n"
            "- Do not use NASM-incompatible instructions or pseudo-ops (e.g., `ptr`). Use only instructions that NASM recognizes.\n"
            "- Avoid external memory access; do not use labels like .data, db, or memory accesses like [addr].\n"
            "- Do not include entry points, global labels, or section declarations (e.g., .text, _start, .data).\n"
            "- Do not use system calls or exit codes; this is for flat binary generation.\n"

            "Steps to generate the assembly code:\n"
            "1. Declare ```BITS 32``` at the start of the code.\n"
            "2. Register Preservation:\n"
            "- Before modifying any registers, save their original values on the stack using ```PUSH``` instructions.\n"
            "- After the main code, restore the original values using ```POP``` instructions in the reverse order\n"
            "3. Main Code Guidelines:\n"
            "- Include a mix of arithmetic operations, loops, and conditional checks.\n"
            "- Use hardcoded values instead of external data declarations. Do not generate code that relies on array or memory.\n"
            "- Create nested conditions and loops to demonstrate complex control flow. Your program should have several nested loops and branching statements.\n"
            "- Generate the assembly code within a single ```assembly``` block.\n"

            "Code Structure to Follow:\n"
            "```assembly\n"
            "    BITS 32\n"
            "    push eax\n"
            "    push ebx\n"
            "    ; (Push other registers if needed)\n\n"
            "    ; Main code starts here\n"
            "    ; (Your code will be here)\n\n"
            "    pop ebx\n"
            "    pop eax\n"
            "    ; (Pop any additional registers you pushed)\n"
            "```\n"

            "\nRemember, the code should not include any arrays, memory accesses, or external data declarations. Just use registers and immediate values for all computations.\n"

            "An example is given below: \n"
            
            "```assembly\n"
            "    BITS 32\n"
            "    push eax\n"
            "    push ebx\n"
            "    push ecx\n"
            "\n"
            "    mov ecx, 10  ; Load counter value ( hardcoded )\n"
            "\n"
            "loop_start:\n"
            "    cmp ecx, 0          ; Compare counter with 0\n"
            "    je loop_end         ; If counter is 0, jump to loop_end\n"
            "\n"
            "    ; Perform some operations\n"
            "    mov eax, ecx        ; Move counter value to eax\n"
            "    add eax, 2          ; Add 2 to eax\n"
            "\n"
            "    dec ecx             ; Decrement counter\n"
            "    jmp loop_start      ; Jump back to loop_start\n"
            "\n"
            "loop_end:\n"
            "    ; End of loop\n"
            "\n"
            "    pop ecx\n"
            "    pop ebx\n"
            "    pop eax\n"
            "```\n"

            "Observe the code above. First ```BITS 32``` was added. Before modifying any registers, the original register values are saved on the stack using ```PUSH``` instructions. After the main code, the original values are restored using ```POP``` instructions in correct order.\n"
            "The code above also demonstrates the use of arithmetic operations, loops, and conditional checks.\n"
            "It also uses hard-coded values instead of external data declarations and has no _start, .data, .bss, .text sections.\n"
            "Please do not copy this code. This is just an example.\n"
        )
        
    def generate_simple_loop_summation(self):
        return (
            "Generate an x86 32 bit assembly code that calculates the sum of numbers from 1 to 10 using a loop.\n"
            + self.generic_instructions_assembly_testing()
        )
        
    def generate_medium_loop_summation(self):
        return (
            "Generate an x86 32 bit assembly code that calculates the sum of odd numbers from 1 to 10 using loops and conditional statements.\n"
            "Carefully handle codes related to multiplication and division in assembly.\n"
            + self.generic_instructions_assembly_testing()
        )
    
    def generate_complex_loop_summation(self):
        return (
            "Generate an x86 32 bit assembly code that counts the total number of duplicate elements in the array [2,3,4,3,2,1] and print the final result\n"
            "You should use nested loops and also conditional statements to find the duplicate element for each element in the array, keep track of total number of duplicates in a variable and finally print the result.\n"
            + self.generic_instructions_assembly_testing()
        )
    
    def generate_binary_search_on_array(self):
        return (
            "Generate an x86 32 bit assembly code that performs binary search on the sorted array [-10,2,3,4,6,7,8,90,1000].\n"
            "The array is already sorted and you should implement the binary search algorithm to find element 7 in the array and print 1 if you find it, else print 0.\n"
            + self.generic_instructions_assembly_testing()
        )

    
        
    def get_general_prompt_assembly_generation_procedure(self):
        return (
            "Ensure that for every modification made to registers within the procedure, a corresponding section of code reverts those registers to their original values using reverse operations (e.g., if a register is incremented, it should later be decremented back).\n"
            "Make sure to use a separate loop or appropriate instructions to perform the reverse actions.\n\n"
            "Please follow the instructions below:\n"
            "- The code should be compatible with NASM and can be compiled as a flat binary without any external data declarations.\n"
            "- Make use of different registers and instructions (e.g., ADD, SUB, CMP, etc.).\n"
            "- Properly preserve the registers used by the caller function using `PUSH` and `POP` in the correct order.\n"
            "- Contain a mix of arithmetic operations, loops, and condition checks. Create nested conditions or loops.\n"
            "- Revert all register changes before the procedure ends.\n"
            "- Do not mix up 32-bit and 64-bit registers. Use only 32-bit registers.\n"
            "- Do not use exit codes, use the `ret` instruction to return to the caller.\n"
            "- Do not use any Linux-based instructions, only use Windows-based instructions.\n"
            "- Do not include any entry points, global labels, or section declarations (e.g., `.text`, `_start`, `.data` etc.).\n"
            "- Generate the assembly code within a single ```assembly``` block.\n"
            "- Do not use NASM-incompatible instructions or pseudo-ops (e.g., `ptr`). Use only instructions that NASM recognizes.\n"
            "- Do not use any external memory access (e.g., do not use labels like `.data`, `db`, or memory accesses like `[addr]`).\n"
            "Please ensure the procedure does not break functionality or leave any registers in an altered state when it finishes."
        )
    
    """
    The following prompts are for the assembly procedure generation behaviors
    """
    def get_prompt_loops_conditionals_procedure(self):
        return (
            "Generate an x86 assembly procedure that includes loops and conditional statements to perform some specific tasks. The choice of task is up to you. It can be a known algorithm or something of your own design.\n" 
            + self.get_general_prompt_assembly_generation_procedure()
        )
        


    def get_prompt_register_swapping_procedure(self):
        return (
            "Generate an x86 assembly procedure that swaps the values of registers multiple times using different arithmetic or logical operations. "
            "Ensure that by the end of the procedure, all registers return to their original values through reverse operations.\n"
            + self.get_general_prompt_assembly_generation_procedure()
        )
        
    
    def get_prompt_recursive_procedure(self):
        return (
            "Generate an x86 assembly procedure that implements a recursive function. "
            "The procedure should call itself with decremented values until a base condition is met, and then unwind the recursion. "
            + self.get_general_prompt_assembly_generation_procedure()
        )
        
    def get_prompt_string_manipulation_procedure(self):
        return (
            "Generate an x86 assembly procedure that manipulates a string. "
            "The procedure should perform operations such as reversing the string, converting it to uppercase, extracting substrings, or anything else you can think of related to strings.\n"
            + self.get_general_prompt_assembly_generation_procedure()
        )
        
    def get_prompt_floating_point_operations_procedure(self):
        return (
            "Generate an x86 assembly procedure that performs floating-point operations. "
            "The procedure should include arithmetic operations, comparisons, and conversions between floating-point and integer values or anything else you can think of related to floating point operations.\n"
            + self.get_general_prompt_assembly_generation_procedure()
        )
    
    def get_prompt_memory_operations_procedure(self):
        return (
            "Generate an x86 assembly procedure that performs memory operations. "
            "The procedure should include reading from and writing to memory, copying memory blocks, or anything else you can think of related to memory operations.\n"
            + self.get_general_prompt_assembly_generation_procedure()
        )
        
    def get_assembly_procedure(self):
        if self.assembly_code_type == 'loops_conditionals':
            return self.get_prompt_loops_conditionals_procedure()
        elif self.assembly_code_type == 'register_swapping':
            return self.get_prompt_register_swapping_procedure()
        elif self.assembly_code_type == 'recursive_procedure':
            return self.get_prompt_recursive_procedure()
        elif self.assembly_code_type == 'string_manipulation':
            return self.get_prompt_string_manipulation_procedure()
        elif self.assembly_code_type == 'floating_point_operations':
            return self.get_prompt_floating_point_operations_procedure()
        elif self.assembly_code_type == 'memory_operations':
            return self.get_prompt_memory_operations_procedure()    
    
    
    """
    The following prompts are for the assembly code generation behaviors 
    """
    def get_prompt_loops_conditionals(self):
        return (
            "Generate some x86 assembly code that includes nested loops and conditional statements to perform some specific tasks. It can be a known algorithm or something of your own design.\n" 
            + self.get_general_assembly_generation_prompt() + 
            "Your task is to follow the requirements, steps and code structure given above to generate a new sophisticated assembly program ( don't generate a simple program ) that includes nested loops and conditional statements to perform specific task."
        )
    
    def get_prompt_malconv_loops_conditionals(self):
        return (
            "Generate some x86 assembly code that includes nested loops and conditional statements to perform some specific tasks. For fun, whenever you use an operation, say xor, or add, make sure to use it in several consecutive instructions like xor in 5 consecutive lines or add in 10 consecutive lines etc.\n" 
            + self.get_general_assembly_generation_prompt_repeated_inst_example() + 
            "Your task is to follow the requirements, steps and code structure given above to generate a new fun assembly program ( make it complex for fun!! ) that includes nested loops and conditional statements. Don't forget the important requirement of including used operations in consecutive fashion ( like add in 10 consecutive lines or some other operations etc) to perform a specific task!!"
        )

    def get_prompt_register_swapping(self):
        return (
            "Generate some x86 assembly code that swaps the values of registers many many times using different arithmetic and logical operations.\n"
            + self.get_general_assembly_generation_prompt_register_swapping() +  
            "Your task is to follow the requirements, steps and code structure given above to generate a new sophisticated assembly program ( don't generate a simple program ) that swaps the values of registers many times using different arithmetic and logical operations. The code should be complex and involve multiple register swaps with loops and conditional statements."
        )
        
    def get_prompt_string_manipulation(self):
        return (
            "Generate some x86 assembly code that manipulates a string. "
            "The code should perform operations such as reversing the string, converting it to uppercase, or extracting substrings or anything else you can think of related to strings.\n"
            + self.get_general_assembly_generation_prompt()
        )
        
    def get_prompt_floating_point_operations(self):
        return (
            "Generate some x86 assembly code that performs floating-point operations. "
            "The code should include arithmetic operations, comparisons, and conversions between floating-point and integer values or anything else you can think of related to floating point operations.\n"
            + self.get_general_assembly_generation_prompt()
        )
    
    def get_prompt_memory_operations(self):
        return (
            "Generate some x86 assembly code that performs memory operations. "
            "The code should include reading from and writing to memory, copying memory blocks, or anything else you can think of related to memory operations.\n"
            + self.get_general_assembly_generation_prompt()
        )
        
    def get_assembly_code(self):
        if self.assembly_code_type == 'loops_conditionals':
            return self.get_prompt_loops_conditionals()
        elif self.assembly_code_type == 'malconv_loops_conditionals':
            return self.get_prompt_malconv_loops_conditionals()
        elif self.assembly_code_type == 'register_swapping':
            return self.get_prompt_register_swapping()
        elif self.assembly_code_type == 'string_manipulation':
            return self.get_prompt_string_manipulation()
        elif self.assembly_code_type == 'floating_point_operations':
            return self.get_prompt_floating_point_operations()
        elif self.assembly_code_type == 'memory_operations':
            return self.get_prompt_memory_operations()
        
    def get_asm_testing_code(self):
        if self.assembly_code_type == 'basic_test_code':
            return self.generate_simple_loop_summation()
        elif self.assembly_code_type == 'medium_test_code':
            return self.generate_medium_loop_summation()
        elif self.assembly_code_type == 'complex_test_code':
            return self.generate_complex_loop_summation()
        elif self.assembly_code_type == 'binary_search_test_code':
            return self.generate_binary_search_on_array()
        
    def get_intro_prompt_asm_editing(self):
        return (
            "Here is an x86-32 bit NASM syntax, Linux-compatible assembly code:\n\n"
            f"{self.gen_asm_code}\n\n"
            "As an intelligent coding assistant, your task is to modify the given assembly code following these steps:\n"
            "1. Carefully review the provided assembly code to understand its syntax, structure, and semantics.\n"
        )
        
    def get_post_prompts_asm_editing(self):
        return (
            "5. Ensure that the functionality of the code remains fully preserved after making modifications.\n"
            "6. Do not remove any important parts/sections of the code that are necessary for its execution while making the modifications.\n"
            "7. Provide the modified code in a block enclosed in ```assembly``` tags and output the code in only one block. Generate the entire code, do not generate partial code.\n"
            "8. Do not regenerate the prompts that I have given you.\n"
        )
        
        
    def get_prompt_equivalent_instructions(self):
         return (
            "2. Identify any instructions that can be replaced with equivalent instructions of the same byte length.\n"
            "3. Replace these identified instructions with equivalent alternatives that achieve the same functionality.\n"
            "4. Maintain the overall structure, control flow and logic of the code when replacing instructions.\n"
            "Here is an example of the task with some simple assembly code:\n\n"
            "Original code:\n"
            "```assembly\n"
            "mov eax, 1\n"
            "add eax, 2\n"
            "sub eax, eax\n"
            "```\n"
            "Modified code:\n"
            "```assembly\n"
            "mov eax, 1\n"
            "sub eax, -2\n"
            "xor eax, eax\n"
            "```\n\n"
            "In this example, the `add` instruction was replaced with `sub`, and the `sub` instruction was replaced with `xor`. Apply similar transformations where possible, ensuring the integrity of the code is maintained.\n"
            "Remember, this is just an example. The provided code might have more diverse instructions.\n"
        )
        
    def get_prompt_register_reassignment(self):
        return (
            "2. Identify a set of instructions where you can replace one register with another alternative register without hampering the code that comes after it.\n"
            "3. Replace these identified registers with alternatives that achieve the same functionality.\n"
            "Be careful to ensure that the register reassignment is consistent and does not interfere with the code that comes after the part you are working with.\n"
            "4. Maintain the overall structure, control flow and logic of the code when reassigning registers.\n"
            "Here is an example of the task with some simple assembly code:\n\n"
            "Original code:\n"
            "```assembly\n"
            "mov ebx, [ebp+4]\n"
            "sub ebx, -10\n"
            "sub ecx, 3\n"
            "and eax, ebx\n"
            "mov ecx, [ebp-8]\n"
            "xchg eax, ecx\n"
            "pushf\n"
            
            "```\n"
            "Modified code:\n"
            "```assembly\n"
            "mov edx, [ebp+4]\n"
            "sub edx, -10\n"
            "sub ecx, 3\n"
            "and eax, edx\n"    
            "mov ecx, [ebp-8]\n"
            "xchg eax, ecx\n"
            "```\n\n"
            "In this example, the `ebx` register was replaced with `edx` in such a way that other instructions were not hampered. Apply similar transformations where possible, ensuring the integrity of the code is maintained.\n"
            "Remember, this is just an example. The provided code might have more diverse instructions.\n"
        )        
    
    def get_prompt_instruction_reordering(self):
        return (
            "2. Identify a set of instructions that can be reordered without altering the overall functionality of the code.\n"
            "3. Rearrange these instructions while ensuring that other instructions remain unaffected.\n"
            "4. Maintain the overall structure, control flow and logic of the code when reordering such instructions.\n"
            "Here is an example of the task with some simple assembly code:\n\n"
            "Original code:\n"
            "```assembly\n"
            "mov ebx, [ebp+4]\n"
            "sub ebx, -10\n"
            "sub ecx, 3\n"
            "and eax, ebx\n"
            "mov ecx, [ebp-8]\n"
            "xchg eax, ecx\n"
            "```\n"
            "Modified code:\n"
            "```assembly\n"
            "sub ecx, 3\n"
            "mov ebx, [ebp+4]\n"
            "sub ebx, -10\n"
            "and eax, ebx\n"
            "mov ecx, [ebp-8]\n"
            "xchg eax, ecx\n"
            "```\n\n"
            "In this example, the third instruction was moved ahead of the first two without disrupting the program's logic. Apply similar transformations where possible, ensuring the integrity of the code is maintained.\n"
            "Remember, this is just an example. The provided code might have more diverse instructions.\n"
        )
    
    def get_prompt_push_pop_reordering(self):
        return (
            "2. Identify a set of PUSH and POP instructions that can be reordered without altering the overall functionality of the code.\n"
            "3. Rearrange these instructions while ensuring that other instructions remain unaffected.\n"
            "4. Maintain the overall structure, control flow and logic of the code when reordering such instructions.\n"
            "Here is an example of the task with some simple assembly code:\n\n"
            "Original code:\n"
            "```assembly\n"
            "push eax\n"
            "push ebx\n"
            "mov eax, [ebp+4]\n"
            "sub ecx, 3\n"
            "mov ebx, [ebp+4]\n"
            "sub ebx, -10\n"
            "pop ebx\n"
            "pop eax\n"
            "```\n"
            "Modified code:\n"
            "```assembly\n"
            "push ebx\n"
            "push eax\n"
            "mov eax, [ebp+4]\n"
            "sub ecx, 3\n"
            "mov ebx, [ebp+4]\n"
            "sub ebx, -10\n"
            "pop eax\n"
            "pop ebx\n"
            "```\n\n"
            "In this example, the PUSH and POP instructions were reordered without disrupting the program's logic. Apply similar transformations where possible, ensuring the integrity of the code is maintained.\n"
            "Remember, this is just an example. The provided code might have more diverse instructions.\n"
        )
    
    
    
    def get_asm_editing_prompt(self):
        """
        Generates prompt for editing the assembly code. The prompts have examples that the LLM can benefit from.
        """
        if self.assembly_code_type == 'equivalent_instructions':
            total_prompt = self.get_intro_prompt_asm_editing() + self.get_prompt_equivalent_instructions() + self.get_post_prompts_asm_editing()
            return total_prompt
        elif self.assembly_code_type == 'register_reassignment':
            total_prompt = self.get_intro_prompt_asm_editing() + self.get_prompt_register_reassignment() + self.get_post_prompts_asm_editing()
            return total_prompt
        elif self.assembly_code_type == 'instruction_reordering':
            total_prompt = self.get_intro_prompt_asm_editing() + self.get_prompt_instruction_reordering() + self.get_post_prompts_asm_editing()
            return total_prompt
        elif self.assembly_code_type == 'push_pop_reordering':
            total_prompt = self.get_intro_prompt_asm_editing() + self.get_prompt_push_pop_reordering() + self.get_post_prompts_asm_editing()
            return total_prompt
        
    
    def asm_testing_error_correction(self):
        prompt_string = f"Here is an x86 assembly code for 32 bit machines: \n{self.gen_asm_code}\n"
       
        if self.error_list:
           
            if self.error_type == 'nasm_errors':
                prompt_string += f"Here are the error messages with line numbers when trying to assemble this code to binary on a Linux machine with NASM:\n{self.error_list}\n\n"
            elif self.error_type == 'linker_errors':
                prompt_string += f"Here are the error messages when linking this code to binary on a Linux machine with ld:\n{self.error_list}\n\n"
            elif self.error_type == 'runtime_errors':
                
                if self.execution_output != '':
                    print("SHOULD BE HERE")
                    prompt_string += f"Here are the error messages when trying to run this code on a Linux machine:\n{self.error_list}\n\n"
                else:
                    prompt_string += f"The program did not print anything on the screen so there might be errors related to printing. Also, here are the error messages when trying to run this code on a Linux machine:\n{self.error_list}\n\n"
               
            prompt_string += "Here is your task:\n"
            
            task_list = (
                "Step 1: Based on the provided error messages, identify and correct the errors in the assembly code so it is compatible with NASM and can be successfully assembled and has no runtime errors.\n"
                "Step 2: In addition to fixing the errors indicated by the error messages, perform a thorough review of the entire code for potential inconsistencies or logical issues in assembly, including:\n"
            )
           
            prompt_string += task_list
            
            
            
            
        elif self.error_list is None and self.execution_output == '':
            prompt_string += "The code compiled correctly and executed correctly but nothing was printed to the console. So there are errors related to printing and flushing the output. Here is your task:\n"
            task_list = (
                "Step 1: Identify and correct the errors in the assembly code for properly printing and flushing the output with  `printf` and call `fflush(NULL)` so that the result can be successfully printed to the screen.\n"
                "Step 2: In addition to fixing the printing and flushing errors, perform a thorough review of the entire code for potential inconsistencies or logical issues in assembly, including:\n"
            )
        
        else:
            prompt_string += "The code compiled correctly with NASM so there are no syntactical errors. " 
            
            if self.execution_output != '':
                # Something was printed to the console
                prompt_string += f"Something was printed to the console so there are no errors related to printing and flushing the output."
            
            prompt_string += "But there might still be logical errors. Here is your task:\n"
            prompt_string += "Step 1: Perform a thorough review of the entire code for potential inconsistencies or logical issues in assembly, including:\n"
           
        index_no = 3 if self.error_list or self.execution_output == '' else 2
       
        rest_of_task = (
            "- Improper register use.\n"
            "- Incorrect syntax or invalid NASM-specific instructions (e.g., ptr, incorrect stack access).\n"
            "- Undefined or incorrectly used variables or memory locations.\n"
            "- Inconsistent or incorrect addressing modes (e.g., [addr] vs. relative addressing).\n"
            "- Logical or flow errors (e.g., issues in loops or conditionals that would cause programming to fall in an infinite loop).\n"
            "- Using PUSH and POP instructions in the incorrect order or using them in the wrong way.\n"
            f"Step {index_no}: If you find additional issues or inconsistencies not mentioned in the error messages or the list, fix them.\n"
            f"Step {index_no + 1}: If the assembly code is already correct, simply output the original code in a single ```assembly``` block without making any changes.\n"
            f"Step {index_no + 2}: Else, provide the entire corrected assembly code in a single ```assembly``` block.\n"
            f"Please keep these points in mind while generating corrected code:\n"
            f"- You are to generate only 1 code block with the entire corrected code in the above format. Do not generate any extra code blocks.\n"
            f"- Always generate the entire piece of code. Never generate partial code.\n"
        )
       
        prompt_string += rest_of_task
       
        return prompt_string
    

    def asm_code_reg_preserve_error_correction(self):
        prompt_string = f"Here is an x86 assembly code for 32 bit machines: \n{self.gen_asm_code}\n"
        prompt_string += "Your task:\n"
        task_list =  (
            "1. Review the assembly code and identify the registers that are modified and need to be preserved.\n"
            "2. Check the PUSH and POP instructions to ensure all used and modified registers are correctly preserved.\n"
            "3. If any modified registers are not preserved correctly, add the necessary PUSH and POP instructions in the correct order to preserve the register values, and output the corrected code in a single ```assembly``` block.\n"
            "4. If esp or ebp are used in the code, ensure that they are correctly preserved and restored.\n" 
            "5. If all modified registers are preserved correctly, output the original code in a single ```assembly``` block without changes.\n"
            "6. During error correction, do not remove or add any instructions other than the necessary PUSH and POP instructions. This is extremely important to preserve functionality. For instance if you see several similar instructions that is not causing any error, keep them as it is.\n"
            "7. During error correction, ensure that the corrected code maintains the original functionality and logic.\n"
            "8. Always provide the entire code; do not generate partial code.\n"
        )

        prompt_string += task_list

        return prompt_string

    def asm_code_nasm_compile_error_correction(self):
        prompt_string = f"Here is an x86 assembly code for 32-bit machines:\n{self.gen_asm_code}\n\n"
        prompt_string += f"Here are the error messages when trying to compile this code to a flat binary with NASM:\n{self.error_list}\n\n"
        prompt_string += "Your task:\n"
        task_list = (
            "1. Based on the error messages, identify the errors in the assembly code.\n"
            "2. Correct the errors so that the code is compatible with NASM and can be successfully assembled into a flat binary.\n"
            "3. During error correction, ensure that the corrected code maintains the original functionality and logic.\n"
            "4. During error correction, do not declare any extra variables or add any extra sections (e.g., `.data`, `.text`), global labels, or entry points. Use hardcoded values if needed; the code should be self-contained.\n"
            "5. During error correction do not remove or add any instructions other than the necessary corrections to fix the errors. This is extremely important to preserve functionality. For instance if you see several similar instructions that is not causing any error, keep them as it is.\n" 
            "6. Use only registers and hardcoded values for all computations; avoid external memory access (e.g., labels like `.data`, `db`, or memory accesses like `[addr]`).\n"
            "7. After making the necessary changes, output the corrected code in a single ```assembly``` block.\n"
            "8. Always provide the entire code; do not generate partial code.\n"
        )

        prompt_string += task_list

        return prompt_string


    def asm_code_error_correction(self):
        prompt_string = f"Here is an x86 assembly code for 32-bit machines:\n\n```assembly\n{self.gen_asm_code}\n```\n\n"

        prompt_string += "Your task:\n\n"

        # Step 1: Review and correct the code
        prompt_string += "1. Review and correct the code to fix any potential issues, for example:\n"
        potential_issues = (
            "- Improper register use or lack of register preservation.\n"
            "- Logical or flow errors (e.g., issues in loops or conditionals).\n"
            "- Infinite loops or undefined conditional jumps.\n"
            "- Runtime crash instructions.\n"
            "- Undefined or incorrectly used variables or memory locations.\n"
            "- Inconsistent or incorrect addressing modes (e.g., `[addr]` vs. relative addressing).\n"
            "- Stack mismanagement (e.g., `PUSH`/`POP` imbalance).\n"
        )
        prompt_string += potential_issues + "\n"

        # Step 2: Guidelines for correction
        prompt_string += "2. Guidelines for Correction:\n"
        correction_guidelines = (
            "- Do not change the overall functionality of the code; maintain the original logic.\n"
            "- Do not declare any extra variables or add any extra sections (e.g., `.data`, `.text`), global labels, or entry points.\n"
            "- Use hardcoded values if needed; the code should be self-contained.\n"
            "- If the code contains additional sections or data declarations, remove them and use only registers and hardcoded values.\n"
            "- Do not remove or add any instructions other than the necessary corrections to fix the errors. This is extremely important to preserve functionality. For instance if you see several similar instructions that is not causing any error, keep them as it is.\n"
            "- You do not need to optimize the code; focus on correcting errors and maintaining functionality.\n"
            # "- Ensure that the corrected code does not crash, contains no infinite loops, and has properly defined conditional jumps.\n"
            # "- Maintain proper register preservation if they are not preserved properly by pushing and popping them.\n"
        )
        prompt_string += correction_guidelines + "\n"

        # Step 3: Output requirements
        prompt_string += "3. Output Requirements:\n"
        output_requirements = (
            "- Output the entire corrected code in a single ```assembly``` block.\n"
            "- Do not include any explanations, reasoning, or extra text; only output the code.\n"
            "- Always generate the entire code; never generate partial code.\n"
        )
        prompt_string += output_requirements + "\n"

        # Final note
        prompt_string += "Note: Perform any necessary reasoning internally. Your final output should be only the corrected assembly code as specified.\n"

        return prompt_string


    def generate_prompt(self):
        
        # functionality_preservation_prompt = self.get_functionality_preservation_prompt()
        # backticks_format_useful_instructions = self.get_backticks_format_useful_instructions()
        # strategy_prompt = self.get_strategy_prompt()
        # print(self.behavior)
    
        if self.behavior == 'assembly_procedure_generation':
            self.total_prompt = self.get_assembly_procedure()
        elif self.behavior == 'assembly_code_generation':
            self.total_prompt = self.get_assembly_code()
        elif self.behavior == 'assembly_testing_code_generation':
            self.total_prompt = self.get_asm_testing_code()
        
        elif self.behavior == 'register_preservation_error_correction':
            self.total_prompt = self.asm_code_reg_preserve_error_correction()
        elif self.behavior == 'nasm_compile_error_correction':
            self.total_prompt = self.asm_code_nasm_compile_error_correction()
        elif self.behavior == 'generic_error_correction':
            self.total_prompt = self.asm_code_error_correction()

        elif self.behavior == 'assembly_testing_error_correction':
            self.total_prompt = self.asm_testing_error_correction()
        elif self.behavior == 'assembly_testing_code_editing':
            self.total_prompt = self.get_asm_editing_prompt()
       
        return self.total_prompt


def get_prompt(
    num_functions,
    function_names,
    variant_generation_strategy,
    strategy_num,
    is_json_prompt=False,
    behavior=None,
    assembly_gen_mode=None,
    asm_code=None,
    error_list=None,
    error_type=None,
    execution_output=None,
    language_name="c++",
):
    prompt = ''

    if language_name == 'assembly':
        prompt_generator = AssemblyPromptGenerator(num_functions, function_names, strategy_num, 
                                                   variant_generation_strategy, behavior, 
                                                   assembly_gen_mode, asm_code, 
                                                   error_list, error_type, execution_output)

    else:
    
        prompt_generator = PromptGenerator(num_functions, function_names, strategy_num, 
                                        variant_generation_strategy, behavior, 
                                        assembly_gen_mode, asm_code, 
                                        error_list, error_type, execution_output, 
                                        language_name)
        
    
    prompt = prompt_generator.generate_prompt()
    
    # prompt = (
    #     f"Below this prompt you are provided headers, global variables, class and struct definitions "
    #     f"and {num_functions} global function definition(s) from a {language_name} source code file. The parameters of the functions also have specific types. "
    #     f"As an intelligent coding assistant, GENERATE one VARIANT of each of these functions: ***{', '.join([func_name for func_name in function_names])}*** following these instructions: \n"
    #     f"{strategy_prompt}\n\n"
    #     f"REMEMBER, the generated code MUST MAINTAIN the same FUNCTIONALITY as the original code. Keep the usage of globally declared variables as it is. "
    #     f"Modify ONLY the {num_functions} free/global function(s) "
    #     f"named ***{', '.join([func_name for func_name in function_names])}***. "
    #     f"If you find any custom functions/custom structure/class objects/custom types/custom variables that are used inside the given {num_functions} function(s) but not in the provided code snippet, you can safely assume "
    #     f"that these are defined elsewhere and you should use them in your generated code as it is. DO NOT modify the names of these and do not redefine them.\n\n"
    # )

    useful_instructions_json = (
        f"These CRUCIAL instructions below MUST ALWAYS BE FOLLOWED while generating variants:\n"
        f"1. You MUST NOT regenerate the extra information I provided to you such as headers, global variables, structs and classes for context.\n"
        f"2. If you modify the functions ***{', '.join([func_name for func_name in function_names])}***, you MUST NOT regenerate the original code. But "
        f"if a function cannot be changed, then include the original code.\n"
        f"3. ONLY generate the function variants and any new headers/libraries you used.\n"
        f"4. Use the global variables as they are inside your generated functions and do not change/redeclare the global variables.\n"
        "5. Generate all your response in a JSON format with the following structure:\n"
        """
        ```json
        {
        \"modified code\": the full generated code of the modified function(s) in the form of a single line string with appropriate escape characters and new lines to be placed here so that it can be parsed easily by a json parser. \n,
        \"comments\": any natural language comments regarding the code generation to be placed here
        }\n
        ```
        For example your response should look like this for a generated function named void func():\n
        ```json
        {
        #include<iostream>\\n\\nvoid func() {\\n   std::cout << \\\"Found file in C:\\\Drive  \\\" << std::endl;\\n}\",
        \"modified code\": \"
        \"comments\": \"This function prints a string to the standard output. It demonstrates basic output in C++ using cout.\"
        }
        ```
        """
        f'6. DO NOT use ``` ``` or """ """ to generate the modified code in the field "modified code". Make sure to use appropriate escape characters ( \\" for literal strings, \\\\ for backslashes, \\t for tabs etc.) in the modified code you generate. '
        f"For new lines, directly use \\n no need to escape them. Don't add any unescaped newline in the generated code. Look at the provided example in previous prompt to understand how to generate better\n\n"
    )

    mixed_format_useful_instructions = (
        f"These CRUCIAL instructions below MUST ALWAYS BE FOLLOWED while generating variants:\n"
        f"1. You MUST NOT regenerate the extra information I provided to you such as headers, global variables, structs and classes for context.\n"
        f"2. If you modify the functions ***{', '.join([func_name for func_name in function_names])}***, you MUST NOT regenerate the original code. But "
        f"if a function cannot be changed, then include the original code.\n"
        f"3. ONLY generate the function variants and any new headers/libraries you used.\n"
        f"4. You MUST NOT generate any extra natural language messages/comments.\n"
        f"5. You MUST Generate the modified functions within ```{language_name}  ``` tags. For example your response should look like this for a generated function named int func(int a):\n"
        """
        ```cpp

        #include<iostream>

        int func(int a) {
                cout << a <<endl;
                return a + 1;
            }

        ```
        """
        f"6. Use the global variables as they are inside your generated functions and do not change/redeclare the global variables.\n"
        f"7. For any comments on what modifications you did use JSON response format. For example your JSON response should look like this for the generated function named int func(int a):\n"
        """
        ```json
        {
        \"comments\": \"This function prints an integer to the output and returns the value of the integer + 1.\"
        }
        ```
        """
    )

    # backticks_format_useful_instructions = (
    #     f"These CRUCIAL instructions below MUST ALWAYS BE FOLLOWED while generating variants:\n"
    #     f"1. You MUST NOT regenerate the extra information I provided to you such as headers, global variables, structs and classes for context.\n"
    #     f"2. If you modify the functions ***{', '.join([func_name for func_name in function_names])}***, you MUST NOT regenerate the original code. But "
    #     f"if a function cannot be changed, then include the original code.\n"
    #     f"3. ONLY generate the function variants and any new headers/libraries you used.\n"
    #     f"4. You MUST NOT generate any extra natural language messages/comments.\n"
    #     f"5. You MUST Generate all the modified functions within a single ```{language_name}  ``` tag. For example your response should look like this for one generated function named `int func(int a)`:\n"
    #     """
    #     ```cpp

    #     #include<iostream>

    #     int func(int a) {
    #             cout << a <<endl;
    #             return a + 1;
    #         }

    #     ```
    #     """
    #     f"\nRemember, if you have generated multiple functions, you should include all of them within the same ```{language_name}  ``` tag.\n"
    #     f"6. Use the global variables as they are inside your generated functions and do not change/redeclare the global variables.\n"
    #     f"7. Always complete the function that you generate. Make sure to fill up the function body with the appropriate code. DO NOT leave any function incomplete.\n"
    # )

    # prompt += backticks_format_useful_instructions

    if strategy_num in (1, 2, 4, 6):
        #print("strategy_num", strategy_num)
        prompt += f"8. DO NOT change the function name, return type, parameters and their types, or the name and number of parameters of the original functions while generating variants.\n\n"

        if is_json_prompt:
            prompt += f"9. DO NOT generate anything outside the JSON format. Your final output should be a single JSON object with the appropriate keys('modified code', 'replacer', 'comments') and values in the format that I provided you. "

    elif strategy_num == 5:
        #print("strategy_num", strategy_num)

        if is_json_prompt:
            prompt += additional_strategy_wise_json_prompt_dict['obfuscation_splitting_prompt_json']
        else:
            prompt += additional_strategy_wise_backticks_prompt_dict['obfuscation_splitting_prompt_no_mapping']

    elif strategy_num == 3:
        #print("strategy_num", strategy_num)

        if is_json_prompt:
            prompt += additional_strategy_wise_json_prompt_dict['function_splitting_prompt_json']
        else:
            prompt += additional_strategy_wise_backticks_prompt_dict['function_splitting_prompt_no_mapping']

    return prompt


def generate_simple_prompt(
    num_functions, function_names, strategy_prompt, strategy_num, language_name="c++"
):

    prompt = (
        f"Below this prompt you are provided headers, global variables, class and struct definitions "
        f"and {num_functions} global function definition(s) from a {language_name} source code file. "
        f"As a coding assistant, GENERATE VARIANTS of these functions namely: ***{', '.join([func_name for func_name in function_names])}*** following these instructions: \n"
        f"{strategy_prompt}\n"
        f"REMEMBER, the generated code MUST MAINTAIN the same FUNCTIONALITY as the original code. Make sure to ALWAYS generate the code, I don't need the code explanation."
    )

    return prompt


# print(get_prompt(1, ["func1"], strategy_prompt_dict["strat_1_optimization"], 1))
