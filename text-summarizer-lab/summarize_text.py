# File Path: ai-cloud-lab/text-summarizer-lab/summarize_text.py
import sys
import json
import PyPDF2
from transformers import pipeline

def get_text_from_file(file_path: str) -> str:
    text_content = ""
    if file_path.lower().endswith('.pdf'):
        with open(file_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_content += page_text + "\n"
    else:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            text_content = f.read()
    return text_content

def summarize_text(file_path: str):
    try:
        text_to_summarize = get_text_from_file(file_path)
        if not text_to_summarize.strip():
            return {"error": f"Could not extract any text from the file: {file_path}"}

        summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
        summary = summarizer(text_to_summarize, max_length=150, min_length=30, do_sample=False)

        result = {"original_char_count": len(text_to_summarize), "summary": summary[0]['summary_text']}
        return result
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python summarize_text.py <path_to_file>"}, indent=4))
    else:
        print(json.dumps(summarize_text(sys.argv[1]), indent=4))