from setuptools import find_packages,setup

setup(
    name='mcq_generator',
    version='1.0',
    author='ragib hasan',
    author_email='ragibhasan5303721@gmail.com',
    install_requires=['google-generativeai',
                      'langchain',
                      'streamlit',
                      'python-dotenv',
                      'PyPDF2'],
    packages=find_packages()
)
