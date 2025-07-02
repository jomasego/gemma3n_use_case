import streamlit as st
import requests
import base64
import io
import fitz  # PyMuPDF
from PIL import Image
import pandas as pd
import json
import tempfile
import os
from typing import List, Dict, Any

# Document Intelligence App powered by Gemma 3n
st.set_page_config(
    page_title="Gemma 3n Document Analyzer",
    page_icon="📄",
    layout="wide"
)

class DocumentAnalyzer:
    def __init__(self, ollama_url: str, model: str):
        self.ollama_url = ollama_url
        self.model = model

    def call_gemma3n(self, prompt: str, image_data: str = None) -> str:
        """Call Gemma 3n via Ollama with optional image"""
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,
                "top_p": 0.9
            }
        }

        if image_data:
            payload["images"] = [image_data]

        try:
            response = requests.post(f"{self.ollama_url}/api/generate", json=payload)
            response.raise_for_status()
            return response.json().get("response", "No response generated")
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}"

    def extract_pdf_pages(self, pdf_file) -> List[Image.Image]:
        """Extract pages from PDF as images"""
        pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
        pages = []

        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            mat = fitz.Matrix(2, 2)  # Zoom factor
            pix = page.get_pixmap(matrix=mat)
            img_data = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_data))
            pages.append(img)

        pdf_document.close()
        return pages

    def analyze_document_content(self, pages: List[Image.Image], analysis_type: str) -> List[Dict]:
        """Analyze document pages based on type"""
        results = []

        for i, page in enumerate(pages):
            # Convert image to base64
            img_buffer = io.BytesIO()
            page.save(img_buffer, format='PNG')
            img_data = base64.b64encode(img_buffer.getvalue()).decode()

            # Generate prompt based on analysis type
            if analysis_type == "summary":
                prompt = f"""Please provide a concise summary of the content shown in this document page {i+1}. 
                Focus on key points, main topics, and important information."""

            elif analysis_type == "extract_data":
                prompt = f"""Extract structured data from this document page {i+1}. 
                Look for tables, lists, key-value pairs, dates, numbers, and names. 
                Present the extracted data in a clear, organized format."""

            elif analysis_type == "questions":
                prompt = f"""Based on the content of this document page {i+1}, generate 5 relevant questions 
                that could be answered using the information shown. Include both factual and analytical questions."""

            elif analysis_type == "translation":
                prompt = f"""Identify the language of this document page {i+1} and provide an English translation 
                if it's in another language. If it's already in English, provide a summary instead."""

            elif analysis_type == "compliance":
                prompt = f"""Analyze this document page {i+1} for potential compliance issues, 
                legal concerns, or regulatory requirements. Look for dates, signatures, 
                terms and conditions, and any compliance-related content."""

            else:  # custom analysis
                prompt = f"""Analyze this document page {i+1} and provide insights about: {analysis_type}"""

            # Get analysis
            analysis = self.call_gemma3n(prompt, img_data)

            results.append({
                "page": i + 1,
                "analysis": analysis,
                "image": page
            })

        return results

# Streamlit UI
st.title("📄 Gemma 3n Document Analyzer")
st.markdown("Upload documents and get AI-powered analysis using Gemma 3n's multimodal capabilities!")

# Sidebar configuration
st.sidebar.title("Configuration")
ollama_url = st.sidebar.text_input("Ollama URL", "http://localhost:11434")
model_name = st.sidebar.selectbox("Gemma 3n Model", ["gemma3n:e4b", "gemma3n:e2b"])

# Initialize analyzer
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = DocumentAnalyzer(ollama_url, model_name)

# File upload
st.subheader("📁 Upload Document")
uploaded_file = st.file_uploader(
    "Choose a document", 
    type=['pdf', 'png', 'jpg', 'jpeg'],
    help="Upload PDF documents or images for analysis"
)

