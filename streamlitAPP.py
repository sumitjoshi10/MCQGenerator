import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file,get_table_data
import streamlit as st
from src.mcqgenerator.logger import logging
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain

# Load the JSON File
response_path = os.path.join(os.getcwd(),"response.json")
with open(response_path,"r") as f:
    RESPONSE_JSON = json.load(f)
    
#Crete the title
st.title("MCQ Generator App with LangChain")

#create a form
with st.form("user_inputs"):
    #file upload
    uploaded_file = st.file_uploader("Upload a PDF or txt file")
    
    #number field
    mcq_count = st.number_input("No. of MCQs", min_value=3 , max_value= 50)
    
    #Subject
    subject = st.text_input("Insert Subject",max_chars=20)
    
    #Quiz Tone
    tone = st.text_input("Complexity Level of Questions",max_chars=20,placeholder="Simple")
    
    #add Button
    button = st.form_submit_button("Create MCQs")
    
    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("Loading...."):
            try:
                text = read_file(uploaded_file)
                response = generate_evaluate_chain({
                    "text" : text,
                    "number" : mcq_count,
                    "subject": subject,
                    "tone": tone,
                    "response_json": json.dumps(RESPONSE_JSON)
                })
                
            except Exception as e:
                traceback.print_exception(type(e), e , e.__traceback__)
                st.error("Error")
                
            else:
                if isinstance(response,dict):
                    # Extract Quiz data from the resposne
                    
                    quiz = response.get("quiz").split("\n")[1]
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        if table_data is not None:
                            df = pd.DataFrame(table_data)
                            df.index = df.index +1
                            st.table(df)
                            
                            #Display the review in the text box as well
                            st.text_area(label= "Review",value= response["review"])
                        else:
                            st.error("Error in the table data")
                else:
                    st.write(response)