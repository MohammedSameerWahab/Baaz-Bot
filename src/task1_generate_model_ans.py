# src/task1_generate_model_answers.py
import json
import re
import time
import os
from src.llm_client import get_gemini_response
from src.utils import extract_text_from_image, parse_answers_with_llm
from pathlib import Path

# Define paths for clarity
QUESTIONS_FILE = 'data/questions.json'
MODEL_ANSWERS_FILE = 'data/model_answers.json'
INSIGHTS_FILE = 'data/insights.txt'


def generate_model_answers():
    """
    Generates a model answer for each question and saves them to a file.
    """
    print("🚀 Starting: Generating Model Answers...")

    with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
        questions = json.load(f)

    model_answers = []
    for q in questions:
        question_id = q['id']
        question_text = q['question']
        max_marks = q['max_marks']

        print(f"\n🧠 Generating model answer for Question {question_id}...")
        prompt_model_answer = f"""
You are a University Professor and Chief Examiner...
# (Your full prompt here)
**Question:** "{question_text}"
**Maximum Marks:** {max_marks}
"""
        model_answer_text = get_gemini_response(prompt_model_answer)
        model_answers.append({"question_id": question_id, "model_answer": model_answer_text})

        print("🕒 Waiting for 20 seconds before the next request...")
        time.sleep(20)

    # This block is correctly placed OUTSIDE the for loop
    with open(MODEL_ANSWERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(model_answers, f, indent=4)
    print(f"\n✅ Model answers saved to {MODEL_ANSWERS_FILE}")


def generate_insights(answer_dir: str):
    """
    Generates insights by processing all images in a given directory.
    """
    print(f"🚀 Starting: Generating Insights from directory: {answer_dir}")

    answer_path = Path(answer_dir)
    if not answer_path.is_dir():
        print(f"❌ Error: Directory not found at {answer_dir}")
        return

    if not os.path.exists(MODEL_ANSWERS_FILE):
        print(f"❌ Error: Model answers file not found at {MODEL_ANSWERS_FILE}")
        return

    # Step 1: OCR
    all_text = []
    image_files = sorted(list(answer_path.glob("*.png")) + list(answer_path.glob("*.jpg")))
    if not image_files:
        print(f"❌ No image files found in {answer_dir}. Aborting.")
        return

    print(f"📄 Found {len(image_files)} pages to process. Starting OCR...")
    for image_path in image_files:
        text = extract_text_from_image(str(image_path))
        all_text.append(text)
    student_answer_full_text = "\n\n--- Page Break ---\n\n".join(all_text)
    print("✅ All pages processed successfully via OCR.")
    
    # Step 2: Load Data
    with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
        questions = json.load(f)
    with open(MODEL_ANSWERS_FILE, 'r', encoding='utf-8') as f:
        model_answers_list = json.load(f)
    
    # Step 3: LLM Parsing
    parsed_answers = parse_answers_with_llm(student_answer_full_text, questions)
    if not parsed_answers:
        print("❌ Aborting insights generation due to parsing failure.")
        return

    model_answers_dict = {item['question_id']: item['model_answer'] for item in model_answers_list}

    # Step 4: Generate Insights for Each Question (The Loop)
    all_insights = []
    for q in questions:
        question_id = q['id']
        question_text = q['question']
        max_marks = q['max_marks']
        
        student_answer_for_q = parsed_answers.get(question_id, "No answer provided")
        model_answer_text = model_answers_dict.get(question_id, "Model answer not found.")

        if model_answer_text == "Model answer not found.":
            print(f"⚠️ Warning: Skipping Question {question_id} as no model answer was found.")
            continue

        print(f"\n 🕵️‍♀️ Generating insights for Question {question_id}...")
        prompt_analysis = f"""
You are an empathetic yet rigorous Teaching Assistant. Your primary goal is to help the student understand their mistakes and learn from them.
**Task:** Create a detailed, multi-part feedback report by comparing the student's answer to the model answer. This report will be the *only* document the student sees, so it must be self-contained, clear, and actionable. It will also be used as a knowledge base for a support chatbot, so a predictable, detailed structure is critical.
**Required Output Structure:**
### 1. Overall Summary
Provide a concise paragraph summarizing the student's grasp of the topic. Mention both strengths and the primary areas that need improvement.
### 2. Positive Points
Even if the answer is poor, identify at least one or two things the student did correctly or partially correctly. This encourages the student. (e.g., "The student correctly identified that a process is an executing program.")
### 3. Areas for Improvement (Detailed Breakdown)
This is the most important section. Iterate through every error, omission, or misconception. For each point, you **MUST** follow this exact format:
* **[Error Type, e.g., Conceptual Error/Omission/Vague Statement]:** The student wrote, "[Directly quote the student's incorrect phrase here]".
* **Correction:** Explain *why* it's wrong and what the correct concept is, referencing the model answer. Be specific.
**Example Format for a single point:**
* **Conceptual Error:** The student wrote, "a thread is a separate program."
* **Correction:** This is incorrect. A thread is not a separate program but the smallest unit of execution *within* a process. Threads of the same process share the same memory space, whereas separate programs (processes) do not.
### 4. Actionable Path to Improvement
Suggest concrete next steps for the student. For example: "To improve, the student should review the concepts of 'shared memory vs. separate memory spaces' and practice explaining the 'process state model'."
### 5. Estimated Score
Provide a numerical score and a brief, one-sentence justification that links back to the major issues identified in the breakdown.
---
**Question:** "{question_text}"
**Maximum Marks:** {max_marks}
**Model Answer:**
"{model_answer_text}"
**Student's Answer:**
"{student_answer_for_q}"
"""
        insight_text = get_gemini_response(prompt_analysis)
        
        formatted_insight = f"""
==================================================
Analysis for Question {question_id}: {question_text}
==================================================
{insight_text}
"""
        all_insights.append(formatted_insight)
        
        print("🕒 Waiting for 20 seconds before the next request...")
        time.sleep(20)

    # --- Step 5: Save the Final Insights File ---
    # This block is now correctly placed OUTSIDE and AFTER the for loop
    with open(INSIGHTS_FILE, 'w', encoding='utf-8') as f:
        f.write("".join(all_insights))
    print(f"\n✅ Analysis insights saved to {INSIGHTS_FILE}")