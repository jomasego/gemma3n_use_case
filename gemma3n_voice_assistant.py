
import streamlit as st
import requests
import speech_recognition as sr
from gtts import gTTS
import pygame
import tempfile
import io
import json
import threading
import queue
import numpy as np
from pydub import AudioSegment
import base64
import time

# Voice Assistant powered by Gemma 3n
st.set_page_config(
    page_title="Gemma 3n Voice Assistant",
    page_icon="🎤",
    layout="wide"
)

# Initialize pygame for audio playback
pygame.mixer.init()

# Sidebar configuration
st.sidebar.title("Voice Assistant Settings")
ollama_url = st.sidebar.text_input("Ollama URL", "http://localhost:11434")
model_name = st.sidebar.selectbox("Gemma 3n Model", ["gemma3n:e4b", "gemma3n:e2b"])
voice_language = st.sidebar.selectbox("Voice Language", ["en", "es", "fr", "de", "it"])
voice_enabled = st.sidebar.checkbox("Enable Voice Responses", True)

st.title("🎤 Gemma 3n Voice Assistant")
st.markdown("Talk to your AI assistant using voice commands!")

# Initialize session state
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "is_listening" not in st.session_state:
    st.session_state.is_listening = False

# Voice recognition setup
recognizer = sr.Recognizer()
microphone = sr.Microphone()

def listen_for_speech():
    """Listen for speech input and return text"""
    try:
        with microphone as source:
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=1)
            st.info("🎤 Listening... Speak now!")

            # Listen for audio
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)

        # Convert speech to text
        text = recognizer.recognize_google(audio)
        return text
    except sr.WaitTimeoutError:
        return "⏰ Listening timeout - no speech detected"
    except sr.UnknownValueError:
        return "❌ Could not understand audio"
    except sr.RequestError as e:
        return f"❌ Error with speech recognition service: {e}"

def call_gemma3n_api(prompt, conversation_history):
    """Call Gemma 3n via Ollama with conversation context"""
    # Build conversation context
    context = "You are a helpful voice assistant. Keep responses conversational and concise.\n\n"
    for msg in conversation_history[-5:]:  # Last 5 messages for context
        context += f"Human: {msg['user']}\nAssistant: {msg['assistant']}\n\n"

    full_prompt = context + f"Human: {prompt}\nAssistant:"

    payload = {
        "model": model_name,
        "prompt": full_prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "max_tokens": 200
        }
    }

    try:
        response = requests.post(f"{ollama_url}/api/generate", json=payload)
        response.raise_for_status()
        return response.json().get("response", "Sorry, I couldn't generate a response.")
    except requests.exceptions.RequestException as e:
        return f"Error calling Gemma 3n: {str(e)}"

def text_to_speech(text, language="en"):
    """Convert text to speech and play it"""
    if not voice_enabled:
        return

    try:
        # Create TTS object
        tts = gTTS(text=text, lang=language, slow=False)

        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            tts.save(tmp_file.name)

            # Play the audio
            pygame.mixer.music.load(tmp_file.name)
            pygame.mixer.music.play()

            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)

    except Exception as e:
        st.error(f"Error with text-to-speech: {str(e)}")

# Control buttons
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🎤 Start Listening", disabled=st.session_state.is_listening):
        st.session_state.is_listening = True

        # Listen for speech
        with st.spinner("Listening for your voice..."):
            user_input = listen_for_speech()

        st.session_state.is_listening = False

        if not user_input.startswith("⏰") and not user_input.startswith("❌"):
            # Display user input
            st.success(f"You said: {user_input}")

            # Get AI response
            with st.spinner("Thinking..."):
                ai_response = call_gemma3n_api(user_input, st.session_state.conversation_history)

            # Add to conversation history
            st.session_state.conversation_history.append({
                "user": user_input,
                "assistant": ai_response,
                "timestamp": time.time()
            })

            # Display AI response
            st.info(f"Assistant: {ai_response}")

            # Convert to speech
            if voice_enabled:
                with st.spinner("Speaking..."):
                    text_to_speech(ai_response, voice_language)
        else:
            st.warning(user_input)

with col2:
    if st.button("🔇 Stop Voice"):
        pygame.mixer.music.stop()

with col3:
    if st.button("🗑️ Clear History"):
        st.session_state.conversation_history = []

# Manual text input as fallback
st.subheader("💬 Or type your message:")
manual_input = st.text_input("Type your message here:")
if st.button("Send Text") and manual_input:
    # Get AI response
    with st.spinner("Processing..."):
        ai_response = call_gemma3n_api(manual_input, st.session_state.conversation_history)

    # Add to conversation history
    st.session_state.conversation_history.append({
        "user": manual_input,
        "assistant": ai_response,
        "timestamp": time.time()
    })

    # Display response
    st.success(f"You: {manual_input}")
    st.info(f"Assistant: {ai_response}")

    # Convert to speech
    if voice_enabled:
        text_to_speech(ai_response, voice_language)

# Display conversation history
if st.session_state.conversation_history:
    st.subheader("📝 Conversation History")
    for i, conv in enumerate(reversed(st.session_state.conversation_history[-10:])):
        with st.expander(f"Conversation {len(st.session_state.conversation_history) - i}"):
            st.write(f"**You:** {conv['user']}")
            st.write(f"**Assistant:** {conv['assistant']}")
            st.write(f"*Time:* {time.ctime(conv['timestamp'])}")

# Installation instructions
with st.expander("📦 Installation Requirements"):
    st.code("""
# Install required packages
pip install streamlit speechrecognition gtts pygame pydub pyaudio

# Additional system requirements:
# - Ollama with Gemma 3n model installed
# - Microphone access
# - Audio output device

# Run with:
streamlit run gemma3n_voice_assistant.py
    """)

# Usage tips
with st.expander("💡 Usage Tips"):
    st.markdown("""
    - **Clear Speech**: Speak clearly and avoid background noise
    - **Internet Required**: Speech recognition and TTS require internet
    - **Model Setup**: Make sure Ollama is running with Gemma 3n loaded
    - **Microphone**: Grant microphone permissions when prompted
    - **Conversation Context**: The assistant remembers recent conversation
    """)
