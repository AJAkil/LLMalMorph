import ollama
from openai import OpenAI

# deepseek-coder:6.7b-instruct 7B
# dolphin-mistral:latest 7B
# llama3:8b-instruct-q4_0 8.0B
# codellama:13b-instruct 13B
# codegemma:7b-instruct 9B

openai_client = OpenAI(
    base_url = 'http://localhost:11434/v1',
    api_key='ollama', # required, but unused
)

def ollama_generate_api(model_name, prompt):
    print('*'*10, f'Generating code using model {model_name}', '*'*10)
    response = ollama.generate(model=model_name, prompt=prompt)
    return response['response']

def ollama_chat_api(model_name, system_prompt, user_prompt, seed=42):
    print("=>=>=> TTTTTHHHHHE SEED IS", seed)
    print('\n\n')
    print('*'*10, f'Generating with {model_name}', '*'*10)
    print('\n\n')
    response = ollama.chat(
        
        model=model_name, 
        
        messages=[
        {'role': 'system','content': system_prompt,},
        {'role': 'user', 'content': user_prompt},
        ],

        options={
        'temperature': 0.8, # default 0.8
        'top_k': 40, # default 40
        'top_p': 0.9, # default 0.9,
        'seed': seed,
        },
    )

    return response['message']['content']

def ollama_openai_chat_api(openai_client, model_name, system_prompt, user_prompt):
    print('*'*10, f'Generating with {model_name}', '*'*10)
    
    response = openai_client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.7,
        stream=False
    )
    return response.choices[0].message.content


def print_model_names():
    models = ollama.list()['models']
    print(models)
    for model in models:
        print(model['name'])

