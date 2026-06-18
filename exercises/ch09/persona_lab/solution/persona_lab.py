import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from shared import get_completion

# ---------------------------------------------------------------------------
# Questions asked to every persona
# ---------------------------------------------------------------------------

QUESTIONS = [
    "How do I handle an exception in Python?",
    "What should I eat for breakfast to stay focused?",
]

# ---------------------------------------------------------------------------
# Persona definitions
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
# Exercise function
# ---------------------------------------------------------------------------


def ask_persona(system_content: str, question: str) -> str:
    """Send a question to a persona defined by system_content."""
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

    # Validate that all personas have been configured.
    for persona in PERSONAS:
        if not persona["system_content"]:
            print(
                f"[!] '{persona['name']}' system_content is empty. "
                "Complete the TODO in PERSONAS before running."
            )
            sys.exit(1)

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
