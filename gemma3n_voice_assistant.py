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

def c
