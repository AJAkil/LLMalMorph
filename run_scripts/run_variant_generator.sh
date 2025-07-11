#!/bin/bash

# Read configuration file
source variant_gen_config.cfg

# Run the Python script with the parameters from the configuration file
python ../src/variant_source_generator.py \
    --num_functions_merge_back="$num_functions_merge_back" \
    --source_code_file_path="$source_code_file_path" \
    --cached_dir="$cached_dir"