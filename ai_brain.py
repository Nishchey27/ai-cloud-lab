import os
import requests
import json
from dotenv import load_dotenv

# Load variables from the .env file into the environment
load_dotenv()

# Load the API key from the environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def decide_tool_and_params(user_prompt: str):
    """
    Sends a user prompt to the LLM to decide which tool to use.
    """
    if not GROQ_API_KEY or GROQ_API_KEY == "paste-your-new-groq-api-key-here":
        return {"error": "Groq API key is not configured. Please check your .env file."}

    system_prompt = """
    You are an expert orchestrator agent. Your job is to select the correct tool based on the user's prompt and the filename they provided.

    The available tools are:
    1. "data_analyzer": Use this for requests involving statistics, analysis, anomalies, or CSV files.
    2. "text_summarizer": Use this for requests involving summarizing text, articles, documents, or PDF/TXT files.

    You must decide which tool is appropriate.
    You must respond with only a single, valid JSON object in the following format, with no other text or explanation:
    {"tool_name": "..."}
    """

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-8b-instant", # This is the model name used by Groq
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.0
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()

        ai_response_text = response.json()['choices'][0]['message']['content']

        decision = json.loads(ai_response_text)
        return decision

    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {e}"}
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        return {"error": f"Failed to parse AI response: '{ai_response_text}'. Error: {e}"}