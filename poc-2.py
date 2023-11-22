import argparse
import json
import os
import openai
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style

# Define argument parser
parser = argparse.ArgumentParser(description='Interactively chat with OpenAI.', add_help=False)
parser.add_argument('--api_key', action='store_true', help='Prompt for your OpenAI API key.')
parser.add_argument('-m', '--model', type=str, default="gpt-4", help='The model to be used for the conversation.')
parser.add_argument('-l', '--long', action='store_true', help='Use the full set of security questions.')
parser.add_argument('--custom-help', action='store_true', help='Display the custom help message.')

# Parse arguments
args = parser.parse_args()

# Custom Help Function
def display_custom_help():
    print("Custom Help Message")
    print("Usage: poc-gpt-infosec-consultant [options]")
    print("Options:")
    print("  --api_key            Prompt for your OpenAI API key.")
    print("  -m, --model          Specify the model (default: gpt-4).")
    print("  -l, --long           Use the full set of security questions.")
    print("  --custom-help        Display this custom help message.")
    # Add more instructions as needed

# Check if custom help is requested
if args.custom_help:
    display_custom_help()
    exit()

# Load security questions
questions_file = 'security_questions-short.json' if not args.long else 'security_questions.json'
with open(questions_file, 'r') as file:
    questions = json.load(file)

# Set API key
if args.api_key:
    openai.api_key = input("Please enter your OpenAI API key: ")
else:
    openai.api_key = os.getenv("OPENAI_API_TOKEN")

if openai.api_key is None:
    print("No OpenAI API Key provided. Please provide your API key.")
    exit()

# Define a custom style for the prompt
style = Style.from_dict({
    'prompt': 'bold',
    'input': 'green',
    'you-prompt': 'bg:orange fg:white bold',
})

# Create custom keybindings
kb = KeyBindings()

# Create a prompt session
session = PromptSession()

# Add keyboard shortcuts
@kb.add('c-space')
def _(event):
    event.app.exit(result=event.app.current_buffer.text)

@kb.add('c-q')
def _(event):
    event.app.exit()

# Initialize messages
messages = []

# Main loop
for question in questions:
    print(f"Question: {question['question']}")
    user_input = session.prompt(
        [('class:you-prompt', '    You:'), ('class:input', '\n')],
        multiline=True,
        key_bindings=kb,
        style=style,
        wrap_lines=True,
        complete_while_typing=True,
        enable_history_search=True,
        prompt_continuation=lambda width, line_number, is_soft_wrap: '')

    if user_input.strip().lower() in ["exit", "q"]:
        print("Ending the conversation. Goodbye!")
        break

    messages.append({"role": "user", "content": user_input})

    try:
        response = openai.chat.completions.create(
            model=args.model,
            messages=messages,
            temperature=0.7
        )
        print(f"GPT Response: {response.choices[0].message.content}")
        messages.append({"role": "assistant", "content": response.choices[0].message.content})
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    print("\nNext question or type 'exit' to end.\n")
