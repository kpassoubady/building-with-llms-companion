"""
Lab 1.3: User Story Generator (Solution)
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from shared import get_completion

def generate_user_story(feature_idea):
    """
    Takes a brief feature idea and returns a structured agile user story.
    """
    system_message = """You are an experienced Agile Product Manager.
Convert feature ideas into well-structured user stories.

For each feature idea, provide:
1. **Title**: A clear, concise title
2. **User Story**: "As a [user], I want to [action] so that [benefit]"
3. **Acceptance Criteria**: A bulleted list of 3-5 testable criteria
4. **Edge Cases**: 1-2 edge cases to consider

Use Markdown formatting. Be professional and thorough."""

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": feature_idea}
    ]

    # Temperature 0.2-0.5 is good for structured but slightly creative text
    response = get_completion(
        messages=messages,
        temperature=0.3
    )

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
