"""
Exercise: Context Manager
Chapter 9: Conversation Design & Multi-turn Chat

Goal: Implement three context strategies (full history, sliding window,
running summary) and compare their approximate token cost over a 10-turn
conversation.

Skills practiced:
- Truncating and windowing message history
- Requesting running summaries to compress old context
- Reading response.usage.prompt_tokens to measure real token cost

Instructions:
1. Read CONVERSATION - a pre-built 10-turn history used as input.
2. Complete apply_full_history() - returns the list unchanged.
3. Complete apply_sliding_window() - keeps system message plus last N turns.
4. Complete apply_summary_strategy() - calls the model to summarise old turns,
   then returns [system, summary_message] + last N turns verbatim.
5. Complete measure_tokens() - sends the trimmed history to the model,
   reads response.usage.prompt_tokens, and returns the count.
6. Run main() and compare the three token counts.

Run: python solutions/ch09/context_manager.py  (from the repo root)
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from shared import get_completion, get_completion_full

# ---------------------------------------------------------------------------
# Sample conversation (10 user/assistant turns, pre-built)
# ---------------------------------------------------------------------------

SYSTEM_MSG = {
    "role": "system",
    "content": (
        "You are a Python learning assistant. "
        "Answer Python questions clearly and concisely."
    ),
}

# A synthetic 10-turn conversation (user + assistant interleaved)
CONVERSATION = [
    {"role": "user", "content": "Hi, my name is Sam. I am learning Python."},
    {"role": "assistant", "content": "Hi Sam! Great choice. What would you like to learn first?"},
    {"role": "user", "content": "What are Python data types?"},
    {"role": "assistant", "content": "Python has int, float, str, bool, list, tuple, dict, and set."},
    {"role": "user", "content": "Can you show me an example of a dictionary?"},
    {"role": "assistant", "content": 'Sure: person = {"name": "Sam", "age": 30}'},
    {"role": "user", "content": "How do I loop over a dictionary?"},
    {"role": "assistant", "content": "Use: for key, value in person.items(): print(key, value)"},
    {"role": "user", "content": "What is a list comprehension?"},
    {"role": "assistant", "content": "It is a compact way to build a list: [x*2 for x in range(5)]"},
    {"role": "user", "content": "How is that different from a regular for loop?"},
    {"role": "assistant", "content": "A comprehension is one expression; a for loop can span many lines."},
    {"role": "user", "content": "What are lambda functions?"},
    {"role": "assistant", "content": "A lambda is an anonymous function: double = lambda x: x * 2"},
    {"role": "user", "content": "When should I prefer lambda over def?"},
    {"role": "assistant", "content": "Use lambda for short, throwaway functions passed to map/filter/sorted."},
    {"role": "user", "content": "What is my name?"},
    {"role": "assistant", "content": "Your name is Sam, as you mentioned at the start."},
]

WINDOW_SIZE = 4  # Number of most-recent turns (user+assistant pairs) to keep


# ---------------------------------------------------------------------------
# Solution functions
# ---------------------------------------------------------------------------


def apply_full_history(system_msg: dict, conversation: list) -> list:
    """Return the complete message list: system message + all turns.

    Args:
        system_msg: The system message dict.
        conversation: All user/assistant message dicts.

    Returns:
        [system_msg] + conversation
    """
    return [system_msg] + conversation


def apply_sliding_window(system_msg: dict, conversation: list, n: int) -> list:
    """Return system message plus the last n*2 messages (n user/assistant pairs).

    Older turns are dropped entirely.

    Args:
        system_msg: The system message dict.
        conversation: All user/assistant message dicts (pairs interleaved).
        n: Number of most-recent turns (pairs) to retain.

    Returns:
        [system_msg] + last n*2 messages from conversation.
    """
    return [system_msg] + conversation[-(n * 2):]


def apply_summary_strategy(
    system_msg: dict, conversation: list, keep_last_n: int
) -> list:
    """Summarise old turns and keep recent ones verbatim.

    1. Split conversation into old_turns (everything except the last
       keep_last_n*2 messages) and recent_turns (the last keep_last_n*2).
    2. If old_turns is non-empty, ask the model to summarise them in
       two sentences.
    3. Return [system_msg, summary_message] + recent_turns, where
       summary_message is {"role": "assistant", "content": <summary>}.

    Args:
        system_msg: The system message dict.
        conversation: All user/assistant message dicts.
        keep_last_n: Number of most-recent turns to keep verbatim.

    Returns:
        Trimmed message list with a summary replacing old turns.
    """
    old_turns = conversation[:-(keep_last_n * 2)]
    recent = conversation[-(keep_last_n * 2):]
    if not old_turns:
        return apply_full_history(system_msg, conversation)
    old_text = "\n".join(
        f"{m['role'].upper()}: {m['content']}" for m in old_turns
    )
    summary_prompt = (
        "Summarise this conversation in two sentences, keeping key facts "
        f"like the user's name and topics covered:\n\n{old_text}"
    )
    summary = get_completion(
        [{"role": "user", "content": summary_prompt}],
        tier="mini",
        temperature=0.3,
    )
    summary_msg = {
        "role": "assistant",
        "content": f"[Summary of earlier conversation]: {summary}",
    }
    return [system_msg, summary_msg] + recent


def measure_tokens(messages: list) -> int:
    """Send messages to the model and return the prompt token count.

    Uses get_completion_full() to access response.usage.prompt_tokens.
    Sends a minimal user question to avoid adding many completion tokens.

    Args:
        messages: The trimmed message list (includes system + history).

    Returns:
        Number of prompt tokens reported by the API, or -1 if unavailable.
    """
    probe = messages + [{"role": "user", "content": "What is my name?"}]
    response = get_completion_full(probe, tier="mini", temperature=0.0, max_tokens=10)
    if response.usage:
        return response.usage.prompt_tokens
    return -1


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    print("=== Context Manager: Strategy Comparison ===\n")
    print(f"Full conversation length: {len(CONVERSATION)} messages ({len(CONVERSATION) // 2} turns)\n")

    strategies = [
        ("Full history", apply_full_history(SYSTEM_MSG, CONVERSATION)),
        (
            f"Sliding window (last {WINDOW_SIZE} turns)",
            apply_sliding_window(SYSTEM_MSG, CONVERSATION, WINDOW_SIZE),
        ),
        (
            f"Running summary (keep last {WINDOW_SIZE} turns)",
            apply_summary_strategy(SYSTEM_MSG, CONVERSATION, WINDOW_SIZE),
        ),
    ]

    print(f"{'Strategy':<40} {'Messages':>8} {'Prompt tokens':>14}")
    print("-" * 65)

    for label, messages in strategies:
        tokens = measure_tokens(messages)
        print(f"{label:<40} {len(messages):>8} {tokens:>14}")

    print("\nObservation: sliding window drops the most messages; summary")
    print("compresses old context into a single message at modest token cost.")


if __name__ == "__main__":
    main()


# Expected output (illustrative):
# === Context Manager: Strategy Comparison ===
#
# Full conversation length: 20 messages (10 turns)
#
# Strategy                                  Messages  Prompt tokens
# -----------------------------------------------------------------
# Full history                                    21            412
# Sliding window (last 4 turns)                    9            210
# Running summary (keep last 4 turns)             10            235
#
# Observation: sliding window drops the most messages; summary
# compresses old context into a single message at modest token cost.
