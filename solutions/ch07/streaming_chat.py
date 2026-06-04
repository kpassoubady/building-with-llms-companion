"""
Exercise: Streaming Chat
Chapter 7: API Parameters & Output Control

Goal: Build a terminal chat loop that prints tokens as they arrive using
litellm streaming, and maintains conversation history across turns.

Skills practiced:
- Using litellm.completion(..., stream=True) for token-by-token output
- Maintaining a growing messages list for multi-turn context
- Detecting and handling stream end and error conditions
- Graceful exit on 'quit' or 'exit' command

Instructions:
1. Implement stream_response() to iterate chunks and print tokens as they arrive.
2. Implement chat_loop() to manage history and call stream_response() per turn.
3. Run the file, type a message, and watch tokens stream in real time.
4. Type 'quit' to exit. Notice how the assistant remembers earlier turns.

Run: python solutions/ch07/streaming_chat.py  (from the repo root)
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

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
# Solution functions
# ---------------------------------------------------------------------------


def stream_response(messages):
    """Stream the assistant reply token by token and return the full text.

    Args:
        messages: Full conversation history including the latest user message.

    Returns:
        The complete assistant reply as a string.
    """
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


# Expected output (illustrative):
# Chapter 7 - Streaming Chat
#
# Chat started. Type 'quit' to exit.
#
# You: What is a stack overflow?
# Assistant: A stack overflow occurs when the call stack...  <- tokens stream in
#
# You: Give me a Python example.
# Assistant: Sure! Here is a classic recursive example...   <- context preserved
#
# You: quit
# Goodbye!
