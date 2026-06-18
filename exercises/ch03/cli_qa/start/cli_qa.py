import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from shared import get_completion

SYSTEM_PROMPT = (
    "You are a helpful assistant. Answer questions clearly and concisely. "
    "If you do not know something, say so directly."
)

EXIT_COMMANDS = {"quit", "exit", "q", "bye"}


def ask(question: str) -> str:
    """Send `question` to the LLM and return the answer string.

    TODO: Implement this function.
      Build a messages list with the SYSTEM_PROMPT as a "system" message
      and the question as a "user" message. Call get_completion() with tier="mini".
    """
    raise NotImplementedError("Implement ask()")


def run_loop() -> None:
    """Read questions from stdin in a loop and print the LLM's answers.

    TODO: Implement this function.
    Loop structure:
      1. Print a prompt (e.g., "You: ").
      2. Read input() - strip whitespace.
      3. If empty, print a short nudge and continue.
      4. If input is in EXIT_COMMANDS, break.
      5. Call ask() and print the result labeled "Assistant:".
      6. Catch KeyboardInterrupt and EOFError to exit cleanly.
    """
    raise NotImplementedError("Implement run_loop()")


def main():
    print("CLI Q&A - interactive LLM session")
    print("Type your question and press Enter. Type 'quit' to exit.")
    print("-" * 50)

    # TODO: call run_loop()


if __name__ == "__main__":
    main()
