"""
Exercise: CLI Q&A
Chapter 3: Working with LLM APIs

Goal: Build an interactive question-answering loop that reads questions from
stdin, sends each to the LLM, and prints the answer - demonstrating the
most basic form of human-in-the-loop interaction with an API.

Skills practiced:
- Reading user input with input() and handling edge cases
- Building a request-response loop with get_completion()
- Gracefully handling exit signals and empty input

Instructions:
1. Implement `ask()` to wrap get_completion() for a single question.
2. Implement `run_loop()` to read questions in a loop until the user types "quit".
3. Guard for empty input (skip the API call, prompt again).
4. Run the file and ask at least 3 questions. Type "quit" to exit.

Keyboard shortcuts that also stop the loop:
- Ctrl+C  (KeyboardInterrupt)
- Ctrl+D  (EOFError - end of piped input)

Run: python solutions/ch03/cli_qa.py  (from the repo root)
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from shared import get_completion

SYSTEM_PROMPT = (
    "You are a helpful assistant. Answer questions clearly and concisely. "
    "If you do not know something, say so directly."
)

EXIT_COMMANDS = {"quit", "exit", "q", "bye"}


def ask(question: str) -> str:
    """Send `question` to the LLM and return the answer string."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]
    return get_completion(messages, tier="mini")


def run_loop() -> None:
    """Read questions from stdin in a loop and print the LLM's answers."""
    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break
        if not user_input:
            print("(Please type a question, or 'quit' to exit.)")
            continue
        if user_input.lower() in EXIT_COMMANDS:
            print("Goodbye!")
            break
        answer = ask(user_input)
        print(f"\nAssistant: {answer}")


def main():
    print("CLI Q&A - interactive LLM session")
    print("Type your question and press Enter. Type 'quit' to exit.")
    print("-" * 50)

    run_loop()


if __name__ == "__main__":
    main()


# Expected output (illustrative):
#
# CLI Q&A - interactive LLM session
# Type your question and press Enter. Type 'quit' to exit.
# --------------------------------------------------
#
# You: What is a token in the context of LLMs?
#
# Assistant: A token is the basic unit of text that an LLM processes. It is
# roughly 3-4 characters on average for English text - common words like "the"
# or "is" are single tokens, while longer or rarer words may split into multiple
# tokens. LLMs are billed per token for both input and output.
#
# You: How many tokens is a typical paragraph?
#
# Assistant: A typical paragraph of 100-150 words contains roughly 130-200
# tokens in English.
#
# You: quit
# Goodbye!
