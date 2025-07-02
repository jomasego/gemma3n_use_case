
import streamlit as st
import requests
import base64
from io import BytesIO
from PIL import Image
import json
import os

# Streamlit app for Gemma 3n Multimodal Chat
st.set_page_config(
    page_title="Gemma 3n Multimodal Assistant",
    page_icon="🤖",
    layout="wide"
)

# Sidebar configuration
st.sidebar.title("Gemma 3n Configuration")
api_provider = st.sidebar.selectbox(
    "Choose API Provider",
    ["Ollama (Local)", "Together AI", "Google AI Studio"]
)

# API configuration based on provider
if api_provider == "Ollama (Local)":
    ollama_url = st.sidebar.text_input("Ollama URL", "http://localhost:11434")
    model_name = st.sidebar.selectbox("Model", ["gemma3n:e4b", "gemma3n:e2b"])
elif api_provider == "Together AI":
    together_api_key = st.sidebar.text_input("Together AI API Key", type="password")
    model_name = "google/gemma-3n-E4B-it"
else:
    google_api_key = st.sidebar.text_input("Google AI API Key", type="password")
    model_name = "gemma-3n-e4b"

st.title("🤖 Gemma 3n Multimodal Assistant")
st.markdown("Upload images, record audio, or ask text questions!")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# File uploaders
col1, col2 = st.columns(2)
with col1:
    uploaded_image = st.file_uploader("Upload an image", type=['png', 'jpg', 'jpeg'])
with col2:
    uploaded_audio = st.file_uploader("Upload audio", type=['mp3', 'wav', 'ogg'])

# Display uploaded image
if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_container_width=True)

# Chat interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Ask about the image, audio, or anything else..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                if api_provider == "Ollama (Local)":
                    response = call_ollama_api(prompt, uploaded_image, uploaded_audio, ollama_url, model_name)
                elif api_provider == "Together AI":
                    response = call_together_api(prompt, uploaded_image, uploaded_audio, together_api_key, model_name)
                else:
                    response = call_google_ai_api(prompt, uploaded_image, uploaded_audio, google_api_key, model_name)

                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

            except Exception as e:
                st.error(f"Error: {str(e)}")

def call_ollama_api(prompt, image, audio, url, model):
    """Call Ollama local API with multimodal support"""
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    # Add image if provided
    if image:
        image_data = base64.b64encode(image.getvalue()).decode()
        payload["images"] = [image_data]

    # Note: Audio support coming soon in Ollama
    if audio:
        st.warning("Audio support coming soon to Ollama!")

    response = requests.post(f"{url}/api/generate", json=payload)
    return response.json().get("response", "No response")

def call_together_api(prompt, image, audio, api_key, model):
    """Call Together AI API with multimodal support"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    messages = [{"role": "user", "content": prompt}]

    # Add image if provided
    if image:
        image_data = base64.b64encode(image.getvalue()).decode()
        messages[0]["content"] = [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
        ]

    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": 1000
    }

    response = requests.post("https://api.together.xyz/v1/chat/completions", 
                           headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"]

def call_google_ai_api(prompt, image, audio, api_key, model):
    """Call Google AI Studio API with multimodal support"""
    # Implementation for Google AI Studio API
    # This would use the official Google AI SDK
    st.info("Google AI Studio integration - use the SDK for full implementation")
    return "Response from Google AI Studio (implement with official SDK)"

# Add reset button
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rewrite()
