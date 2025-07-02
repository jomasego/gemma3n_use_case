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
