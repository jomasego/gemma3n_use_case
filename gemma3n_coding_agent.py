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

        prompt = f"""Please analyze this {Path(file_pat
