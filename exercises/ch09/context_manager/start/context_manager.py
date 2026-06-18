import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
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
# Exercise functions
# ---------------------------------------------------------------------------


def apply_full_history(system_msg: dict, conversation: list) -> list:
    """Return the complete message list: system message + all turns.

    Args:
        system_msg: The system message dict.
        conversation: All user/assistant message dicts.

    Returns:
        [system_msg] + conversation
    """
    # TODO: Return a list starting with system_msg followed by all items in
    #   conversation.
    raise NotImplementedError("Complete apply_full_history() to continue.")


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
    # TODO: Slice conversation to keep the last n*2 entries.
    #   Return [system_msg] + that slice.
    raise NotImplementedError("Complete apply_sliding_window() to continue.")


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
    # TODO:
    #   1. Split: old_turns = conversation[:-(keep_last_n * 2)]
    #             recent = conversation[-(keep_last_n * 2):]
    #   2. If old_turns is empty, return apply_full_history(system_msg, conversation).
    #   3. Build a summarisation prompt that contains the old turns as text.
    #   4. Call get_completion() with tier="mini" to get the summary.
    #   5. Return [system_msg, {"role": "assistant", "content": summary}] + recent.
    raise NotImplementedError("Complete apply_summary_strategy() to continue.")


def measure_tokens(messages: list) -> int:
    """Send messages to the model and return the prompt token count.

    Uses get_completion_full() to access response.usage.prompt_tokens.
    Sends a minimal user question to avoid adding many completion tokens.

    Args:
        messages: The trimmed message list (includes system + history).

    Returns:
        Number of prompt tokens reported by the API, or -1 if unavailable.
    """
    # TODO: Append a short probe question, call get_completion_full() with
    #   tier="mini", then return response.usage.prompt_tokens.
    #   Return -1 if response.usage is None.
    raise NotImplementedError("Complete measure_tokens() to continue.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    print("=== Context Manager: Strategy Comparison ===\n")
    print(f"Full conversation length: {len(CONVERSATION)} messages ({len(CONVERSATION) // 2} turns)\n")

    # strategies = [
    #     ("Full history", apply_full_history(SYSTEM_MSG, CONVERSATION)),
    #     (
    #         f"Sliding window (last {WINDOW_SIZE} turns)",
    #         apply_sliding_window(SYSTEM_MSG, CONVERSATION, WINDOW_SIZE),
    #     ),
    #     (
    #         f"Running summary (keep last {WINDOW_SIZE} turns)",
    #         apply_summary_strategy(SYSTEM_MSG, CONVERSATION, WINDOW_SIZE),
    #     ),
    # ]

    # print(f"{'Strategy':<40} {'Messages':>8} {'Prompt tokens':>14}")
    # print("-" * 65)

    # for label, messages in strategies:
    #     tokens = measure_tokens(messages)
    #     print(f"{label:<40} {len(messages):>8} {tokens:>14}")

    # print("\nObservation: sliding window drops the most messages; summary")
    # print("compresses old context into a single message at modest token cost.")


if __name__ == "__main__":
    main()
