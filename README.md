Certainly! I'll update the README to include instructions for using the installation scripts and the command `poc-gpt-infosec-consultant`. I'll also add information about the two different JSON files for the security questions and how to use the `-l` flag for a quick proof of concept with fewer questions.

---

# Security Assessment Chatbot - Proof of Concept

## Overview
This project is a proof of concept (POC) for a security assessment tool that leverages OpenAI's ChatGPT API. It simulates a conversation with a security consultant, offering insights and recommendations tailored to the user's specific needs. The tool interacts with users by asking a series of security-related questions and then providing advice based on their responses.

## Features
- Interactive Q&A format for security assessment.
- Integration with OpenAI's ChatGPT for generating advice and explanations.
- Ability to discuss questions with ChatGPT for additional clarification.
- Customizable context setting for ChatGPT to tailor its responses.

## Installation
To install the tool, run the provided install scripts. These scripts will set up everything needed and create links or shortcuts. After installation, you can start the tool by simply typing `poc-gpt-infosec-consultant` into your terminal.

## Usage
1. After installation, open your terminal.
2. Type `poc-gpt-infosec-consultant` to start the standard version with the full set of questions.
3. For a quick demonstration, use `poc-gpt-infosec-consultant -l` to load a longer version with more than just 3 questions.

### JSON Files for Security Questions
- `security_questions.json`: This file contains the full set of security assessment questions.
- `security_questions-short.json`: This file contains a shorter set of 3 questions for a quick proof of concept.

## Project Status
This tool is in the proof of concept stage and may require further development and testing for production use.
