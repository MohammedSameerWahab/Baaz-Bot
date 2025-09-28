# src/llm_client.py
import os
import time 
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def get_gemini_response(prompt: str) -> str:
    """
    Sends a prompt to the Gemini API and returns the response.
    Includes a retry mechanism with exponential backoff for reliability.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")
        
    genai.configure(api_key=api_key)
    
    generation_config = {
        "temperature": 0.0,
        "max_output_tokens": 4096, # Increased token limit for detailed answers
    }

    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash", # Sticking with gemini-pro for high-quality text generation
        generation_config=generation_config,
    )

    # --- NEW: Retry Logic ---
    max_retries = 3
    delay = 5  # Initial delay in seconds
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"An error occurred: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2  # Exponential backoff
            else:
                print("Max retries reached. Returning empty string.")
                return "" # Return empty if all retries fail