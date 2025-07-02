#!/usr/bin/env python3
"""
Gemma 3n Local Coding Agent
A smart coding assistant that runs entirely on your machine
"""

import os
import sys
import json
import subprocess
import requests
import argparse
import re
from pathlib import Path
from typing import List, Dict, Optional
import tempfile
import shutil

class Gemma3nCodingAgent:
    def __init__(self, ollama_url: str = "http://localhost:11434", model: str = "gemma3n:e4b"):
        self.ollama_url = ollama_url
        self.model = model
        self.conversation_history = []
        self.workspace = Path.cwd()

    def call_gemma3n(self, prompt: str, system_prompt: str = None) -> str:
        """Call Gemma 3n via Ollama API"""
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"

        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,  # Lower temperature for more deterministic code
                "top_p": 0.9
            }
        }

        try:
            response = requests.post(f"{self.ollama_url}/api/generate", json=payload)
            response.raise_for_status()
            return response.json().get("response", "")
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}"

    def analyze_code(self, file_path: str) -> str:
        """Analyze a code file and provide insights"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code_content = f.read()
        except Exception as e:
            return f"Error reading file: {e}"

        system_prompt = """You are a code analysis expert. Analyze the provided code and give:
1. Code quality assessment
2. Potential bugs or issues
3. Performance improvements
4. Security considerations
5. Best practices recommendations
Be specific and actionable."""

        prompt = f"""Please analyze this {Path(file_path).suffix} code:

```{Path(file_path).suffix}
{code_content}
```

File: {file_path}"""

        return self.call_gemma3n(prompt, system_prompt)

    def generate_code(self, description: str, language: str = "python") -> str:
        """Generate code based on description"""
        system_prompt = f"""You are an expert {language} programmer. Generate clean, well-documented, 
and efficient code based on the user's requirements. Include:
1. Proper error handling
2. Clear variable names
3. Comments explaining complex logic
4. Docstrings for functions/classes
5. Follow {language} best practices"""

        prompt = f"""Generate {language} code for the following requirement:

{description}

Please provide complete, runnable code with explanations."""

        return self.call_gemma3n(prompt, system_prompt)

    def debug_code(self, code: str, error_message: str = None) -> str:
        """Help debug code issues"""
        system_prompt = """You are a debugging expert. Analyze the provided code and error message.
Provide:
1. Explanation of the issue
2. Step-by-step debugging approach
3. Fixed code
4. Prevention tips for similar issues"""

        prompt = f"""Please help debug this code:

```
{code}
```"""

        if error_message:
            prompt += f"\n\nError message:\n{error_message}"

        return self.call_gemma3n(prompt, system_prompt)

    def optimize_code(self, code: str) -> str:
        """Optimize code for performance"""
        system_prompt = """You are a code optimization expert. Analyze the code and provide:
1. Performance bottlenecks
2. Optimized version of the code
3. Explanation of improvements
4. Trade-offs considered
5. Benchmarking suggestions"""

        prompt = f"""Please optimize this code for better performance:

```
{code}
```"""

        return self.call_gemma3n(prompt, system_prompt)

    def explain_code(self, code: str) -> str:
        """Explain how code works"""
        system_prompt = """You are a code educator. Explain the provided code in a clear, 
educational manner suitable for developers. Include:
1. Overall purpose and functionality
2. Step-by-step breakdown
3. Key concepts and patterns used
4. Dependencies and requirements
5. Use cases and examples"""

        prompt = f"""Please explain how this code works:

```
{code}
```"""

        return self.call_gemma3n(prompt, system_prompt)

    def suggest_tests(self, code: str) -> str:
        """Suggest unit tests for code"""
        system_prompt = """You are a test automation expert. Generate comprehensive unit tests for the provided code.
Include:
1. Test cases for normal functionality
2. Edge cases and error conditions
3. Mock objects where needed
4. Setup and teardown methods
5. Clear test documentation"""

        prompt = f"""Please generate unit tests for this code:

```
{code}
```"""

        return self.call_gemma3n(prompt, system_prompt)

    def review_pull_request(self, diff_content: str) -> str:
        """Review a pull request diff"""
        system_prompt = """You are a senior developer conducting a code review. 
Provide a thorough review including:
1. Code quality assessment
2. Potential issues or bugs
3. Security considerations
4. Performance implications
5. Suggestions for improvement
6. Positive feedback on good practices"""

        prompt = f"""Please review this pull request diff:

