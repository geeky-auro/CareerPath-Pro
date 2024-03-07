import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Google API Key
API_KEY = os.environ.get("GOOGLE_API_KEY")

# Configure Streamlit page settings
st.set_page_config(
    page_title="CareerPath Pro",
    page_icon="👨‍💼",
    layout="centered",
)

# Check if API key is provided
if not API_KEY:
    st.error("Please set the GOOGLE_API_KEY environment variable.")
    st.stop()

# Function to configure Gemini AI model with the provided API key
def configure_gemini_api(api_key):
    genai.configure(api_key=api_key)

# Configure Gemini AI model with the provided API key
configure_gemini_api(API_KEY)

# Function to get response from Gemini AI
def get_gemini_response(input_text):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input_text)
    return response.text

# Function to extract text from uploaded PDF file
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Prompt Template
input_prompt = """
As a Career Counsellor persona, you are tasked with analyzing a user's resume. 
Your job is to scrutinize the details of their skills, experiences, and qualifications, then provide a prediction for their next best career option. 
Consider the user's career progression, transferable skills, and potential areas for growth or improvement. 
Guide them towards a career path that aligns with their capabilities and career objectives.
resume:{text}

I want the response in one single string having the structure
Best Suited Option :
"""

## Streamlit app
st.title("Career Path Pro")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the PDF")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt.format(text=text))
        st.subheader("Response:")
        st.write(response)