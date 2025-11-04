# AI Lab-to-Cloud Orchestrator

A dynamic, AI-powered system that creates and orchestrates specialized containerized labs on demand to perform complex tasks based on user-uploaded files.

---

## 🚀 Concept

This project demonstrates a novel approach to AI assistance. Instead of just providing information, the "AI Lab-to-Cloud Orchestrator" acts as a dynamic lab technician. It analyzes a user's natural language request and the provided file, selects the appropriate containerized tool from its library (e.g., data analysis, text summarization), and spins it up on demand using Docker to execute the task and deliver a result.

## ✨ Features

* **AI-Powered Tool Selection:** Uses Groq and Llama 3 to intelligently route tasks.
* **Dynamic Container Orchestration:** Launches Docker containers on the fly for isolated and reproducible task execution.
* **Interactive File Uploads:** Allows users to upload their own files (`.csv`, `.txt`, `.pdf`) for processing.
* **Extensible Architecture:** New labs with new capabilities can be easily added.

## ⚙️ How It Works

1.  **API Layer:** A **FastAPI** server provides an endpoint (`/agent-request`) that accepts a user's prompt and a file upload.
2.  **File Handling:** The uploaded file is temporarily saved to an `uploads` directory.
3.  **AI Brain:** The prompt and filename are sent to the **Groq API**. The Llama 3 model decides which tool is right for the task and responds with a JSON decision.
4.  **Orchestrator:** The Python orchestrator receives the AI's decision and executes the correct **Docker** command, pointing it to the temporarily saved file.
5.  **Docker Labs:** A specialized Docker container (e.g., `data-analyzer` or `text-summarizer` with PDF support) is launched, performs its task, and returns a JSON result.
6.  **Cleanup:** The temporarily uploaded file is automatically deleted.

## 🛠️ Setup & Run

1.  **Prerequisites:** Ensure you have Docker Desktop installed and running.
2.  **Clone the Repository:** `git clone <https://github.com/Nishchey27/ai-cloud-lab.git>
3.  **Create a Secrets File:** Create a `.env` file in the root directory.
4.  **Add Your API Key:** Add your Groq API key to the `.env` file: `GROQ_API_KEY="your-key-goes-here"`
5.  **Install Dependencies:** `pip install -r requirements.txt`
6.  **Build Docker Images:**
    * `cd data-analyzer-lab && docker build -t data-analyzer . && cd ..`
    * `cd text-summarizer-lab && docker build -t text-summarizer . && cd ..`
7.  **Run the Server:** `uvicorn main:app --reload`
8.  **Access the API:** Open your browser to **`http://127.0.0.1:8000/docs`** to test the file upload endpoint.

## 📝 A Note on the API Provider

Our initial plan was to use the Cerebras API. During development, we encountered a persistent, region-specific DNS issue. To ensure a functional project, we demonstrated adaptability by pivoting to the Groq API. Our `ai_brain.py` module is designed to be provider-agnostic.

## 🎬 Demo Video

[Link to your short demo video here]
