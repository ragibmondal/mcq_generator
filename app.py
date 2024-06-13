import streamlit as st
import time
import base64
import io
from fpdf import FPDF

# Set the page configuration
st.set_page_config(page_title="MCQs Generator App",
                   page_icon="🧐",
                   layout="centered",
                   initial_sidebar_state="auto",
                   )
from src.helper import llm_chain
from src.data_util import read_input_file
from src.logger import logging

# Set the page title
st.title(':red[MCQ] :blue[Generator]')
st.caption('                By :orange[Gemini-Flash-1.5] using Langchain 🐦')

def create_pdf(response):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=response)
    pdf_bytes = pdf.output(dest="S").encode("latin-1")
    return pdf_bytes

with st.sidebar:
    # uploading the input file
    uploaded_file = st.file_uploader("Choose a PDF | Text file",
                                     accept_multiple_files=False,
                                     type=['txt', 'pdf']
                                     )
    # Number of mcq questions user wants
    number = st.number_input("Insert a number",
                             min_value=1,
                             max_value=100,
                             value=5, placeholder="Type a number...")
    # Difficulty level slider
    level = st.select_slider('Select difficulty',
                             options=['Easy', 'Medium', 'Hard'])
    # Language selection
    language = st.selectbox('Select Language', ['English', 'Bangla', 'Hindi', 'Urdu', 'French', 'Spanish', 'German', 'Italian'])

if uploaded_file and number and level and language:
    data = read_input_file(uploaded_file)
    gen_button = st.button("Generate", key="gen_button")

if gen_button:
    try:
        with st.spinner('Generating Multi Choice Questions...'):
            # Generating the response from the model
            response = llm_chain.run(number=number,
                                     difficulty=level,
                                     text=data,
                                     language=language)
            # print(response)
        logging.info('MCQ are generated')
    except Exception as e:
        st.error(f"An error occurred: {e}")
    else:
        # write to UI
        message_placeholder = st.empty()
        full_response = ""
        for chunk in response.replace('\n', '  \n').replace('\t', '----'):
            full_response += chunk
            time.sleep(0.005)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

        # PDF download button
        pdf_download_button = st.download_button(
            label="Download PDF",
            data=create_pdf(response),
            file_name="mcqs.pdf",
            mime="application/pdf"
        )
