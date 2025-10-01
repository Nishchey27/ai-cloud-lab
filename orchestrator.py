import subprocess
import json
import os

def run_data_analysis_tool(file_path):
    """
    Orchestrates a Docker container to analyze a given dataset.

    Args:
        file_path (str): The path to the dataset on the host machine.

    Returns:
        dict: The analysis results from the container, or an error message.
    """
    try:
        # Construct the full command to run the Docker container
        # Using 'os.path.abspath' to get a full path, which is more reliable for Docker.
        local_path = os.path.abspath(file_path)

        # The docker run command with volume mounting
        # Ensure the local path uses forward slashes for cross-platform compatibility with Docker
        # You might need to manually adjust the volume path for a different OS (e.g., macOS/Linux)
        # The part after the colon is the path inside the container, which is fixed at '/app'
        command = [
            "docker", "run", "--rm",
            "-v", f"{local_path}:/app/{os.path.basename(local_path)}",
            "data-analyzer",
            "python", "/app/analyze_data.py", f"/app/{os.path.basename(local_path)}"
        ]

        # Execute the command and capture the output
        # We use subprocess.run with capture_output=True and text=True
        print(f"Executing command: {' '.join(command)}")
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        # The script inside the container prints a JSON object.
        # We parse this JSON output and return it.
        analysis_output = json.loads(result.stdout)

        return analysis_output

    except subprocess.CalledProcessError as e:
        # If the command fails, this block catches the error and prints it
        print(f"Error running Docker command: {e}")
        print(f"Stderr: {e.stderr}")
        return {"error": f"Docker command failed: {e.stderr}"}
    except FileNotFoundError:
        return {"error": "Docker is not running or the command was not found."}
    except json.JSONDecodeError:
        print(f"Failed to parse JSON output: {result.stdout}")
        return {"error": "Failed to parse JSON output from container."}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Example usage:
    # Assuming you have 'sample_data.csv' in the same directory
    test_file = "sample_data.csv"
    analysis_results = run_data_analysis_tool(test_file)
    print("\n--- Final Analysis Results (From Orchestrator) ---")
    print(json.dumps(analysis_results, indent=4))