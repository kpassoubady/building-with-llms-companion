"""
Lab 1.3: User Story Generator (Starter)
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from shared import get_completion

def generate_user_story(feature_idea):
    """
    Takes a brief feature idea and returns a structured agile user story.
    """
    # TODO: Define a strong system message that acts as a Product Manager.
    # It should instruct the model to output:
    # 1. Title
    # 2. User Story (As a... I want to... So that...)
    # 3. Acceptance Criteria (3-5 bullet points)
    # 4. Edge Cases (1-2 points)
    system_message = """
    """

    # TODO: Construct the messages array with the system message and user's feature_idea
    messages = [
        # ...
    ]

    # TODO: Call get_completion() with the messages.
    # Tip: What temperature should you use?
    response = ""

    return response

if __name__ == "__main__":
    print("--- User Story Generator ---")
    print("Enter a brief feature idea (e.g., 'Add a forgot password link to the login page').")
    print("Type 'quit' to exit.\n")
    
    while True:
        idea = input("Feature idea: ")
        if idea.lower() in ['quit', 'exit', 'q']:
            break
            
        if not idea.strip():
            continue
            
        print("\nGenerating user story...")
        story = generate_user_story(idea)
        print("\n" + "="*50)
        print(story)
        print("="*50 + "\n")
