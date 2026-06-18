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

# TODO for each persona: replace the empty string with a system message that
#   clearly defines: (1) role/name, (2) audience, (3) tone, (4) scope,
#   and (5) at least one explicit "do NOT" constraint.

PERSONAS = [
    {
        "name": "Formal Legal Assistant",
        # TODO: Write a system message for a formal legal assistant.
        #   Tone: precise, professional, no contractions.
        #   Scope: legal documents, compliance, contracts only.
        #   Do NOT: give personal opinions or casual advice.
        "system_content": "",
    },
    {
        "name": "Casual Cooking Helper",
        # TODO: Write a system message for a casual cooking helper.
        #   Tone: warm, friendly, conversational - contractions encouraged.
        #   Scope: recipes, ingredients, cooking techniques only.
        #   Do NOT: answer questions unrelated to food and cooking.
        "system_content": "",
    },
    {
        "name": "Terse Senior Engineer",
        # TODO: Write a system message for a terse senior software engineer.
        #   Tone: direct, minimal prose, code-first where relevant.
        #   Scope: software engineering and programming only.
        #   Do NOT: add pleasantries, padding, or motivational language.
        "system_content": "",
    },
]


# ---------------------------------------------------------------------------
# Exercise function
# ---------------------------------------------------------------------------


def ask_persona(system_content: str, question: str) -> str:
    """Send a question to a persona defined by system_content.

    Args:
        system_content: The system message text for this persona.
        question: The user question to ask.

    Returns:
        The model's response as a string.
    """
    # TODO: Build a messages list with system_content as the system role
    #   and question as the user role. Call get_completion with tier="default"
    #   and temperature=0.7. Return the response string.
    raise NotImplementedError("Complete ask_persona() to continue.")


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
