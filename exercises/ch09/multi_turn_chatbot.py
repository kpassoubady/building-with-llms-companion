"""
Exercise: Multi-Turn Chatbot
Chapter 9: Conversation Design & Multi-turn Chat

Goal: Build a stateful chat loop that maintains message history so the
bot remembers the user's name and preferences across turns.

Skills practiced:
- Appending user and assistant messages to a shared history list
- Verifying that context persists across multiple API calls
- Designing a system message that defines persona and scope

Instructions:
1. Complete add_user_turn() to append a user message to history.
2. Complete add_assistant_turn() to append an assistant message to history.
3. Complete chat() to send the full history to the model and record the reply.
4. Run main() which drives a scripted 5-turn conversation.
5. Observe that turn 4 ("What's my name?") is answered correctly because
   the history carries context from turn 1.
6. Optional: replace the scripted loop with input() for a live session.

Run: python exercises/ch09/multi_turn_chatbot.py  (from the repo root)
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
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

    # Hint:
    # history.append({"role": "user", "content": text})

    raise NotImplementedError("Complete add_user_turn() to continue.")


def add_assistant_turn(history: list, text: str) -> None:
    """Append an assistant message dict to history in place.

    Args:
        history: The running message list (modified in place).
        text: The assistant's reply text.
    """
    # TODO: Append {"role": "assistant", "content": text} to history.

    # Hint:
    # history.append({"role": "assistant", "content": text})

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

    # Hint:
    # reply = get_completion(history, tier="mini", temperature=0.7)
    # add_assistant_turn(history, reply)
    # return reply

    raise NotImplementedError("Complete chat() to continue.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    print("=== Multi-Turn Chatbot ===\n")

    # Start history with the system message.
    history = [SYSTEM_MESSAGE]

    for i, user_text in enumerate(SCRIPTED_TURNS, start=1):
        print(f"Turn {i}")
        print(f"User:      {user_text}")
        add_user_turn(history, user_text)
        reply = chat(history)
        print(f"Assistant: {reply}\n")

    print(f"Total messages in history: {len(history)}")
    print("(system + user/assistant pairs = "
          f"1 + {len(SCRIPTED_TURNS)} x 2 = {1 + len(SCRIPTED_TURNS) * 2} expected)")


if __name__ == "__main__":
    main()


# Expected output (illustrative):
# === Multi-Turn Chatbot ===
#
# Turn 1
# User:      Hi! My name is Alex and I am a complete beginner.
# Assistant: Nice to meet you, Alex! ...
#
# Turn 4
# User:      What is my name and what did I say my experience level is?
# Assistant: Your name is Alex and you mentioned you are a complete beginner.
#
# Total messages in history: 11
# (system + user/assistant pairs = 1 + 5 x 2 = 11 expected)
