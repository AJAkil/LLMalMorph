# LLMalMorph: On The Feasibility of Generating Variant Malware using Large-Language-Models

LLMalMorph is a modular framework designed to mutate malware source code to generate malware variants using large language models (LLMs). 

## Table of Contents:
- [Project Directory Structure](#project-directory-structure)
- [Hardware and Environment Requirements](#hardware-and-environment-requirements)
- [Installation Instructions](#installation-instructions)
- [Run Instructions](#run-instructions)

<a id="project-directory-structure"></a>

## 🗂️ Project Directory Structure
```bash
LLMalMorph/
├── run_scripts/ 
│   ├── generate_llm_code_config.cfg
│   ├── variant_gen_config.cfg
│   ├── run_generate_llm_code.sh
│   └── run_variant_generator.sh
│
├── samples/
│   └── experiment_samples/
│
├── src/
│   ├── llmalmorph_engine/
│
├── requirements.txt
├── README.md
```

<a id="folder-descriptions"></a>

### 📄 Folder Descriptions
- `run_scripts/` – Configuration files and shell scripts to run the framework.
- `samples/` – Contains experiment_samples/ with real malware source code used in experiments.
- `src/` – Source code for the LLMalMorph. Core logic for function mutation, parsing, merging and LLM calls with Ollama.
- r`equirements.txt` – Python dependencies.
- `README.md` – Project documentation (this file).

<a id="hardware-and-environment-requirements"></a>

## 💻 Hardware and Environment Requirements
All Experiments were conducted with a machine with machine with
- 252 GB of RAM
- AMD Ryzen Threadripper PRO 5965WX 24-Cores
- Single RTX 3090 GPU for running local LLM with Ollama.
- Ubuntu 20.04.6 LTS

⚠️ Environment Disclaimer
We recommend using a similar environment to the one described in this project for best results. Specifically:

- A local GPU with at least 24GB of VRAM is suggested for optimal performance.
- The framework can run on machines with lower RAM and CPU specifications than those referenced here, though performance may vary.
- This project is developed and tested on mentioend veresion of Ubuntu Linux. Users on Windows or macOS may need to manually configure Python dependencies and the Ollama environment to ensure compatibility.

<a id="installation-instructions"></a>

## ⚙️ Installation Instructions
- Install ```ollama``` from this link: [Ollama Official Website.](https://ollama.com/download/linux) for running the LLM Locally on GPU. 
- Create a new Python Virtual Environment with ```python -m venv path/to/venv```
- Activate the Environment with ```source path/to/venv/bin/activate```
- Run ```python -r requirements.txt``` to install all dependencies in the environment


<a id="run-instructions"></a>

## 🖥️ Run Instructions
We provide detailed instruction on how to run the framework end-to-end with a hypothetical malware example. LLMalMorph consists of two key stages:

1. **Function Mutator** – Mutates selected functions in a malware source file using LLMs.
2. **Variant Synthesizer** – Iteratively merges mutated functions into the source file, allowing for manual debugging and testing to produce compilable variants. 

### 📁 Output Directory Structure

All outputs are organized within the `output_dir` you specify in the `generate_llm_code_config.cfg` config file. The following subdirectories are especially important:

| Folder                          | Purpose |
|--------------------------------|---------|
| `llm_responses/`               | Contains the LLM-generated function edits (as `.txt` files). You update these manually after debugging. |
| `variant_source_code/sequential/` | Contains the merged source files with up to *n* functions inserted. These files are used for compiling into malware variants. |

> 💡 These folders are inside your configured `cached_dir` (see examples below).

---

## 🧪 Example Setup (Used Throughout)

For clarity, assume the following:

- You're mutating 5 functions in `file.c` of malware sample named **M**
- Strategy used: `strategy 1`
- LLM model used: `codestral`
- You have access to the **M** malware project with source-code from where you can compile to generate a malware executable.



---

## 🔧 Stage 1: Function Mutator

This stage mutates a malware source file by generating alternative function implementations using an LLM.

### 🔹 Step 1: Edit the Config File

Edit `LLMalMorph/run_scripts/generate_llm_code_config.cfg` with the following parameters:

```ini
log_dir = directory to save the logs
source_file = path/to/file.c
num_funcs = number of functions to modify
llm = name of the llm to use
output_dir = output directory to save everytyhing
trials = 1  # Keep this as-is
``` 

Example:
```ini
log_dir=../samples/example_samples/M/llm_generated_paper
source_file=../samples/example_samples/M/file.c
num_funcs=5
llm=codestral
output_dir=../samples/example_samples/M/llm_generated_paper
trials=1 
```

### 🔹 Step 2: Run the Script
```bash
bash run_generate_llm_code.sh
```

This generates:

- llm_responses/ with files like *file.c_5_trial_1_batch_1.txt, file.c_5_trial_1_batch_2.txt, ...*

- LLM logs and intermediate files

Once the script finish running, all the llm modifications are in the directory `llm_responses/`. The script automerges the first function. For the example setup, we can find the modified source code in `variant_source_code/sequential/file_5_trial_1_func_1.c` which is directly used with malware *M* to compile the new variant for this function. If it succesfully compiles we move to the next stage. Else we debug and fix the corresponding text file for this function: `llm_responses/file.c_5_trial_1_batch_1.txt`

## 🧪 Stage 2: Variant Synthesizer
This stage merges the mutated functions into the source file one by one and tests whether the malware compiles. Manual debugging is used when needed.

### 🔹 Step 1: Edit Variant Synthesizer Config
Edit ```LLMalMorph/run_scripts/variant_gen_config.cfg```:
```ini
num_functions_merge_back= 2
source_code_file_path= path/to/file.c
cached_dir=directory/to/all/cached/file
``` 

Example:
```ini
num_functions_merge_back=2 # the next function to merge
source_code_file_path=../samples/example_samples/M/file.c
cached_dir=../samples/example_samples/M/llm_generated_paper/strat_1/file/codestral/5_functions
```

### 🔹 Step 2: Run the Variant Generator
```bash
bash run_variant_generator.sh
```

This generates a merged version of file.c with the first n LLM-modified functions placed inside: ```variant_source_code/sequential/```. For the above example we would get:
```ini
variant_source_code/sequential/file_5_trial_1_func_2.c
```

This file would contain llm modified functions 1,and 2. 

## 🔁 Iterative Loop: Merge → Compile → Fix → Repeat
Each iteration for the Stage 2 works as follows:

Try compiling the merged file within the original malware project.

If it compiles ✅ → We have a malware variant for this function!! → Move to the next function.

If it fails ❌:

- Manually debug the merged function(s) in *M* malware project. 

- Locate the LLM response file, e.g.:```llm_responses/file.c_5_trial_1_batch_2.txt```
(Here, batch_2 = 2nd function)

- Paste the fixed function code into the corresponding .txt file.

Update ```num_functions_merge_back = 3``` in the ```variant_gen_config.cfg``` and repeat the process to merge the next function along with previous ones (including the ones that were debugged before). 

Continue this loop until all functions are merged. The function wise debugging and fixing the LLM response ensures the error doesnt propagate through the next steps. Here is a flow showing how the steps work:

>f() 1 → Compile With M project → ✅ → Edit variant_gen_config.cfg → Run Script → Merged f() 1 and 2 in source file → Compile With M project → ❌ → Debug M project and fix the f() 2 → Paste debugged f() 2 in corresponding response .txt file → Edit  variant_gen_config.cfg → Run Script → Merged f() 1, 2(debugged) and 3 in source file → Repeat ... 

> 💡 The amount of bugs that may originate while mutating source code is exhaustive and extremely hard to generalize to create an automated approach. We are working on simplifying the stitching process to have less manual intervention as possible.


## ⚠️ Usage Disclaimer

**LLMalMorph is provided solely for academic and offensive security research purposes.** The framework enables mutation of malware source code to generate variants of open-source malware using large language models. This repository also contains source code of open-source malwares that were collected from other Github Repositories. By using this repository fully or partially, **you acknowledge and agree** to the following terms:

1. The authors, contributors, and affiliated institutions **do not endorse**—and **are not responsible for**—any malicious, unethical, or illegal use of this software.
2. **ALL USE IS AT YOUR OWN RISK.** Use of the software is provided **“as‑is,” without warranty** of any kind, either express or implied, including but not limited to warranties of merchantability, fitness for a particular purpose, or non‑infringement.
3. **IN NO EVENT** shall the authors, contributors, or copyright holders be liable for any damages—direct, indirect, incidental, special, consequential, or punitive—arising out of the use of this software, even if they have been advised of the possibility of such damages. This includes, but is not limited to, any loss of data, income, profits, or business interruption, or any malfunction of hardware or software.
4. This project is intended for **educational and research contexts only**, such as academic study, vulnerability analysis, defensive testing, and improving security posture. **Misuse of this framework for the creation, distribution, or execution of harmful software is strictly discouraged** and may violate applicable laws.

By accessing and using this software, you confirm that you understand and accept that any misuse is **solely your responsibility**, and that the authors and affiliated parties are fully exempt from any legal liability.

## ⚠️ Malware Samples Disclaimer
This project relies on open-source malware source codes used during experiments. You can access them in a password protected archive `malware_samples_souce_codes.zip` from the directory `samples/experiment_samples`. Use the password: ***infected*** for the malware source code archive.

- ⚠️ **Extract only in an isolated VM or sandbox environment.**
- **Do NOT execute malware** on systems you care about.
- Use only **offline, isolated virtual environments** for analysis.
- These samples are provided strictly for **educational and research purposes**.

By downloading or using these samples, you acknowledge you are solely responsible for handling them safely and legally.

