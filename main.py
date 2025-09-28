# main.py
import sys
import os
from src.task1_generate_model_ans import generate_model_answers, generate_insights
from src.task2_rag import start_chat_session

def main():
    """
    Main function to orchestrate the chatbot's workflow.
    Provides separate commands for each step of the generation process
    and handles directory paths for multi-image answers.
    """
    if len(sys.argv) < 2:
        print("\nUsage: python main.py [command]")
        print("\nCommands:")
        print("  generate-answers                  - Step 1: Generates only the model answers.")
        print("  generate-insights [path]          - Step 2: Generates insights from an answer directory.")
        print("  generate-all [path]               - Runs both generation steps sequentially.")
        print("  chat                              - Starts the interactive RAG chatbot.")
        print("\nExample for insights: python main.py generate-insights data/student_01")
        sys.exit(1)

    command = sys.argv[1].lower()

    # Create data directory if it doesn't exist to prevent errors
    os.makedirs('data', exist_ok=True)

    if command == "generate-answers":
        generate_model_answers()

    elif command == "generate-insights":
        if len(sys.argv) < 3:
            print("\n❌ Error: Please provide the path to the student's answer directory.")
            print("Usage: python main.py generate-insights path/to/answer_folder")
            sys.exit(1)
        answer_directory = sys.argv[2]
        generate_insights(answer_directory)

    elif command == "generate-all":
        if len(sys.argv) < 3:
            print("\n❌ Error: Please provide the path to the student's answer directory.")
            print("Usage: python main.py generate-all path/to/answer_folder")
            sys.exit(1)
        answer_directory = sys.argv[2]
        print("\n--- Running all generation steps ---")
        generate_model_answers()
        generate_insights(answer_directory)
        print("--- All generation steps complete ---\n")

    elif command == "chat":
        if not os.path.exists('data/insights.txt'):
            print("\n❌ Error: insights.txt not found.")
            print("Please run a 'generate' command first to create the analysis file.")
            sys.exit(1)
        start_chat_session()
        
    else:
        print(f"\n❌ Unknown command: {command}")
        print("See usage below:")
        # Re-print help text for clarity
        print("\nUsage: python main.py [command]")
        print("\nCommands:")
        print("  generate-answers                  - Step 1: Generates only the model answers.")
        print("  generate-insights [path]          - Step 2: Generates insights from an answer directory.")
        print("  generate-all [path]               - Runs both generation steps sequentially.")
        print("  chat                              - Starts the interactive RAG chatbot.")
        sys.exit(1)

if __name__ == "__main__":
    main()