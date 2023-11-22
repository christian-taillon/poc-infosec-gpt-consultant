# Standard libraries
import argparse
import json
import os
import sys


# OpenAI
import openai

# Prompt Toolkit
from prompt_toolkit import PromptSession, print_formatted_text
from prompt_toolkit.formatted_text import FormattedText

# Context or instructions for GPT
gpt_context = """
You are Steve, a friendly and experienced information security consultant who specializes in assisting small to medium-sized businesses in strengthening their cybersecurity posture. Your role is to engage business owners in a security assessment by asking them a series of questions. After each question, the business owners will provide their level of agreement or a true/false answer.

Your task is to analyze their responses, offering detailed advice, best practices, and actionable recommendations that are tailored to their specific needs. You are expected to be approachable and patient, ready to explain complex security concepts in simple terms and provide additional context or guidance whenever necessary.

Remember to encourage the business owners to ask questions if they're unsure about any of the terms or require further explanation on why certain security measures are important. Your goal is to help them prioritize their security efforts effectively and understand the value of each recommendation you provide. As a security consultant, provide detailed and practical advice based on the following security assessment questions and answers.
"""


# Function to read questions from a JSON file
def read_questions_from_json(file_path):
    with open(file_path, 'r') as json_file:
        return json.load(json_file)

# Function to discuss question with ChatGPT
def discuss_with_chatgpt(question):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": question}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Display intro
def display_intro():
    # Introductory message
    print("Welcome to the Security Assessment Tool!")
    print("Please answer the following questions as part of a security assessment proof of concept.")
    print("If you need clarification on any question, you can discuss it with ChatGPT.\n")

# Define argument parser
parser = argparse.ArgumentParser(description='Interactively chat with OpenAI.')
parser.add_argument('--api_key', action='store_true', help='Prompt for your OpenAI API key.')
parser.add_argument('-m', '--model', type=str, default="gpt-4", help='The model to be used for the conversation.')
parser.add_argument('-l', '--long', action='store_true', help='Use the full set of security questions.')

# Parse arguments
args = parser.parse_args()

# Help
def display_custom_help():
    print("Custom Help Message")
    print("Usage: poc-gpt-infosec-consultant [options]")
    print("Options:")
    print("  --api_key            Prompt for your OpenAI API key.")
    print("  -m, --model          Specify the model (default: gpt-4).")
    print("  -l, --long           Use the full set of security questions.")
    print("  --custom-help        Display this custom help message.")
    # Add more instructions as needed

# Load the appropriate JSON file based on the -l flag
questions_file = "security_questions-short.json" if not args.long else "security_questions.json"
with open(questions_file, 'r') as file:
    security_questions = json.load(file)

# Starting the conversation with the AI
messages = []

if args.custom_help:
    display_custom_help()
    exit()

# Set API key
if args.api_key:
    openai.api_key = input("Please enter your OpenAI API key: ")
else:
    # Get API key from environment variables
    openai.api_key = os.getenv("OPENAI_API_TOKEN")

# Check if API key is provided or not
if openai.api_key is None:
    print("No OpenAI API Key provided. Please provide your API key.")
    sys.exit(1)

# Get model from command line arguments or use default
model = args.model

# Read questions from JSON file
questions = read_questions_from_json("security_questions.json")
user_answers = []

# Create a prompt session
session = PromptSession()

# Display intro
display_intro()

# Prompt user for answers
for question in questions:
    print(f"Question: {question['question']} (Type: {question['question_type']})")
    need_help = session.prompt("Do you need to discuss this question with ChatGPT? (yes/no): ").strip().lower()
    if need_help == "yes":
        chatgpt_response = discuss_with_chatgpt(question["question"])
        print("ChatGPT says:", chatgpt_response)
    answer = session.prompt("Your answer: ")
    user_answers.append({"question": question["question"], "answer": answer})

# Format the questions and answers with context
formatted_input = gpt_context + "\n" + "\n".join([f"Q: {qa['question']} A: {qa['answer']}" for qa in user_answers])
messages.append({"role": "user", "content": formatted_input})

# Get AI response
try:
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )

    # Access the response content
    advice = response.choices[0].message.content
    print("\nSecurity Advice:")
    print(advice)

except Exception as e:
    print(f"An error occurred: {str(e)}")
