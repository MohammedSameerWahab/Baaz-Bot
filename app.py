# app.py
import os
import time
import json
from flask import Flask, render_template, request, Response, session, jsonify
from src.task2_rag import setup_rag_system
from llama_index.core.llms import ChatMessage

# --- Flask App Initialization ---
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "a_very_secret_key_for_baaz_bot")

# --- Global variable for the RAG Index ---
rag_index = None

# --- NEW: Define the custom system prompt as a global constant ---
SYSTEM_PROMPT = (
    "You are Baaz Bot, a friendly and encouraging AI mentor. "
    "Your primary purpose is to help a student understand why they lost marks on their exam evaluation. "
    "You have been given a context document that contains a detailed analysis of their answers. "
    "Follow these rules:\n"
    "1. For exam-related questions: When the user asks about their performance, a specific question number (e.g., 'question 3'), or a concept "
    "mentioned in their evaluation, you MUST use the provided context to give a detailed and helpful answer.\n"
    "2. For general questions: If the user asks a general question about you (e.g., 'who are you?', 'what can you do?', 'what is your name?'), "
    "answer it based on your persona as Baaz Bot. Do NOT try to find the answer in the context for these questions.\n"
    "3. For unrelated questions: If a question is completely unrelated to the exam or your purpose (e.g., 'what is the capital of France?'), "
    "politely state that you can only help with questions about the student's evaluation.\n"
    "Always be supportive and encouraging in your tone."
)

def initialize_rag_system():
    global rag_index
    if rag_index is None:
        print("="*50)
        print("🚀 Initializing RAG Index for the first time...")
        rag_index = setup_rag_system()
        print("✅ RAG Index initialized successfully!")
        print("="*50)

# --- Routes ---

@app.before_request
def before_first_request_func():
    initialize_rag_system()

@app.route("/")
def index():
    session.clear()
    return render_template("index.html")

@app.route("/new_chat", methods=["POST"])
def new_chat():
    session.clear()
    return jsonify({"status": "success", "message": "New chat session started."})

@app.route("/stream_ask")
def stream_ask():
    user_message = request.args.get("message", "")
    if not user_message:
        return Response("Error: Message cannot be empty.", status=400)

    chat_history_dicts = session.get("chat_history", [])
    chat_history = [ChatMessage.parse_obj(msg) for msg in chat_history_dicts]
    
    # --- MODIFIED: Pass the system_prompt to the chat engine ---
    chat_engine = rag_index.as_chat_engine(
        chat_history=chat_history,
        chat_mode='condense_plus_context',
        system_prompt=SYSTEM_PROMPT  # <-- The fix is applied here
    )
    
    # ... (The rest of the function remains the same) ...
    
    streaming_response = chat_engine.stream_chat(user_message)
    
    full_response_text = "".join(list(streaming_response.response_gen))
    
    session["chat_history"] = [msg.model_dump() for msg in chat_engine.chat_history]
    
    def stream_characters(text):
        for char in text:
            sse_data = f"data: {json.dumps({'token': char})}\n\n"
            yield sse_data
            time.sleep(0.01)

    return Response(stream_characters(full_response_text), mimetype='text/event-stream')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')