Baaz Bot: An AI-Powered Smart Mentor for Academic Feedback

Baaz Bot is a sophisticated, multi-stage chatbot designed to act as a personal AI mentor for students. It bridges the gap between receiving a grade and truly understanding the feedback by allowing students to have a natural conversation about their exam performance. The bot analyzes a student's answer script, compares it against model answers, and provides detailed, context-aware explanations for why marks were lost.

✨ Core Features

AI-Powered Feedback Generation: Uses a Large Language Model (LLM) to act as a subject matter expert, generating ideal "model answers" and creating detailed, constructive feedback by comparing them with the student's script.

RAG-Based Conversational AI: The generated feedback and model answers are used to build a knowledge base for a Retrieval-Augmented Generation (RAG) chatbot, ensuring all responses are grounded in the specific context of the student's evaluation.

OCR for Answer Script Digitization: Automatically extracts text from images of typed answer scripts using Tesseract OCR with OpenCV-powered image preprocessing for improved accuracy.

Conversational History: Maintains a unique conversation history for each user session, allowing the bot to understand follow-up questions and provide context-aware responses.

Real-time Streaming Interface: Features a modern web interface built with Flask, where the bot's responses are streamed character-by-character for a dynamic and engaging user experience.

Intelligent Persona: The bot is configured with a system prompt that allows it to answer both specific questions about the exam and general questions about its own purpose and capabilities.

🚀 Project Workflow

The project operates on a powerful two-tiered approach:

Phase 1: Data Generation & Indexing (main.py)

The system takes an exam's question paper (questions.json) and images of a student's answer script.

It uses an LLM (Gemini) to generate ideal, "gold-standard" model answers for each question.

It then uses the LLM again, this time acting as an expert evaluator, to compare the student's answers (extracted via OCR) with the model answers. This produces a detailed insights.txt file.

This insights.txt file becomes the knowledge base for the next phase.

Phase 2: Conversational Chat (app.py)

A RAG pipeline is created using the insights.txt file as its source of truth.

A Flask web server is launched, providing a user-friendly chat interface.

Students can ask questions like, "Why did I lose marks in question 2?" or "What key points did I miss for the deadlock question?", and the bot will use its knowledge base to provide specific, helpful answers.

🛠️ Technology Stack

Backend: Flask

AI & RAG: LlamaIndex, Google Generative AI (Gemini)

Vector Store & Embeddings: LlamaIndex (local storage), Hugging Face Transformers (bge-small-en-v1.5)

OCR: Tesseract, OpenCV, Pytesseract, Pillow

Frontend: HTML, CSS, JavaScript

Real-time Rendering: marked.js

📂 Project Structure

smart-mentor-chatbot/
├── app.py              # Main Flask web application
├── main.py             # Orchestrator script for data generation
├── requirements.txt    # Project dependencies
├── .env                # For API keys (not in repo)
├── data/
│   ├── questions.json
│   └── student_01/     # Example folder for student answer images
│       ├── page_01.png
│       └── ...
├── src/
│   ├── task1_generate_model_answers.py
│   ├── task2_build_rag.py
│   ├── llm_client.py
│   └── utils.py
├── static/
│   ├── css/style.css
│   ├── js/script.js
│   └── images/logo.png
└── templates/
    └── index.html


⚙️ Setup and Installation

Follow these steps to get the project running on your local machine.

1. Prerequisites

Python 3.9+

Tesseract OCR Engine

2. Clone the Repository

git clone [https://github.com/your-username/smart-mentor-chatbot.git](https://github.com/MohammedSameerWahab/baaz-bot.git)
cd baaz-bot


3. Install Tesseract OCR

You must install the Tesseract engine on your operating system.

Windows: Download and run the installer from the official Tesseract repository. After installation, you must configure the path in src/utils.py.

macOS: brew install tesseract

Linux (Debian/Ubuntu): sudo apt-get install tesseract-ocr

4. Create a Virtual Environment

# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate


5. Install Dependencies

pip install -r requirements.txt


6. Set Up Environment Variables

Create a file named .env in the root of the project and add your Google Generative AI API key:

GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"
FLASK_SECRET_KEY="a_random_secret_string_for_sessions"


7. Configure Tesseract Path (for Windows)

Open src/utils.py and update the pytesseract.pytesseract.tesseract_cmd line with the correct path to your Tesseract installation (e.g., r'C:\Program Files\Tesseract-OCR\tesseract.exe').

▶️ How to Run the Application

The application is run in two stages: first, you generate the analysis files, and second, you run the web app.

Stage 1: Generate Insights from an Answer Script

Prepare Data:

Add your exam questions to data/questions.json.

Place the images of the student's answer script in a dedicated folder, e.g., data/student_01/.

Run the Generation Script:
Execute the following command in your terminal. This will perform all the necessary steps: generating model answers, running OCR on the images, and creating the final insights.txt file.

python main.py generate-all data/student_01


This will create data/model_answers.json and data/insights.txt. It will also create a storage directory, which is the vector index for the RAG system.

Stage 2: Run the Baaz Bot Web App

Start the Flask Server:

flask run


Access the Chatbot:
Open your web browser and navigate to http://127.0.0.1:5000.

You can now start chatting with Baaz Bot!

🛣️ Future Work

Stage 3: Handwriting Recognition: The next major step is to move beyond typed text and integrate a more powerful OCR service (like Google Cloud Vision API) capable of accurately recognizing handwritten answers.

User Authentication: Add a user login system to manage and store evaluations for multiple students.

Database Integration: Store insights and chat histories in a database (e.g., PostgreSQL or MongoDB) instead of local files for better scalability.

🤝 Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

📄 License

This project is licensed under the MIT License.
