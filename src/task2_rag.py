# src/task2_build_rag.py

import os
from pathlib import Path  # NEW: Import for modern path handling
from dotenv import load_dotenv
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    Settings,
    StorageContext,
    load_index_from_storage,
)
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# Load environment variables
load_dotenv()

# --- NEW: Define constants for paths ---
DATA_DIR = Path("./data")
PERSIST_DIR = Path("./storage") # Directory to store the index

def setup_rag_system():
    """
    Sets up the RAG system by creating or loading a vector index.
    The index is built from the insights and model answers.
    """
    print("Setting up RAG system...")
    
    # Configure LLM (This stays the same)
    Settings.llm = Gemini(model_name="gemini-2.5-flash", api_key=os.getenv("GEMINI_API_KEY"))
    
    # Configure a local, open-source embedding model
    print("Using local embedding model: bge-small-en-v1.5")
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

    # --- UPDATED: Filesystem check using pathlib ---
    if not PERSIST_DIR.exists():
        print("Creating new index...")
        # LlamaIndex's SimpleDirectoryReader works directly with string paths
        documents = SimpleDirectoryReader(str(DATA_DIR)).load_data()
        
        # Create and persist the index
        index = VectorStoreIndex.from_documents(documents)
        # The persist method also works directly with string paths
        index.storage_context.persist(persist_dir=str(PERSIST_DIR))
        print(f"Index created and saved to {PERSIST_DIR}")
    else:
        print(f"Loading existing index from {PERSIST_DIR}...")
        # Load the existing index
        storage_context = StorageContext.from_defaults(persist_dir=str(PERSIST_DIR))
        index = load_index_from_storage(storage_context)
        print("Index loaded successfully.")
        
    return index

def start_chat_session():
    """
    Initializes the RAG system and starts an interactive chat loop.
    """
    index = setup_rag_system()

    system_prompt = (
        "You are Baaz Bot, a friendly and encouraging AI mentor. "
        "Your primary purpose is to help a student understand why they lost marks on their exam evaluation. "
        "You have been given a context document that contains a detailed analysis of their answers. "
        "Follow these rules:\n"
        "1. **For exam-related questions:** When the user asks about their performance, a specific question number (e.g., 'question 3'), or a concept "
        "mentioned in their evaluation, you MUST use the provided context to give a detailed and helpful answer.\n"
        "2. **For general questions:** If the user asks a general question about you (e.g., 'who are you?', 'what can you do?', 'what is your name?'), "
        "answer it based on your persona as Baaz Bot. Do NOT try to find the answer in the context for these questions.\n"
        "3. **For unrelated questions:** If a question is completely unrelated to the exam or your purpose (e.g., 'what is the capital of France?'), "
        "politely state that you can only help with questions about the student's evaluation.\n"
        "Always be supportive and encouraging in your tone."
    )
    
    # --- MODIFIED: Pass the system_prompt to the chat engine ---
    chat_engine = index.as_chat_engine(
        chat_mode='condense_plus_context',
        system_prompt=system_prompt
    )
    
    print("\n🎓 Smart Mentor Chatbot is ready!")
    print("Ask me questions about your answers")
    print("Type 'exit' to end the session.")

    while True:
        query = input("\nStudent: ")
        if query.lower() == 'exit':
            print("Goodbye! Keep learning. 👋")
            break
        if not query:
            continue
            
        response = chat_engine.chat(query)
        print(f"\nMentor: {response}")
