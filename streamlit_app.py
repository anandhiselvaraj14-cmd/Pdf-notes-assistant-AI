import streamlit as st
import pymupdf  # PyMuPDF
from google import genai
import os

# Streamlit பக்க வடிவமைப்பு
st.set_page_config(page_title="AI PDF Notes Assistant", layout="centered")
st.title("📚 AI PDF Notes Assistant")
st.write("Upload your study PDF and get AI insights instantly!")

# Streamlit Secrets-ல் இருந்து பாதுகாப்பாக API Key-ஐ எடுத்தல்
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error("API Key missing! Please add GEMINI_API_KEY in Streamlit Secrets.")
    st.stop()

# PDF கோப்பை அப்லோடு செய்யும் பகுதி
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # PDF-ல் இருந்து டெக்ஸ்ட்டை பிரித்தெடுத்தல்
    with st.spinner("Extracting text from PDF..."):
        text = ""
        with pymupdf.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
    
    if text.strip() == "":
        st.warning("No text found in the PDF. Please upload a readable PDF.")
    else:
        st.success("Text extracted successfully!")
        
        # AI செய்ய வேண்டிய வேலைகளுக்கான ஆப்ஷன்கள்
        task = st.selectbox(
            "What would you like the AI to do?",
            ["Summary", "Key Points", "Quiz Questions", "Simple Explanation"]
        )
        
        if st.button("Generate with AI"):
            with st.spinner(f"Generating {task}... Please wait..."):
                try:
                    # பயனரின் தேர்வுக்கு ஏற்ப ப்ராம்ப்ட் அமைத்தல்
                    prompt = f"Based on the following text, provide a comprehensive {task.lower()}:\n\n{text[:8000]}"
                    
                    # Gemini API மூலம் பதிலை உருவாக்குதல்
                    response = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=prompt,
                    )
                    
                    # பதிலை திரையில் காட்டுதல்
                    st.markdown(f"### 🤖 AI Generated {task}")
                    st.write(response.text)
                    
                except Exception as ex:
                    st.error(f"An error occurred with the AI Model: {ex}")
                    