```diff
{diff_content}
```"""

        return self.call_gemma3n(prompt, system_prompt)

    def create_project_structure(self, project_name: str, project_type: str) -> str:
        """Create a project structure"""
        system_prompt = f"""You are a project architecture expert. Create a well-structured 
{project_type} project layout with:
1. Appropriate directory structure
2. Configuration files
3. Documentation templates
4. Basic code files
5. Development setup instructions"""

        prompt = f"""Create a complete project structure for a {project_type} project named '{project_name}'.
Provide the directory tree and essential files with their basic content."""

        return self.call_gemma3n(prompt, system_prompt)

    def interactive_chat(self):
        """Start an interactive coding chat session"""
        print("🤖 Gemma 3n Coding Agent - Interactive Mode")
        print("Type 'help' for commands, 'exit' to quit\n")

        while True:
            try:
                user_input = input("You: ").strip()

                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print("Goodbye! Happy coding! 👋")
                    break

                if user_input.lower() == 'help':
                    self.show_help()
                    continue

                if user_input.startswith('/'):
                    self.handle_command(user_input)
                    continue

                # Regular coding question
                system_prompt = """You are a helpful coding assistant. Provide clear, 
                practical answers to programming questions. Include code examples when relevant."""

                response = self.call_gemma3n(user_input, system_prompt)
                print(f"\n🤖 Assistant: {response}\n")

            except KeyboardInterrupt:
                print("\n\nGoodbye! 👋")
                break
            except Exception as e:
                print(f"Error: {e}")

    def handle_command(self, command: str):
        """Handle special commands"""
        parts = command.split()
        cmd = parts[0][1:]  # Remove the '/'

        if cmd == 'analyze' and len(parts) > 1:
            file_path = parts[1]
            if os.path.exists(file_path):
                result = self.analyze_code(file_path)
                print(f"\n📊 Analysis for {file_path}:\n{result}\n")
            else:
                print(f"File not found: {file_path}")

        elif cmd == 'workspace':
            print(f"Current workspace: {self.workspace}")
            print("Files:")
            for item in self.workspace.iterdir():
                print(f"  {'📁' if item.is_dir() else '📄'} {item.name}")

        else:
            print("Unknown command. Type 'help' for available commands.")

    def show_help(self):
        """Show available commands"""
        help_text = """
🤖 Gemma 3n Coding Agent Commands:

General Commands:
  help                    - Show this help message
  exit/quit/bye          - Exit the program

File Commands:
  /analyze <file>        - Analyze a code file
  /workspace            - Show current workspace

Direct Questions:
  - Ask any coding question
  - Request code generation
  - Get debugging help
  - Ask for explanations

Examples:
  "Generate a Python function to sort a list"
  "Explain how recursion works"
  "Debug this error: IndexError"
  "/analyze main.py"
        """
        print(help_text)

def main():
    parser = argparse.ArgumentParser(description="Gemma 3n Local Coding Agent")
    parser.add_argument("--ollama-url", default="http://localhost:11434", 
                       help="Ollama server URL")
    parser.add_argument("--model", default="gemma3n:e4b", 
                       help="Gemma 3n model to use")
    parser.add_argument("--analyze", type=str, 
                       help="Analyze a specific file")
    parser.add_argument("--generate", type=str, 
                       help="Generate code based on description")
    parser.add_argument("--language", default="python", 
                       help="Programming language for code generation")
    parser.add_argument("--interactive", action="store_true", 
                       help="Start interactive chat mode")

    args = parser.parse_args()

    # Initialize the coding agent
    agent = Gemma3nCodingAgent(args.ollama_url, args.model)

    # Check if Ollama is accessible
    try:
        response = requests.get(f"{args.ollama_url}/api/tags")
        response.raise_for_status()
    except requests.exceptions.RequestException:
        print(f"❌ Error: Cannot connect to Ollama at {args.ollama_url}")
        print("Please make sure Ollama is running and Gemma 3n is installed.")
        sys.exit(1)

    print("✅ Connected to Ollama successfully!")

    if args.analyze:
        if os.path.exists(args.analyze):
            print(f"🔍 Analyzing {args.analyze}...")
            result = agent.analyze_code(args.analyze)
            print(f"\nAnalysis Result:\n{result}")
        else:
            print(f"❌ File not found: {args.analyze}")

    elif args.generate:
        print(f"🛠️ Generating {args.language} code...")
        result = agent.generate_code(args.generate, args.language)
        print(f"\nGenerated Code:\n{result}")

    elif args.interactive:
        agent.interactive_chat()

    else:
        print("🤖 Gemma 3n Coding Agent")
        print("Use --help to see available options")
        print("Use --interactive to start chat mode")

if __name__ == "__main__":
    main()
