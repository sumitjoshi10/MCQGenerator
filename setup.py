from setuptools import find_packages,setup

setup(
    name="MCQgenerator",
    version="0.0.1",
    author="Sumit Joshi",
    author_email="sumit.joshi9818@gmail.com",
    install_requires = ["google-generativeai","langchain","streamlit","python-dotenv","PyPDF2"],
    packages=find_packages()
)