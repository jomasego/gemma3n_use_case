#!/bin/bash
# Gemma 3n Setup Script

echo "🚀 Setting up Gemma 3n Environment..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Install Ollama
echo "📦 Installing Ollama..."
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    curl -fsSL https://ollama.com/install.sh | sh
elif [[ "$OSTYPE" == "darwin"* ]]; then
    brew install ollama || curl -fsSL https://ollama.com/install.sh | sh
elif [[ "$OSTYPE" == "msys" ]]; then
    echo "Please download Ollama from https://ollama.com/download/windows"
    echo "Then run this script again."
    exit 1
fi

# Start Ollama service
echo "🔧 Starting Ollama service..."
ollama serve &
sleep 5

# Pull Gemma 3n models
echo "⬇️ Downloading Gemma 3n models..."
ollama pull gemma3n:e4b
ollama pull gemma3n:e2b

# Create virtual environment
echo "🐍 Creating Python virtual environment..."
python3 -m venv gemma3n_env
source gemma3n_env/bin/activate

# Install Python dependencies
echo "📚 Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Setup complete!"
echo ""
echo "To start using Gemma 3n:"
echo "1. Activate environment: source gemma3n_env/bin/activate"
echo "2. Run multimodal chat: streamlit run gemma3n_multimodal_chat.py"
echo "3. Run voice assistant: streamlit run gemma3n_voice_assistant.py"
echo "4. Run coding agent: python gemma3n_coding_agent.py --interactive"
