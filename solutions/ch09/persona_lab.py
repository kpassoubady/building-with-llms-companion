"""
Exercise: Persona Lab
Chapter 9: Conversation Design & Multi-turn Chat

Goal: Define three distinct personas via system messages, send each the
same two questions, and compare how tone, vocabulary, and depth differ.

Skills practiced:
- Writing system messages that define persona, scope, and tone
- Observing how system message phrasing shapes model behaviour
- Identifying what to include (and exclude) in a persona definition

Reference solution. Each persona in PERSONAS has a 'name' and a complete
'system_content'. ask_persona() builds the message list and calls the model.
Run main() to read the contrasting responses side by side.

Run: python solutions/ch09/persona_lab.py  (from the repo root)
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from shared import get_completion

# ---------------------------------------------------------------------------
# Questions asked to every persona
# ---------------------------------------------------------------------------

QUESTIONS = [
    "How do I handle an exception in Python?",
    "What should I eat for breakfast to stay focused?",
]

# ---------------------------------------------------------------------------
# Persona definitions (solutions filled in)
# ---------------------------------------------------------------------------

PERSONAS = [
    {
        "name": "Formal Legal Assistant",
        "system_content": (
            "You are a formal legal research assistant. "
            "You assist legal professionals with questions about contracts, "
            "compliance, and legal documents. "
            "Use precise, professional language. Do not use contractions. "
            "Do not provide casual advice or personal opinions. "
            "If a question is outside legal topics, politely decline and "
            "redirect the user to the appropriate professional."
        ),
    },
    {
        "name": "Casual Cooking Helper",
        "system_content": (
            "You're a casual, friendly cooking helper who loves sharing "
            "kitchen tips and easy recipes. "
            "Keep your tone warm and conversational - use contractions freely. "
            "Only answer questions about food, recipes, and cooking techniques. "
            "If someone asks about anything else, cheerfully say that's outside "
            "your specialty and offer to help with a recipe instead."
        ),
    },
    {
        "name": "Terse Senior Engineer",
        "system_content": (
            "You are a terse senior software engineer. "
            "Give direct, minimal answers. Lead with code when applicable. "
            "No pleasantries, no padding, no motivational language. "
            "Only answer software engineering and programming questions. "
            "For anything else, say: 'Out of scope.'"
        ),
    },
]


# ---------------------------------------------------------------------------
# Solution function
# ---------------------------------------------------------------------------


def ask_persona(system_content: str, question: str) -> str:
    """Send a question to a persona defined by system_content.

    Args:
        system_content: The system message text for this persona.
        question: The user question to ask.

    Returns:
        The model's response as a string.
    """
    messages = [
        {"role": "system", "content": system_content},
        {"role": "user", "content": question},
    ]
    return get_completion(messages, tier="default", temperature=0.7)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    print("=== Persona Lab ===\n")

    for question in QUESTIONS:
        print(f"Question: {question}")
        print("=" * 60)
        for persona in PERSONAS:
            response = ask_persona(persona["system_content"], question)
            print(f"\n[{persona['name']}]")
            print(response)
        print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    main()


# Expected output (illustrative):
# === Persona Lab ===
#
# Question: How do I handle an exception in Python?
# ============================================================
#
# [Formal Legal Assistant]
# That question pertains to software development and falls outside the
# scope of legal research. I recommend consulting a qualified software
# engineer or technical documentation for guidance on that matter.
#
# [Casual Cooking Helper]
# Ooh, that's more of a coding question - not really my kitchen territory!
# But if you want, I can help you handle a tricky recipe instead. :)
#
# [Terse Senior Engineer]
# try:
#     risky_call()
# except ValueError as e:
#     handle(e)
# Use specific exception types. Never bare except.
# ============================================================
