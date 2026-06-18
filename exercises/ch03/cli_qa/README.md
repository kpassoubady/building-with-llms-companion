# Exercise: CLI Q&A

**Chapter 3: Working with LLM APIs**

**Goal:** Build an interactive question-answering loop that reads questions from stdin, sends each to the LLM, and prints the answer - demonstrating the most basic form of human-in-the-loop interaction with an API.

**Skills practiced:**
- Reading user input with `input()` and handling edge cases
- Building a request-response loop with `get_completion()`
- Gracefully handling exit signals and empty input

## Instructions

1. Go to the `start/` directory and open `cli_qa.py`.
2. Implement `ask()` to wrap `get_completion()` for a single question.
3. Implement `run_loop()` to read questions in a loop until the user types "quit".
4. Guard for empty input (skip the API call, prompt again).
5. Run the file and ask at least 3 questions. Type "quit" to exit.
   ```bash
   python exercises/ch03/cli_qa/start/cli_qa.py
   ```

Keyboard shortcuts that also stop the loop:
- `Ctrl+C`  (KeyboardInterrupt)
- `Ctrl+D`  (EOFError - end of piped input)

## Getting Stuck?
If you need help, check the `solution/` directory for the completed, working code.
