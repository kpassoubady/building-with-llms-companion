"""
Exercise: System Message Lab
Chapter 5: Prompt Engineering Fundamentals

Goal: Send the same user message with 5 different system messages and observe
how dramatically the system message changes the tone, structure, and depth of
the response.

Skills practiced:
- Understanding the system message as a persistent persona and rule layer
- Seeing the effect of role, tone, and format constraints on output
- Designing system messages for different audiences and use cases

Instructions:
1. Read USER_MESSAGE - this never changes across the 5 calls.
2. Read SYSTEM_MESSAGES - each entry defines a different persona/constraint.
3. Complete call_with_system() to send the combined system+user message.
4. Run the file and compare the 5 responses printed in order.
5. Write a 6th system message of your own (e.g. "sarcastic critic" or
   "haiku poet") and add it to SYSTEM_MESSAGES.

Run: python exercises/ch05/system_message_lab.py  (from the repo root)
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
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
    """Send a chat completion with the given system and user messages.

    Args:
        system_message: The content for the system role message.
        user_message: The content for the user role message.

    Returns:
        The model's response as a string.
    """
    # TODO: Build a messages list with a system message and a user message,
    # then call get_completion with tier="mini" and temperature=0.5.

    # Hint:
    # messages = [
    #     {"role": "system", "content": system_message},
    #     {"role": "user", "content": user_message},
    # ]
    # return get_completion(messages, tier="mini", temperature=0.5)

    raise NotImplementedError("Complete call_with_system() to continue.")


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


# Expected output (illustrative):
# === System Message Lab ===
#
# User message (constant): What is a database index and when should I use one?
#
# ------------------------------------------------------------
# System persona: Terse expert
# ------------------------------------------------------------
# - Speeds up SELECT queries on large tables.
# - Use on columns in WHERE, JOIN, ORDER BY.
# - Avoid on small tables or write-heavy columns.
#
# ------------------------------------------------------------
# System persona: Friendly tutor
# ------------------------------------------------------------
# Think of a book's index at the back. Instead of reading every page,
# you jump straight to the topic. A database index works the same way -
# it lets the database skip most rows and find your data fast. Use one
# on columns you search or sort by often.
#
# ------------------------------------------------------------
# System persona: JSON only
# ------------------------------------------------------------
# {"definition": "A data structure that speeds up row lookups on a column",
#  "when_to_use": ["Columns in WHERE clauses", "Foreign key columns"],
#  "when_to_avoid": ["Tables with under 1000 rows"]}
#
# (... two more personas follow ...)
