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
    """Return the complete message list: system message + all turns."""
    return [system_msg] + conversation


def apply_sliding_window(system_msg: dict, conversation: list, n: int) -> list:
    """Return system message plus the last n*2 messages (n user/assistant pairs)."""
    return [system_msg] + conversation[-(n * 2):]


def apply_summary_strategy(
    system_msg: dict, conversation: list, keep_last_n: int
) -> list:
    """Summarise old turns and keep recent ones verbatim."""
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
    summary_msg = {"role": "assistant", "content": f"[Summary of earlier conversation]: {summary}"}
    return [system_msg, summary_msg] + recent


def measure_tokens(messages: list) -> int:
    """Send messages to the model and return the prompt token count."""
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
