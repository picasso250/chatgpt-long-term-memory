# Chat Assistant with Long-Term Memory

## Overview

This Python script implements a chat-based assistant using OpenAI's GPT-3.5 model. The assistant maintains a long-term memory file (`long_term_memory.txt`) to store and recall information. Users can interact with the assistant, and the script leverages OpenAI's API to generate responses.

## Prerequisites

- Python 3.x
- OpenAI GPT-3.5 API key (set as the `OPENAI_API_KEY` environment variable)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/your-repo.git
    cd your-repo
    ```

2. Install dependencies:

    ```bash
    pip install openai colorama
    ```

3. Set up the OpenAI API key:

    - Obtain an API key from [OpenAI](https://beta.openai.com/signup/).
    - Set the API key as an environment variable:

        ```bash
        export OPENAI_API_KEY=your-api-key
        ```

## Usage

1. Run the script:

    ```bash
    python chat_assistant.py
    ```

2. Interact with the assistant by typing messages. Type "exit" to end the conversation.

    ```bash
    User: Hello
    Bot: [Assistant's reply]
    ```

3. To update long-term memory, type "!":

    ```bash
    User: !
    Bot: Organize `long_term_memory.txt` and save it.
    ```

## Long-Term Memory

The assistant uses a long-term memory file (`long_term_memory.txt`) to store and recall information. It can save, append, and organize data in this file.

## Contributing

Feel free to contribute by opening issues or pull requests. Any contributions are welcome!

## License

This project is licensed under the [MIT License](LICENSE).
