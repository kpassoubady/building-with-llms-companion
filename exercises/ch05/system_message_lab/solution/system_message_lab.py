import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from shared import get_completion

# ---------------------------------------------------------------------------
# Sample data - the user message stays constant for every call
# ---------------------------------------------------------------------------

USER_MESSAGE = (
    "What is a database index and when should I use one?"
)

# Five system messages - same user question, five different experiences.
SYSTEM_MESSAGES = [
    {
        "label": "Terse expert",
        "system": (
            "You are a senior database engineer. "
            "Answer in 3 bullet points, no more than 10 words each. "
            "Use technical terms without defining them."
        ),
    },
    {
        "label": "Friendly tutor",
        "system": (
            "You are a patient coding tutor explaining concepts to a beginner. "
            "Use an analogy to a real-world object. "
            "Keep the total answer under 100 words."
        ),
    },
    {
        "label": "JSON only",
        "system": (
            "Respond with ONLY valid JSON. No prose before or after. "
            "Use this structure exactly:\n"
            '{"definition": "string", "when_to_use": ["reason1", "reason2"], '
            '"when_to_avoid": ["reason1"]}'
        ),
    },
    {
        "label": "Strict reviewer",
        "system": (
            "You are a skeptical code reviewer. "
            "List the three most common mistakes developers make with this topic. "
            "Be direct and critical. "
            "Format as a numbered list."
        ),
    },
    {
        "label": "ELI5 (explain like I am 5)",
        "system": (
            "Explain everything as if talking to a 5-year-old. "
            "Use very simple words and a short story or toy example. "
            "No technical terms at all."
        ),
    },
]


# ---------------------------------------------------------------------------
# Exercise function
# ---------------------------------------------------------------------------


def call_with_system(system_message: str, user_message: str) -> str:
    """Send a chat completion with the given system and user messages."""
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ]
    return get_completion(messages, tier="mini", temperature=0.5)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    print("=== System Message Lab ===")
    print(f"\nUser message (constant): {USER_MESSAGE}\n")
    separator = "-" * 60

    for entry in SYSTEM_MESSAGES:
        print(separator)
        print(f"System persona: {entry['label']}")
        print(separator)
        response = call_with_system(entry["system"], USER_MESSAGE)
        print(response)
        print()


if __name__ == "__main__":
    main()
