#!/bin/bash

source generate_llm_code_config.cfg

# Define the base directory for logs
LOG_DIR="$log_dir"

# Ensure the log directory exists
mkdir -p "$LOG_DIR"

# Define the base command as an array
BASE_CMD=(
    "python" 
    "../src/run_pipeline.py"
    "--source_file=$source_file"
    "--num_func=$num_funcs"
    "--llm=$llm"
    "--output_dir=$output_dir"
    "--trials=$trials"
)

# Loop through strategies strat_1 to strat_6
for i in {1..6}; do
    STRATEGY="strat_$i"
    LOG_FILE="$LOG_DIR/ST_$i.log"
    
    # Run the command with the current strategy and redirect output to the log file
    "${BASE_CMD[@]}" "--strategy=$STRATEGY" > "$LOG_FILE" 2>&1
done

# Wait for all background processes to finish
wait 

echo "All strategies have been executed."