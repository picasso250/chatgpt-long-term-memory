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
            "name": "save_to_file",
            "description": "Save data to the long-term memory file",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": "The data to be saved to the long-term memory file"
                    }
                },
                "required": ["data"]
            }
        }
    },
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
    # print(f"System: {system_prompt}")

    messages_with_system = [{"role": "system", "content": system_prompt}] + messages

    # Call the OpenAI API
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages_with_system,
        tools=tools,
    )
    # print(response)

    tool_calls = response.choices[0].message.tool_calls
    if tool_calls:
        available_functions = {
            "append_to_memory": append_to_memory,
            "save_to_file": save_to_file,
        }  
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)

            # Call the function with the provided arguments
            result = function_to_call(**function_args)
            print(f"{GRAY}Function Name: {function_name}{RESET}")
            print(f"{GRAY}Arguments: {tool_call.function.arguments}{RESET}")

    # Get the model's reply
    model_reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": model_reply if model_reply else ""})

    return model_reply


while True:
    user_input = input(f"{Fore.BLUE}User:{Style.RESET_ALL} ")

    # Add a condition to break out of the loop, for example, if the user types "exit"
    if user_input.lower() == "exit":
        print(f"{Fore.YELLOW}Bot: Goodbye!{Style.RESET_ALL}")
        break
    elif user_input == "!":
        user_input = "organize `long_term_memory.txt` and save it.(收集新的信息，删除不重要的信息)"

    messages.append({"role": "user", "content": user_input})
    # Call the chat_with_memory function or any other function you want to use
    bot_reply = chat_with_memory(messages)

    # Print the bot's reply in green
    print(f"{Fore.GREEN}Bot:{Style.RESET_ALL} {bot_reply}")