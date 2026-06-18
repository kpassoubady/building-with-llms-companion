# User Story Generator

**Goal:** Build a tool that takes a brief feature idea and generates a structured agile user story.

**Requirements:**
1. Accept a brief feature description as input.
2. Use a system message that instructs the model to act as a Product Manager.
3. Output: Title, User Story format (As a... I want to... So that...), and 3-5 Acceptance Criteria.
4. Format the output clearly in Markdown.

## Instructions

1. Go to the `start/` directory and open `user_story_generator.py`.
2. Implement the `TODO`s by writing the prompt that instructs the LLM to format the response into a Markdown-formatted agile user story.
3. Run the application from your terminal:
   ```bash
   python exercises/ch04/user_story_generator/start/user_story_generator.py
   ```
4. Enter some feature ideas to see what the model generates.

## Getting Stuck?
If you need help or want to see the final working version, check the `solution/` directory.
