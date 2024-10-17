import os
import json
import PyPDF2
import traceback

def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
                
        except Exception as e:
            raise Exception ("Error Reading the pdf File")
        
    elif file.name.endswith(".txt"):
        try:
            return file.read().decode("utf-8")
        except Exception as e:
            raise Exception ("Error Reading the txt File")
    else:
        raise Exception(
            "Unsuported file formate only pdf or txt format"
        )
        
        
def get_table_data(quiz_str):
    try:
        #Convert quid from str to dict
        quiz_dict = json.loads(quiz_str)
        
        #looping through the dict file
        quiz_table = []
        for key, value in quiz_dict.items():
            mcq = value["mcq"]
            options = " || ".join(
                [
                    f"{option}--> {option_value}"
                    for option, option_value in value["options"].items()
                    ]
                )
            correct = value["correct"]
            quiz_table.append({"MCQ": mcq, "Choices": options, "Correct": correct})
        
        return quiz_table
    
    except Exception as e:
        traceback.print_exception(type(e), e , e.__traceback__)
        return False