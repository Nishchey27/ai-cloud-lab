import sys
import pandas as pd
from sklearn.ensemble import IsolationForest


def analyze_data(file_path):
    """
    Analyzes a CSV file for basic statistics and identifies potential anomalies.

    Args:
        file_path (str): The path to the CSV file to analyze.

    Returns:
        dict: A dictionary containing the summary statistics and identified anomalies.
    """
    try:
        # Load the dataset
        df = pd.read_csv(file_path)

        # --- Part 1: Basic Statistics ---
        # Get descriptive statistics for numerical columns
        desc_stats = df.describe(include='number').to_dict()

        # Check for missing values
        missing_values = df.isnull().sum().to_dict()

        # Get the first few rows to show the data structure
        head_data = df.head().to_dict()

        # --- Part 2: Anomaly Detection ---
        # Select only numerical columns for anomaly detection
        numeric_cols = df.select_dtypes(include='number').columns
        if not numeric_cols.empty:
            # Initialize Isolation Forest model
            # Isolation Forest is a good choice for this task as it's effective for outlier detection and works well without needing labeled data.
            model = IsolationForest(random_state=42)

            # Fit the model and predict anomalies (-1 for anomalies, 1 for normal)
            df['anomaly_score'] = model.fit_predict(df[numeric_cols])

            # Filter for rows identified as anomalies
            anomalies = df[df['anomaly_score'] == -1].to_dict('records')
        else:
            anomalies = "No numerical data to analyze for anomalies."

        # --- Part 3: Compile and Return Results ---
        result = {
            "summary_statistics": desc_stats,
            "missing_values": missing_values,
            "data_preview": head_data,
            "anomalies": anomalies
        }

        return result

    except FileNotFoundError:
        return {"error": f"Error: The file at {file_path} was not found."}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}


# This part allows the script to be run from the command line,
# accepting a file path as an argument.
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_data.py <path_to_csv_file>")
    else:
        file_path = sys.argv[1]
        analysis_result = analyze_data(file_path)
        # For this demo, we'll print the result. In the final version,
        # this would be sent back to the orchestrator (FastAPI).
        import json

        print(json.dumps(analysis_result, indent=4))