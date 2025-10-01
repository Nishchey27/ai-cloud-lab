import subprocess
import json
import os

def run_data_analysis_tool(file_path):
    """
    Orchestrates the 'data-analyzer' container for a given dataset.
    """
    print("\n--- Running Data Analysis Lab ---")
    image_name = "data-analyzer"
    script_name = "analyze_data.py"
    try:
        local_path = os.path.abspath(file_path)
        container_path = f"/app/{os.path.basename(local_path)}"

        command = [
            "docker", "run", "--rm",
            "-v", f"{local_path}:{container_path}",
            image_name,
            "python", f"/app/{script_name}", container_path
        ]

        print(f"Executing command: {' '.join(command)}")
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)

    except subprocess.CalledProcessError as e:
        print(f"Error running Docker command for {image_name}: {e}")
        print(f"Stderr: {e.stderr}")
        return {"error": f"Docker command failed for {image_name}: {e.stderr}"}
    except Exception as e:
        return {"error": str(e)}

def run_text_summarization_tool(file_path):
    """
    Orchestrates the 'text-summarizer' container for a given text file.
    """
    print("\n--- Running Text Summarizer Lab ---")
    image_name = "text-summarizer"
    script_name = "summarize_text.py"
    try:
        local_path = os.path.abspath(file_path)
        container_path = f"/app/{os.path.basename(local_path)}"

        command = [
            "docker", "run", "--rm",
            "-v", f"{local_path}:{container_path}",
            image_name,
            "python", f"/app/{script_name}", container_path
        ]

        print(f"Executing command: {' '.join(command)}")
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)

    except subprocess.CalledProcessError as e:
        print(f"Error running Docker command for {image_name}: {e}")
        print(f"Stderr: {e.stderr}")
        return {"error": f"Docker command failed for {image_name}: {e.stderr}"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # --- Test Case 1: Data Analysis ---
    data_file = "sample_data.csv"
    if os.path.exists(data_file):
        analysis_results = run_data_analysis_tool(data_file)
        print("\n--- Final Analysis Results (From Orchestrator) ---")
        print(json.dumps(analysis_results, indent=4))
    else:
        print(f"\nError: Test file '{data_file}' not found.")

    # --- Test Case 2: Text Summarization ---
    text_file = "sample_text.txt"
    if os.path.exists(text_file):
        summary_results = run_text_summarization_tool(text_file)
        print("\n--- Final Summary Results (From Orchestrator) ---")
        print(json.dumps(summary_results, indent=4))
    else:
        print(f"\nError: Test file '{text_file}' not found. Please create it.")