# src/utils.py
import pytesseract
from PIL import Image
import cv2

# IMPORTANT FOR WINDOWS USERS:
# You may need to tell pytesseract where you installed Tesseract.
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image_for_ocr(image_path: str):
    """
    Loads an image and applies preprocessing steps to improve OCR accuracy.
    - Converts to grayscale
    - Applies thresholding to create a binary (black & white) image
    """
    # Read the image using OpenCV
    image = cv2.imread(image_path)
    
    # 1. Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 2. Apply thresholding to get a binary image
    # Otsu's thresholding automatically finds the optimal threshold value
    _, binary_image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    
    # Optional: Apply a median blur to remove noise
    binary_image = cv2.medianBlur(binary_image, 3)
    
    return binary_image

def extract_text_from_image(image_path: str) -> str:
    """
    Uses Tesseract OCR to extract text from an image file,
    applying preprocessing first to improve accuracy.
    """
    try:
        # Preprocess the image first
        preprocessed_image = preprocess_image_for_ocr(image_path)
        
        # Pass the preprocessed image directly to pytesseract
        text = pytesseract.image_to_string(preprocessed_image)
        return text
    except FileNotFoundError:
        print(f"Error: The file at {image_path} was not found.")
        return ""
    except Exception as e:
        print(f"An error occurred during OCR processing: {e}")
        return ""

    
# Parsing with LLM

import json
from src.llm_client import get_gemini_response

def parse_answers_with_llm(raw_text: str, questions: list) -> dict:
    """
    Uses an LLM to intelligently parse raw text into a structured dictionary of answers.

    Args:
        raw_text: The unstructured text from the OCR process.
        questions: The list of question objects from questions.json.

    Returns:
        A dictionary mapping question_id (as int) to the student's answer (as str).
    """
    print("🧠 Using LLM to intelligently parse student answers...")

    # Create a simple list of question numbers for the prompt
    question_numbers = [q['id'] for q in questions]

    # This is a powerful prompt designed specifically for parsing
    parsing_prompt = f"""
You are a text structuring expert. Your task is to analyze the raw, unstructured text from a student's answer sheet and map the answers to the correct question numbers.

**Instructions:**
1.  Read the provided "Raw Text from Answer Sheet".
2.  The official question numbers are: {question_numbers}.
3.  Your job is to intelligently associate the text with the correct question number.
4.  Structure your final output as a single, valid JSON object.
5.  If you cannot find an answer for a specific question, the value for that key should be "No answer provided".

**CRITICAL RULE:** You MUST NOT alter, correct, add to, or summarize the student's original text. Your only job is to copy the existing text verbatim into the correct JSON value. The integrity of the student's answer is paramount.

**Example Output Format:**
{{
  "1": "This is the complete answer for question 1...",
  "2": "This is the answer for question 2...",
  "3": "No answer provided"
}}

---
**Raw Text from Answer Sheet:**
"{raw_text}"
---

Now, provide the structured JSON object.
"""

    response_text = get_gemini_response(parsing_prompt)
        # --- ADD THIS BLOCK TO DEBUG ---
    print("\n" + "="*50)
    print("RAW LLM PARSER RESPONSE:")
    print(response_text)
    print("="*50 + "\n")
    # --- END DEBUG BLOCK ---

    try:
        # Clean up the response to ensure it's valid JSON
        # LLMs sometimes wrap JSON in ```json ... ```
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0]
        
        parsed_json = json.loads(response_text)
        
        # Convert string keys from JSON to integer keys for our dictionary
        parsed_answers = {int(k): v for k, v in parsed_json.items()}
        print("✅ LLM parsing successful.")
        return parsed_answers
    except (json.JSONDecodeError, IndexError, ValueError) as e:
        print(f"❌ Failed to parse LLM response as JSON: {e}")
        print(f"   LLM Response was: {response_text}")
        return {} # Return empty dictionary on failure