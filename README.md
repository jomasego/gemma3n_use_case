# 🤖 What You Can Build with Gemma 3n Now

This repository contains practical applications and examples demonstrating the capabilities of Google's Gemma 3n, the latest multimodal AI model optimized for on-device inference.

## 📁 Created Applications

### gemma3n_multimodal_chat.py
**Type**: Streamlit Web App  
**Description**: Multimodal chat application supporting text, image, and audio inputs  
**Features**: Multiple API providers, Real-time chat, File uploads, Conversation history  
**Complexity**: Intermediate

### gemma3n_voice_assistant.py
**Type**: Streamlit Voice App  
**Description**: Voice-activated AI assistant with speech recognition and text-to-speech  
**Features**: Voice input/output, Multiple languages, Conversation context, Manual text fallback  
**Complexity**: Advanced

### gemma3n_coding_agent.py
**Type**: Command Line Tool  
**Description**: Local coding assistant for code analysis, generation, and debugging  
**Features**: Interactive chat, Code analysis, Project generation, Debug assistance  
**Complexity**: Advanced

### gemma3n_document_analyzer.py
**Type**: Streamlit Web App  
**Description**: Document analysis tool for PDFs and images with AI-powered insights  
**Features**: PDF processing, Multiple analysis types, Data export, Batch processing  
**Complexity**: Advanced

### requirements.txt
**Type**: Configuration  
**Description**: Python package dependencies for all applications  
**Features**: Complete dependency list, Version specifications, Optional packages  
**Complexity**: Basic

### setup.sh
**Type**: Installation Script  
**Description**: Automated setup script for Ollama and Python environment  
**Features**: Cross-platform support, Ollama installation, Virtual environment setup  
**Complexity**: Intermediate

### docker-compose.yml
**Type**: Docker Configuration  
**Description**: Docker Compose configuration for containerized deployment  
**Features**: Ollama service, App containerization, Network configuration  
**Complexity**: Intermediate

### Dockerfile
**Type**: Docker Configuration  
**Description**: Docker container definition for the applications  
**Features**: Python environment, System dependencies, Non-root user  
**Complexity**: Intermediate


## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Ollama installed and running
- Gemma 3n model downloaded

### Installation

1. **Automated Setup** (Recommended):
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

2. **Manual Setup**:
   ```bash
   # Install Ollama
   curl -fsSL https://ollama.com/install.sh | sh

   # Download Gemma 3n
   ollama pull gemma3n:e4b
   ollama pull gemma3n:e2b

   # Install Python dependencies
   pip install -r requirements.txt
   ```

### Running Applications

1. **Multimodal Chat**:
   ```bash
   streamlit run gemma3n_multimodal_chat.py
   ```

2. **Voice Assistant**:
   ```bash
   streamlit run gemma3n_voice_assistant.py
   ```

3. **Coding Agent**:
   ```bash
   python gemma3n_coding_agent.py --interactive
   ```

4. **Document Analyzer**:
   ```bash
   streamlit run gemma3n_document_analyzer.py
   ```

## 🐳 Docker Deployment

For containerized deployment:

```bash
docker-compose up -d
```

## 💡 Use Cases Demonstrated

- **Multimodal Chat**: Customer support, education, content creation
- **Voice Assistant**: Accessibility, hands-free operation, smart home integration
- **Coding Agent**: Development assistance, code review, debugging
- **Document Analysis**: Legal document review, research, data extraction

## 🔧 Customization

Each application is designed to be easily customizable:

- **API Providers**: Switch between Ollama, Together AI, Google AI Studio
- **Models**: Support for both E2B and E4B variants
- **UI/UX**: Streamlit components can be modified or replaced
- **Features**: Add new analysis types, commands, or integrations

## 📚 Learning Resources

- [Gemma 3n Documentation](https://ai.google.dev/gemma/docs/gemma-3n)
- [Ollama Documentation](https://ollama.com/docs)
- [Streamlit Documentation](https://docs.streamlit.io)

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve these applications.

## 📄 License

This project is open source and available under the MIT License.
