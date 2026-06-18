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
    """Stream the assistant reply token by token and return the full text.

    Args:
        messages: Full conversation history including the latest user message.

    Returns:
        The complete assistant reply as a string.
    """
    # TODO: Call litellm.completion with stream=True using get_model(tier="mini").
    #   Iterate over the response stream. For each chunk, extract the delta content
    #   and print it with end="", flush=True so tokens appear immediately.
    #   After the loop, print a newline and return the accumulated full text.
    raise NotImplementedError("Implement stream_response()")


def chat_loop():
    """Run an interactive terminal chat loop with streaming output."""
    # TODO: Initialize the conversation history with SYSTEM_MESSAGE.
    #   Loop: read user input, skip blank lines, exit on EXIT_COMMANDS.
    #   Append the user message to history, call stream_response(),
    #   append the assistant reply to history, and repeat.
    raise NotImplementedError("Implement chat_loop()")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    print("Chapter 7 - Streaming Chat\n")
    # chat_loop()


if __name__ == "__main__":
    main()
