import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
from model import preprocess
import json

load_dotenv()  ## load all our environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

def get_gemini_response_with_pdf(input, pdf_content):
    model = genai.GenerativeModel('gemini-pro')
    # Combine the input prompt with the PDF content
    combined_input = f"{input}\n\n{pdf_content}"
    response = model.generate_content(combined_input)
    return response.text

def get_gemini_response_with_pdf_and_jd(input, pdf_content, input_text):
    model = genai.GenerativeModel('gemini-pro')
    # Combine the input prompt with the PDF content
    combined_input = f"{input}\n\n{pdf_content}\n\n{input_text}"
    response = model.generate_content(combined_input)
    return response.text

def get_gemini_response_with_jd(input, input_text):
    model = genai.GenerativeModel('gemini-pro')
    # Combine the input prompt with the PDF content
    combined_input = f"{input}\n\n{input_text}"
    response = model.generate_content(combined_input)
    return response.text

# New Changes
st.header("SmartHire: Next-Gen Recruitment Platform")
st.subheader('Find the Perfect Fit for Your Team')
input_text = st.text_input("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your Resume(PDF)...", type=["pdf"])
pdf_content = ""

submit1 = st.button("Submit")

input_prompt1 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to extract the job description entered on the different sections like job title, skills required, educational qualification 
of candidate etc. 
Output should be in a string like below example:
"Job Title: Front-end Web Developer Skills Required: HTML CSS JavaScript PHP WordPress WooCommerce UI/UX design Graphic design 
REST API development Relational databases (e.g., MySQL) Agile and test-driven development best practices Eligibility Criteria: 
Bachelor's degree in computer science"
"""

if submit1:
    if input_text is not None:
        response = get_gemini_response_with_jd(input_prompt1, input_text)
        st.subheader("The Response is")
        answer = preprocess(response)
        st.write(answer)
        # convert_to_text(response)
    else:
        st.write("Please enter a Job Description to proceed.")

st.markdown("---")
st.caption("SmartHire: Next-Gen Recruitment Platform")