# File Path: ai-cloud-lab/main.py
import os
import shutil
from fastapi import FastAPI, UploadFile, File, Form
from orchestrator import run_data_analysis_tool, run_text_summarization_tool
from ai_brain import decide_tool_and_params

app = FastAPI(title="AI Lab-to-Cloud Orchestrator")

@app.post("/agent-request")
def agent_request_endpoint(prompt: str = Form(...), file: UploadFile = File(...)):
    uploads_dir = "uploads"
    os.makedirs(uploads_dir, exist_ok=True)
    file_path = os.path.join(uploads_dir, file.filename)

    # Save the uploaded file to the 'uploads' directory
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Ask the AI brain to make a decision
    ai_prompt = f"User prompt: '{prompt}'. The user has uploaded a file named '{file.filename}'."
    decision = decide_tool_and_params(ai_prompt)

    result = {}
    if "error" in decision:
        result = {"error": decision["error"]}
    else:
        tool_name = decision.get("tool_name")
        if not tool_name:
            result = {"error": "AI failed to determine a valid tool."}
        else:
            print(f"AI decided to use tool '{tool_name}' on file '{file_path}'")
            if tool_name == "data_analyzer":
                result = run_data_analysis_tool(file_path)
            elif tool_name == "text_summarizer":
                result = run_text_summarization_tool(file_path)
            else:
                result = {"error": f"AI chose an unknown tool: '{tool_name}'"}

    # Clean up the uploaded file after the task is complete
    os.remove(file_path)

    return result