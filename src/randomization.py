import random
import os


def generate_random_func_sequences(total_target_functions, file_name, random_seed):
    
    random.seed(random_seed)
    
    used_random_function_file = f'{file_name}_used_random_function_serial.txt'
    
    try:
        with open(used_random_function_file, 'r') as f:
            used_random_numbers = set(int(line.strip()) for line in f)
    except FileNotFoundError:
        used_random_numbers = set()
    
    print('TOTAL TARGET FUNCTIONS:', total_target_functions)
    while True:
        random_number = random.randint(1, total_target_functions)
        if random_number not in used_random_numbers:
            used_random_numbers.add(random_number)
            break
    
    with open(used_random_function_file, 'w') as f:
        for number in used_random_numbers:
            f.write(f"{number}\n")
    
    # sort the used random numbers
    used_random_numbers = sorted(used_random_numbers)
    
    random_func_indices = [number - 1 for number in used_random_numbers]
    
    return random_func_indices

def generate_random_file_sequences(malware_sample_project_path, file_extension, output_dir, malware_sample_name, seed):
    
    random.seed(seed)
    
    file_list = os.listdir(malware_sample_project_path)
    
    file_list_filtered = [file for file in file_list if file.endswith(file_extension)]
    
    total_files = len(file_list_filtered)
    
    # randomize the indices 
    
    random_file_indices = random.sample(range(total_files), total_files)
    random_file_names = [file_list_filtered[index] for index in random_file_indices]

    print(f"The random file names are: {random_file_names}")
    
    with open(f"{output_dir}/{malware_sample_name}_random_file_names.txt", 'w') as f:
        for file_name in random_file_names:
            f.write(f"{file_name}\n")
    
    