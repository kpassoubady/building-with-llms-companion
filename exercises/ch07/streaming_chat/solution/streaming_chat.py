import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

import litellm
from shared import get_model

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SYSTEM_MESSAGE = {
    "role": "system",
    "content": (
        "You are a helpful assistant for software developers. "
        "Keep responses concise unless asked for detail."
    ),
}

EXIT_COMMANDS = {"quit", "exit", "q"}

# ---------------------------------------------------------------------------
# Exercise functions
# ---------------------------------------------------------------------------


def stream_response(messages):
    """Stream the assistant reply token by token and return the full text."""
    model = get_model(tier="mini")
    response = litellm.completion(
        model=model,
        messages=messages,
        stream=True,
        temperature=0.7,
        max_tokens=512,
    )
    full_text = ""
    for chunk in response:
        delta = chunk.choices[0].delta.content
        if delta:
            print(delta, end="", flush=True)
            full_text += delta
    print()
    return full_text


def chat_loop():
    """Run an interactive terminal chat loop with streaming output."""
    history = [SYSTEM_MESSAGE]
    print("Chat started. Type 'quit' to exit.\n")
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break
        if not user_input:
            continue
        if user_input.lower() in EXIT_COMMANDS:
            print("Goodbye!")
            break
        history.append({"role": "user", "content": user_input})
        print("Assistant: ", end="", flush=True)
        reply = stream_response(history)
        history.append({"role": "assistant", "content": reply})


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    print("Chapter 7 - Streaming Chat\n")
    chat_loop()


if __name__ == "__main__":
    main()
