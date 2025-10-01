import sys
import json
from transformers import pipeline


def summarize_text(file_path):
    """
    Summarizes the text content of a given file.

    Args:
        file_path (str): The path to the text file.

    Returns:
        dict: A dictionary containing the summary or an error message.
    """
    try:
        # Load the content from the file
        with open(file_path, 'r', encoding='utf-8') as f:
            text_content = f.read()

        # Initialize the summarization pipeline from Hugging Face.
        # 'sshleifer/distilbart-cnn-12-6' is a lightweight yet effective model.
        summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

        # Generate the summary
        # We set a min and max length for a concise summary.
        summary = summarizer(text_content, max_length=150, min_length=30, do_sample=False)

        result = {
            "original_char_count": len(text_content),
            "summary": summary[0]['summary_text']
        }

        return result

    except FileNotFoundError:
        return {"error": f"Error: The file at {file_path} was not found."}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python summarize_text.py <path_to_text_file>")
    else:
        file_path = sys.argv[1]
        summary_result = summarize_text(file_path)
        # Output the result as a JSON string
        print(json.dumps(summary_result, indent=4))