import os
import json,openai
from openai import OpenAI
from colorama import Fore, Style, init
from memory_handler import save_to_file, read_from_file, append_to_memory

# Initialize colorama
init()

# 定义颜色
GRAY = Fore.LIGHTBLACK_EX + Style.BRIGHT
RESET = Fore.RESET + Style.RESET_ALL

# Load OpenAI API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")

# Check if API key is available
if not api_key:
    raise ValueError("OpenAI API key is missing. Set the OPENAI_API_KEY environment variable.")

openai.api_key = api_key

messages = []

tools = [
    {
        "type": "function",
        "function": {
            "name": "append_to_memory",
            "description": "Append data to the long-term memory file",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": "The data to be appended to the long-term memory file"
                    }
                },
                "required": ["data"]
            }
        }
    }
]

from openai import OpenAI
client = OpenAI()

def chat_with_memory(messages):
    # Read existing long-term memory data
    memory_data = read_from_file()

    system_prompt = f"You are a helpful assistant, always respond, with a long term memory file: `long_term_memory.txt`(you can update it!):\n```\n{memory_data}\n```\n"

    system_prompt = f"""
You are a helpful assistant, always respond, with a long term memory file: `long_term_memory.txt` (you can update it!):
```
{memory_data}
```
你的能力
- 使用python代码在当前环境执行操作
"""
    
    messages_with_system = [{"role": "system", "content": system_prompt}] + messages

    # Call the OpenAI API with stream=True
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages_with_system,
        tools=tools,
        stream=True  # Set stream=True for streaming responses
    )

    print(f"{Fore.YELLOW}Bot: {Style.RESET_ALL}",end='')
    arguments=''
    function_name=''
    message=''
    for chunk in response:
        # print(chunk)
        if chunk.choices:
            generated_text = chunk.choices[0].delta.content
            if generated_text is not None:
                print(generated_text,end='')
                message+=generated_text
        if chunk.choices[0].delta.tool_calls:
            for tool_call in chunk.choices[0].delta.tool_calls:
                if tool_call.function.name:
                    function_name = tool_call.function.name
                arguments += tool_call.function.arguments

    print()

    # print(function_name,arguments)
    if function_name:
        print(f"{GRAY}{function_name}{RESET}",f"{GRAY}{arguments}{RESET}")
        available_functions = {
            "append_to_memory": append_to_memory,
        }  
        if function_name=='python':

            code = arguments

            # 使用exec执行给定的代码
            exec(code)
            
            # 获取代码的局部变量字典
            local_vars = locals()
            
            # 获取代码的最后一行
            last_line = code.strip().split('\n')[-1].strip()
            
            # 如果最后一行是变量名，则打印该变量的值
            if last_line in local_vars:
                print(f"{last_line} =", local_vars[last_line])

        else:
            function_to_call = available_functions[function_name]
            function_args = json.loads(arguments)

            # Call the function with the provided arguments
            result = function_to_call(**function_args)
            print(result)

    messages.append({"role": "assistant", "content": message})
    return messages


while True:
    user_input = input(f"{Fore.BLUE}User:{Style.RESET_ALL} ")

    # Add a condition to break out of the loop, for example, if the user types "exit"
    if user_input.lower() == "exit":
        print(f"{Fore.YELLOW}Bot: Goodbye!{Style.RESET_ALL}")
        break
    elif user_input == "!":
        user_input = "根据以上对话，向 `long_term_memory.txt` 追加信息。"

    messages.append({"role": "user", "content": user_input})
    # Call the chat_with_memory function or any other function you want to use
    messages = chat_with_memory(messages)
