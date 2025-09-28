# main.py
import sys
import os
# Import the two new, separate functions
from src.task1_generate_model_ans import generate_model_answers, generate_insights
from src.task2_rag import start_chat_session

def main():
    """
    Main function to orchestrate the chatbot's workflow.
    Provides separate commands for each step of the generation process.
    """
    if len(sys.argv) < 2:
        print("Usage: python main.py [command]")
        print("Commands:")
        print("  generate-answers    - Step 1: Generates only the model answers.")
        print("  generate-insights   - Step 2: Generates only the student feedback insights.")
        print("  generate-all        - Runs both generation steps sequentially.")
        print("  chat                - Starts the interactive RAG chatbot.")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "generate-answers":
        generate_model_answers()
    elif command == "generate-insights":
        generate_insights()
    elif command == "generate-all":
        print("--- Running all generation steps ---")
        generate_model_answers()
        generate_insights()
        print("--- All generation steps complete ---")
    elif command == "chat":
        if not os.path.exists('data/insights.txt'):
            print("❌ Error: insights.txt not found.")
            print("Please run 'python main.py generate-insights' first.")
            sys.exit(1)
        start_chat_session()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()