if uploaded_file is not None:
    # Analysis type selection
    analysis_types = {
        "summary": "📝 Document Summary",
        "extract_data": "📊 Data Extraction", 
        "questions": "❓ Generate Questions",
        "translation": "🌐 Translation/Language",
        "compliance": "⚖️ Compliance Review"
    }

    selected_analysis = st.selectbox(
        "Choose Analysis Type",
        options=list(analysis_types.keys()),
        format_func=lambda x: analysis_types[x]
    )

    # Custom analysis option
    if st.checkbox("Custom Analysis"):
        custom_prompt = st.text_input("Enter your specific analysis request:")
        if custom_prompt:
            selected_analysis = custom_prompt

    # Process document
    if st.button("🔍 Analyze Document"):
        with st.spinner("Processing document..."):
            try:
                # Handle different file types
                if uploaded_file.type == "application/pdf":
                    pages = st.session_state.analyzer.extract_pdf_pages(uploaded_file)
                else:
                    # Single image
                    image = Image.open(uploaded_file)
                    pages = [image]

                st.success(f"Extracted {len(pages)} page(s) from document")

                # Analyze pages
                with st.spinner("Analyzing content with Gemma 3n..."):
                    results = st.session_state.analyzer.analyze_document_content(pages, selected_analysis)

                # Store results in session state
                st.session_state.analysis_results = results
                st.session_state.analysis_type = selected_analysis

            except Exception as e:
                st.error(f"Error processing document: {str(e)}")

# Display results
if 'analysis_results' in st.session_state:
    st.subheader(f"📋 Analysis Results: {analysis_types.get(st.session_state.analysis_type, st.session_state.analysis_type)}")

    # Create tabs for each page
    if len(st.session_state.analysis_results) > 1:
        tabs = st.tabs([f"Page {r['page']}" for r in st.session_state.analysis_results])

        for tab, result in zip(tabs, st.session_state.analysis_results):
            with tab:
                col1, col2 = st.columns([1, 1])

                with col1:
                    st.image(result['image'], caption=f"Page {result['page']}", use_container_width=True)

                with col2:
                    st.markdown("**Analysis:**")
                    st.write(result['analysis'])
    else:
        # Single page
        result = st.session_state.analysis_results[0]
        col1, col2 = st.columns([1, 1])

        with col1:
            st.image(result['image'], caption="Document", use_container_width=True)

        with col2:
            st.markdown("**Analysis:**")
            st.write(result['analysis'])

    # Export results
    st.subheader("💾 Export Results")

    # Prepare export data
    export_data = []
    for result in st.session_state.analysis_results:
        export_data.append({
            "Page": result['page'],
            "Analysis": result['analysis']
        })

    # CSV export
    df = pd.DataFrame(export_data)
    csv = df.to_csv(index=False)
    st.download_button(
        label="📊 Download as CSV",
        data=csv,
        file_name=f"document_analysis_{st.session_state.analysis_type}.csv",
        mime="text/csv"
    )

    # JSON export
    json_data = json.dumps(export_data, indent=2)
    st.download_button(
        label="📄 Download as JSON",
        data=json_data,
        file_name=f"document_analysis_{st.session_state.analysis_type}.json",
        mime="application/json"
    )

# Usage examples
with st.expander("💡 Usage Examples"):
    st.markdown("""
    **Document Summary**: Get concise summaries of contracts, reports, or articles

    **Data Extraction**: Extract tables, names, dates, and structured information

    **Generate Questions**: Create quiz questions or study materials from documents

    **Translation**: Identify languages and translate foreign documents

    **Compliance Review**: Check documents for regulatory compliance issues

    **Custom Analysis**: Ask specific questions about document content
    """)

# Installation requirements
with st.expander("📦 Installation Requirements"):
    st.code("""
# Install required packages
pip install streamlit PyMuPDF pillow pandas requests

# System requirements:
# - Ollama with Gemma 3n model installed
# - Python 3.8+

# Run with:
streamlit run gemma3n_document_analyzer.py
    """)

# API status check
if st.sidebar.button("🔧 Test Connection"):
    try:
        response = requests.get(f"{ollama_url}/api/tags")
        if response.status_code == 200:
            models = response.json().get('models', [])
            gemma_models = [m['name'] for m in models if 'gemma3n' in m['name']]

            if gemma_models:
                st.sidebar.success(f"✅ Connected! Available models: {', '.join(gemma_models)}")
            else:
                st.sidebar.warning("⚠️ Connected but no Gemma 3n models found")
        else:
            st.sidebar.error("❌ Connection failed")
    except Exception as e:
        st.sidebar.error(f"❌ Error: {str(e)}")
