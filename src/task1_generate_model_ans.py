# src/task1_generate_model_answers.py
import json
import re
import time
import os
from src.llm_client import get_gemini_response

# Define paths for clarity
QUESTIONS_FILE = 'data/questions.json'
STUDENT_ANSWER_FILE = 'data/student_answer.txt'
MODEL_ANSWERS_FILE = 'data/model_answers.json'
INSIGHTS_FILE = 'data/insights.txt'

# NEW FUNCTION: Generates only the model answers
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
You are a University Professor and Chief Examiner for a Computer Science course. Your task is to create a gold-standard model answer suitable for a university-level examination.

**Goal:** The answer must be exemplary, serving as the ultimate reference for grading. It should be comprehensive, accurate, and exceptionally clear.

**Formatting and Structural Requirements:**
1.  **Introduction:** Start with a concise, direct definition or introduction of the main topic.
2.  **Structured Body:** Use Markdown headings (`###`) to separate distinct parts of the answer (e.g., "### Key Differences", "### Advantages of Threads").
3.  **Use Lists:** For enumerating points, advantages, disadvantages, or characteristics, use bulleted or numbered lists.
4.  **Bold Key Terms:** Enclose all critical terminology in bold Markdown (`**key term**`). This is essential for emphasis and clarity.
5.  **Conclusion:** End with a brief concluding paragraph that summarizes the most crucial points.

**Question:** "{question_text}"
**Maximum Marks:** {max_marks}
"""
        model_answer_text = get_gemini_response(prompt_model_answer)
        model_answers.append({"question_id": question_id, "model_answer": model_answer_text})

        print("🕒 Waiting for 20 seconds before the next request...")
        time.sleep(20)

    with open(MODEL_ANSWERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(model_answers, f, indent=4)
    print(f"\n✅ Model answers saved to {MODEL_ANSWERS_FILE}")

# NEW FUNCTION: Generates only the insights, using existing model answers
def generate_insights():
    """
    Generates insights by comparing student answers to pre-generated model answers.
    """
    print("🚀 Starting: Generating Insights...")

    # Check if model answers file exists
    if not os.path.exists(MODEL_ANSWERS_FILE):
        print(f"❌ Error: Model answers file not found at {MODEL_ANSWERS_FILE}")
        print("Please run the 'generate-answers' command first.")
        return

    # Load all necessary data
    with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
        questions = json.load(f)
    with open(MODEL_ANSWERS_FILE, 'r', encoding='utf-8') as f:
        model_answers_list = json.load(f)
    with open(STUDENT_ANSWER_FILE, 'r', encoding='utf-8') as f:
        student_answer_full_text = f.read()

    # Convert model answers list to a lookup dictionary for easy access
    model_answers_dict = {item['question_id']: item['model_answer'] for item in model_answers_list}

    # Parse student answers
    parsed_answers = {}
    answer_blocks = re.split(r'Question (\d+):', student_answer_full_text)
    if len(answer_blocks) > 1:
        for i in range(1, len(answer_blocks), 2):
            parsed_answers[int(answer_blocks[i])] = answer_blocks[i+1].strip()
    print("✅ Student answers parsed successfully.")

    all_insights = []
    for q in questions:
        question_id = q['id']
        question_text = q['question']
        max_marks = q['max_marks']
        
        student_answer_for_q = parsed_answers.get(question_id, "No answer found.")
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

    with open(INSIGHTS_FILE, 'w', encoding='utf-8') as f:
        f.write("".join(all_insights))
    print(f"\n✅ Analysis insights saved to {INSIGHTS_FILE}")