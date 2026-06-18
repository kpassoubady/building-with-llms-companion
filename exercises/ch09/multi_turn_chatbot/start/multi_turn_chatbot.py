import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from shared import get_completion

# ---------------------------------------------------------------------------
# Persona / system message
# ---------------------------------------------------------------------------

SYSTEM_MESSAGE = {
    "role": "system",
    "content": (
        "You are a friendly Python learning assistant. "
        "Help users learn Python clearly and concisely. "
        "Remember facts the user tells you (name, experience level, goals). "
        "Do not answer questions unrelated to Python programming."
    ),
}

# Scripted turns for the demo - replace with input() for a live session.
SCRIPTED_TURNS = [
    "Hi! My name is Alex and I am a complete beginner.",
    "What is the difference between a list and a tuple?",
    "I prefer short answers - no more than three sentences.",
    "What is my name and what did I say my experience level is?",
    "Thanks! One more: how do I check the length of a list?",
]


# ---------------------------------------------------------------------------
# Exercise functions
# ---------------------------------------------------------------------------


def add_user_turn(history: list, text: str) -> None:
    """Append a user message dict to history in place.

    Args:
        history: The running message list (modified in place).
        text: The user's message text.
    """
    # TODO: Append {"role": "user", "content": text} to history.
    raise NotImplementedError("Complete add_user_turn() to continue.")


def add_assistant_turn(history: list, text: str) -> None:
    """Append an assistant message dict to history in place.

    Args:
        history: The running message list (modified in place).
        text: The assistant's reply text.
    """
    # TODO: Append {"role": "assistant", "content": text} to history.
    raise NotImplementedError("Complete add_assistant_turn() to continue.")


def chat(history: list) -> str:
    """Send the full history to the model and return the reply string.

    Also appends the assistant reply to history so the caller does not
    have to call add_assistant_turn separately.

    Args:
        history: The running message list including the latest user turn.

    Returns:
        The assistant's reply as a string.
    """
    # TODO: Call get_completion(history, tier="mini", temperature=0.7),
    #   append the reply with add_assistant_turn(), then return the reply.
    raise NotImplementedError("Complete chat() to continue.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    print("=== Multi-Turn Chatbot ===\n")

    # Start history with the system message.
    history = [SYSTEM_MESSAGE]

    # for i, user_text in enumerate(SCRIPTED_TURNS, start=1):
    #     print(f"Turn {i}")
    #     print(f"User:      {user_text}")
    #     add_user_turn(history, user_text)
    #     reply = chat(history)
    #     print(f"Assistant: {reply}\n")

    # print(f"Total messages in history: {len(history)}")
    # print("(system + user/assistant pairs = "
    #       f"1 + {len(SCRIPTED_TURNS)} x 2 = {1 + len(SCRIPTED_TURNS) * 2} expected)")


if __name__ == "__main__":
    main()
