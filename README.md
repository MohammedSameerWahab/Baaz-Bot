# Baaz Bot 🦅

**A smart AI-powered mentor to help students understand exactly where and why they lost marks on their examinations.**

It provides a detailed, conversational breakdown of a student's performance by comparing their answer script (read via OCR) to a "gold-standard" model answer.

## ✨ Key Features

  * **Intelligent Evaluation:** Uses a Generative LLM (Google Gemini) to perform a detailed comparison between a student's answer and a model solution.
  * **Interactive RAG Chatbot:** Built with LlamaIndex, the bot allows students to ask follow-up questions about their evaluation in a natural, conversational way.
  * **OCR Integration:** Reads student answers directly from uploaded images (typed text) using Tesseract and OpenCV for image preprocessing.
  * **Modern Web UI:** A clean, responsive chat interface built with Flask, HTML, and CSS.
  * **Real-time Streaming:** Bot responses are streamed word-by-word (via SSE) and render Markdown in real-time for a smooth, modern user experience.
  * **Conversation History:** Remembers the context of the chat for intelligent, follow-up questions.

## ⚙️ How It Works (The Two-Tiered Architecture)

This project is built on a two-tiered approach to ensure high-quality, relevant responses.

### Task 1: The "Insight Generation" Pipeline (Backend)

This is the data preparation step, orchestrated by `main.py`.

1.  **Read Inputs:** The system takes the official `questions.json` and a folder of the student's answer images (e.g., `data/student_01/`).
2.  **Run OCR:** Images are preprocessed with OpenCV and read by Tesseract to extract the raw text.
3.  **Generate Model Answers:** The LLM generates a "gold-standard" model answer for each question.
4.  **Generate Insights:** The LLM performs a detailed comparison, grading the student's answer against the model answer and producing a comprehensive feedback document (`insights.txt`).

### Task 2: The "RAG Chatbot" (Frontend)

This is the live web application, run by `app.py`.

1.  **Indexing:** On startup, LlamaIndex builds a vector index from the `insights.txt` file created in Task 1. This index becomes the bot's "knowledge base."
2.  **User Interaction:** A student interacts with the Baaz Bot web interface.
3.  **Context-Aware RAG:** When a student asks a question ("Why did I lose marks on question 3?"), the chat engine (using RAG) retrieves the most relevant parts of the `insights.txt` file to formulate a precise, context-aware answer.
4.  **Full Conversation:** The engine maintains session history, allowing students to ask general questions ("Who are you?") or follow-ups ("Can you explain that concept in more detail?").

## 🛠️ Tech Stack

  * **Backend:** Python, Flask
  * **AI/LLM:** Google Gemini (via API)
  * **RAG/VectorDB:** LlamaIndex
  * **Embeddings:** Hugging Face `bge-small-en-v1.5` (local)
  * **OCR:** Tesseract, OpenCV-Python
  * **Frontend:** HTML, CSS, JavaScript
  * **Libraries:** `marked.js` (for Markdown rendering), `EventSource` (for streaming)

## 📁 Project Structure

```
smart-mentor-chatbot/
├── app.py              # Main Flask web application (Task 2)
├── main.py             # Orchestrator script for data processing (Task 1)
├── requirements.txt
├── .env.example        # Example environment file
├── data/
│   ├── questions.json
│   └── student_01/     # Folder for student's answer images
├── src/
│   ├── task1_... .py   # Logic for generating model answers & insights
│   ├── task2_... .py   # Logic for building and querying the RAG index
│   ├── llm_client.py   # Wrapper for Gemini API calls
│   └── utils.py        # OCR, parsing, & text-processing helpers
├── static/
│   ├── css/style.css
│   └── js/script.js
└── templates/
    └── index.html
```

## 🚀 Getting Started

### Prerequisites

1.  **Python 3.10+**
2.  **Tesseract OCR Engine:** You must install Tesseract on your system.
      * **Windows:** Download and run the installer from [here](https://www.google.com/search?q=https://github.com/UB-Mannheim/tesseract/wiki).
          * **Important:** After installation, you must manually update the Tesseract path in `src/utils.py`:
            ```python
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            ```
      * **macOS:** `brew install tesseract`
      * **Linux:** `sudo apt-get install tesseract-ocr`

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/MohammedSameerWahab/baaz-bot.git
    cd baaz-bot
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv myVenv
    # Windows
    .\myVenv\Scripts\activate
    # macOS/Linux
    source myVenv/bin/activate
    ```

3.  **Install the required Python packages:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**

      * Create a file named `.env` in the root directory.
      * Add your Gemini API key:
        ```ini
        GEMINI_API_KEY="YOUR_API_KEY_HERE"
        ```

### How to Run

The project runs in two stages. You must run Stage 1 at least once to create the knowledge base for Stage 2.

#### Stage 1: Generate the Insights

1.  **Add Questions:** Edit `data/questions.json` to include the exam questions.
2.  **Add Student Answers:** Place the student's answer script images (e.g., `page_01.png`, `page_02.png`) inside a folder like `data/student_01`.
3.  **Run the Pipeline:**
    ```bash
    python main.py generate-all data/student_01
    ```
    This will run the full OCR and LLM analysis, creating `data/model_answers.json` and `data/insights.txt`. This step also creates the `storage` directory, which is the vector index for the chatbot.

#### Stage 2: Run the Baaz Bot Web App

1.  **Start the Flask Server:**

    ```bash
    flask run
    ```

    (This will use the `app.py` file)

2.  **Open the Chatbot:**
    Open your browser and navigate to **`http://127.0.0.1:5000`**. You can now chat with Baaz Bot\!

## 🔮 Project Roadmap

  * [✅] **Stage 1:** Initial prototype with plain text files.
  * [✅] **Stage 2:** Integrate OCR for typed-text images (Tesseract + OpenCV).
  * [⬜️] **Stage 3:** Implement advanced OCR for handwritten text using a cloud-based service like Google Cloud Vision API.

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

