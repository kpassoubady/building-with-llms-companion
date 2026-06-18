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
