import json
import sys
import subprocess
import os
from pathlib import Path
from constant import a

import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def remove_json_wrapper(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Remove the first and last lines if they contain triple backticks
    if lines[0].strip().startswith("```json"):
        lines = lines[1:]
    if lines[-1].strip().startswith("```"):
        lines = lines[:-1]
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(lines)

def load_json_to_dict(file_path):
    """
    Loads a JSON file into a Python dictionary.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    data.update(a)
    return data



def setup_react_project(react_app_name:str):
    commands = [
        f"npx create-react-app {react_app_name}",
        "cd mvr && npm install react-router-dom",
        "cd mvr && npm install framer-motion",
        "cd mvr && npm install -D tailwindcss@3",
        "cd mvr && npx tailwindcss init"
    ]
    
    for command in commands:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Error:", result.stderr)



def file_writting(loaded_data,react_app_name:str):
    list_of_files = []
    list_of_data = []

    # Assuming loaded_data is a dictionary with file paths as keys and data as values.
    for key, value in loaded_data.items():
        list_of_files.append(react_app_name+'/'+ key)  # Add file path to list
        list_of_data.append(value)  # Add corresponding data to list

    # Iterate over both lists simultaneously using zip
    for i, filepath in enumerate(list_of_files):
        print(i + 1)  # Start counting from 1 for better readability
        filepath = Path(filepath)
        filedir, filename = os.path.split(filepath)
        
        # Create directories if they don't exist
        if filedir != "":
            os.makedirs(filedir, exist_ok=True)

        # Overwrite file content every time
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(list_of_data[i])  # Write corresponding data to the file


import subprocess
import os

def run_react_app(react_app_name:str):
    project_dir = react_app_name

    # Change directory to 'mvr' and run npm start
    command = "cd {} && npm start".format(project_dir)

    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    # Print output and errors
    print(result.stdout)
    print(result.stderr)

def process_pdf(uploaded_file):
    """Process the uploaded PDF and extract text using LangChain"""
    try:
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            pdf_path = tmp_file.name
        
        # Use LangChain to load and extract text
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
        
        # Split the text into manageable chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        docs = text_splitter.split_documents(pages)
        
        # Combine all text from documents
        extracted_text = "\n".join([doc.page_content for doc in docs])
        
        # Clean up the temporary file
        os.unlink(pdf_path)
        
        return extracted_text
    
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return ""





