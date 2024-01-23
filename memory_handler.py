# memory_handler.py

import os

file_path = "long_term_memory.txt"

def save_to_file(data):
    # Function to save data to the long-term memory file
    with open(file_path, 'w') as file:
        file.write(data + "\n")

def read_from_file():
    # Function to read content from the long-term memory file
    with open(file_path, 'r') as file:
        content = file.read()
    return content

def append_to_memory(data):
    # Function to append data to the long-term memory file
    with open(file_path, 'a') as file:
        file.write("\n" + data + "\n")
