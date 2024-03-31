import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
from Excel import convert_to_excel
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
st.subheader('Elevate Your Resume with Our Optimization Tools')
input_text = st.text_input("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your Resume(PDF)...", type=["pdf"])
pdf_content = ""

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit5 = st.button("Submit")

submit1 = st.button("Tell Me About the Resume")

submit2 = st.button("How Can I Improve my Skills")

submit3 = st.button("What are the Keywords That are Missing")

# submit4 = st.button("Percentage match")

input_prompt1 = """
 You are an experienced Technical Human Resource Manager, your task is to review the provided resume against the job description.
  Please share your professional evaluation on whether the candidate's profile aligns with the role.
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
You are a Technical Human Resource Manager with expertise in data science,
your role is to scrutinize the resume in light of the job description provided.
Share your insights on the candidate's suitability for the role from an HR perspective.
Additionally, offer advice on enhancing the candidate's skills and identify areas where improvement is needed.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality,
your task is to evaluate the resume against the provided job description. As a Human Resource manager,
 assess the compatibility of the resume with the role. Give me what are the keywords that are missing
 Also, provide recommendations for enhancing the candidate's skills and identify which areas require further development.
"""
# input_prompt4 = """
# You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality,
# your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
# the job description. First, the output should come as a percentage and then keywords missing and last final thoughts.
# """

input_prompt5 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality,
your task is to evaluate the resume and extract the following information from the resume i.e., 
1.Name  2.Skills  3.Work Experience  4.Projects  5.Certifications  6.Education
The output should be in the below order only.
{"Name": "Arnav Jain", "Skills": ["C/C++", "Python", "MySQL", "Machine Learning", "Computer Vision", "Data Science", "Data Analytics", "NLP", "Salesforce", "Swift UI", "HTML", "CSS"], 
"Work Experience": ["Salesforce Developer, Salesforce, 05/2023 - 07/2023", "Machine Learning Intern, IISc Bangalore, 02/2023 - 10/2023",
    "AI ML Virtual Internship, Amazon Web Services (AWS), 05/2023 - 07/2023"], "Projects": ["Brain Tumor Detection Model, 08/2023 - 10/2023",
    "Cursor Controlled by Retina, 10/2022 - 11/2022", "Twitter Sentiment Analysis, 03/2023 - 05/2023",
    "Pneumonia Detection, 02/2023 - 05/2023", "Car Price Predictor, 11/2022 - 12/2022"], "Certifications": [Trailhead modules & Developer Superset: Salesforce Fundamentals, Automation, Apex programming, Relationship & Process Management.],
    "Education": [B.Tech in Computer Science and Engineering, SRM Institute of Science and Technology, Kattankulathur, 09/2020 - Present]}
    Use this as an example only.
""" 

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_text(uploaded_file)
        response = get_gemini_response_with_pdf_and_jd(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a PDF file to proceed.")

elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_text(uploaded_file)
        response = get_gemini_response_with_pdf_and_jd(input_prompt2, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a PDF file to proceed.")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_text(uploaded_file)
        response = get_gemini_response_with_pdf_and_jd(input_prompt3, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a PDF file to proceed.")

# elif submit4:
#     if uploaded_file is not None:
#         pdf_content = input_pdf_text(uploaded_file)
#         response = get_gemini_response_with_pdf_and_jd(input_prompt4, pdf_content, input_text)
#         st.subheader("The Response is")
#         st.write(response)
#     else:
#         st.write("Please upload a PDF file to proceed.")

elif submit5:
    if uploaded_file is not None:
        pdf_content = input_pdf_text(uploaded_file)
        response = get_gemini_response_with_pdf(input_prompt5, pdf_content)
        st.subheader("Your Resume is Submitted ")
        # st.write(response)
        data_dict = json.loads(response)
        convert_to_excel(data_dict)
    else:
        st.write("Please upload a PDF file to proceed.")

st.markdown("---")
st.caption("SmartHire: Next-Gen Recruitment Platform")
