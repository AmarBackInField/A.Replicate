from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict
from utils import remove_json_wrapper, load_json_to_dict, setup_react_project, file_writting, run_react_app, process_pdf
from rep.src.rep.crew import Rep
import os

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to allow specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize project state
project_state = {
    "project_started": False,
    "json_processed": False,
    "react_setup": False,
    "file_written": False,
    "react_running": False,
    "react_app_name": "",
    "inputs": ""
}

input_file = 'report5.json'
output_file = 'report6.json'

class ProjectData(BaseModel):
    react_app_name: str
    user_input: str

@app.post("/start_project")
async def start_project(data: ProjectData):
    react_app_name = data.react_app_name
    user_input = data.user_input

    if not react_app_name or not user_input:
        raise HTTPException(status_code=400, detail="React app name and user input are required!")

    project_state["project_started"] = True
    project_state["inputs"] = user_input
    project_state["react_app_name"] = react_app_name

    try:
        Rep().crew().kickoff(inputs={"user_input": user_input})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during project kickoff: {e}")

    remove_json_wrapper(input_file, output_file)
    project_state["json_processed"] = True

    loaded_data = load_json_to_dict(output_file)
    setup_react_project(react_app_name)
    project_state["react_setup"] = True
    file_writting(loaded_data)
    project_state["file_written"] = True

    return {"message": "Project setup completed successfully!", "state": project_state}

@app.post("/run_react_app")
async def start_react():
    if not project_state["react_setup"] or not project_state["file_written"]:
        raise HTTPException(status_code=400, detail="Project setup is not complete!")

    run_react_app()
    project_state["react_running"] = True
    return {"message": "React app is running!", "state": project_state}

@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    extracted_text = process_pdf(file.file)
    if not extracted_text:
        raise HTTPException(status_code=500, detail="Failed to extract text from PDF!")

    project_state["inputs"] = extracted_text
    return {"message": "PDF processed successfully!", "extracted_text": extracted_text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, debug=True)
