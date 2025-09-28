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
    chat_engine = index.as_chat_engine(chat_mode='condense_plus_context')
    
    print("\n🎓 Smart Mentor Chatbot is ready!")
    print("Ask me questions about your answers, like 'Why did I lose marks in question 1?' or 'Explain photosynthesis in more detail.'")
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