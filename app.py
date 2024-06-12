from datetime import datetime
import streamlit as st
import time
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import pdfplumber
import logging

# Set up logging
dir_path = os.path.join(os.getcwd(), 'logs')
os.makedirs(dir_path, exist_ok=True)
date = datetime.now().strftime('%Y_%m_%d_%H_%M')
log_file_name = os.path.join(dir_path, f"{date}.log")
FORMAT = "[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(filename=log_file_name,
                    encoding='utf-8',
                    format=FORMAT,
                    level=logging.INFO)
logging.info('Logging is Initiated...')

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("API_KEY")
logging.info(f'GOOGLE API KEY is {GOOGLE_API_KEY}')

# Create LLM model
@st.cache_resource
def create_llm_model():
    return ChatGoogleGenerativeAI(google_api_key=GOOGLE_API_KEY,
                                  model="gemini-1.5-flash-latest",
                                  temperature=0.3)

llm_model = create_llm_model()
logging.info('LLM model object is created...')

# Prompt template
Template = '''\
You are an expert in the creation of multi-choice questions in different languages. \
Your job is to create {number} multi-choice questions in {language} language at the {difficulty} level. \
Make the quiz to test the cognitive and analytical abilities of a user. \
Make sure the questions are not repeated and answer should be small and follow the below format for creating questions: \n
    1. first multi-choice question.\n
    Ans: \n\tA. "first choice here."\n\tB. "second choice here."\n\tC. "third choice here."\n\tD. "fourth choice here."\n
    Correct: "correct answer".\n
    2. second multi-choice question.\n
    Ans: \n\tA. "first choice here."\n\tB. "second choice here."\n\tC. "third choice here."\n\tD. "fourth choice here."\n
    Correct: "correct answer".\n
Using the following text to generate multi-choice questions based on the above instructions:
"Text": {text}
'''

mcq_prompt = PromptTemplate(
    input_variables=['number', 'difficulty', 'text', 'language'],
    template=Template
)

# Create LLM chain
llm_chain = LLMChain(llm=llm_model,
                     prompt=mcq_prompt,
                     output_key="mcq",
                     verbose=False)

logging.info('Base chain was created...')

# Read input file
def read_input_file(file_name):
    if file_name.name.endswith(".pdf"):
        try:
            with pdfplumber.open(file_name) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text()
            logging.info('Input PDF file was read')
            return text
        except Exception as e:
            logging.error(f"Error while reading input PDF file: {e}")
            raise Exception("Error while reading input PDF file.")
    elif file_name.name.endswith(".txt"):
        logging.info('Input Text file was read')
        return file_name.read().decode('utf-8')
    else:
        raise Exception("Unsupported file format. Only PDF and Text files are supported.")

# Streamlit app
def main():
    # Set the page configuration
    st.set_page_config(page_title="MCQs Creator App",
                       page_icon="💡",
                       layout="wide",
                       initial_sidebar_state="expanded")

    # Set the page title and styling
    st.markdown("""
        <h1 style='text-align: center; color: #FF4B4B;'>MCQ Generator</h1>
        <p style='text-align: center; color: #4B4BFF;'>By Gemini-Pro using Langchain by Ragib</p>
    """, unsafe_allow_html=True)

    # Create a sidebar with a custom CSS style
    st.markdown("""
        <style>
            .sidebar .sidebar-content {
                background-color: #F0F0F0;
                padding: 20px;
                border-radius: 10px;
            }
        </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.title("🔧 Settings")

        # Uploading the input file
        uploaded_file = st.file_uploader("Choose a PDF | Text file",
                                         accept_multiple_files=False,
                                         type=['txt', 'pdf'])

        # Number of MCQ questions user wants
        number = st.number_input("Number of Questions",
                                 min_value=1,
                                 max_value=70,
                                 value=5)

        # Difficulty level slider
        level = st.select_slider('Difficulty Level',
                                 options=['Easy', 'Medium', 'Hard'])

        # Language selection
        language = st.selectbox('Select Language', ['English', 'Spanish', 'French', 'German', 'Bangla', 'Hindi', 'Arabic'])

        if uploaded_file and number and level and language:
            data = read_input_file(uploaded_file)
            gen_button = st.button("Generate", key="gen_button")

    if gen_button:
        with st.spinner('Generating Multi Choice Questions...'):
            # Generating the response from the model
            response = llm_chain.run(number=number,
                                     difficulty=level,
                                     text=data,
                                     language=language)
            # print(response)
        logging.info('MCQ are generated')

    if response:
        # Write to UI with custom styling
        st.markdown(f"""
            <div style='background-color: #F0F0F0; padding: 20px; border-radius: 10px;'>
                <h2 style='text-align: center; color: #4B4BFF;'>Generated Questions</h2>
                <pre style='white-space: pre-wrap; word-wrap: break-word;'>{response}</pre>
            </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
