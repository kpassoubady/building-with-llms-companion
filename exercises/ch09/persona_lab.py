"""
Exercise: Persona Lab
Chapter 9: Conversation Design & Multi-turn Chat

Goal: Define three distinct personas via system messages, send each the
same two questions, and compare how tone, vocabulary, and depth differ.

Skills practiced:
- Writing system messages that define persona, scope, and tone
- Observing how system message phrasing shapes model behaviour
- Identifying what to include (and exclude) in a persona definition

Instructions:
1. Read the three entries in PERSONAS. Each has a 'name' and a stub
   'system_content' that you must complete.
2. Complete the system_content for all three personas following the
   guidance in the TODO comments.
3. Complete ask_persona() to build the message list and call the model.
4. Run main() and read the contrasting responses side by side.
5. Optional: add a fourth persona of your own design.

Run: python exercises/ch09/persona_lab.py  (from the repo root)
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
        #
        # Hint:
        # "system_content": (
        #     "You are a formal legal research assistant. "
        #     "You assist legal professionals with questions about contracts, "
        #     "compliance, and legal documents. "
        #     "Use precise, professional language. Do not use contractions. "
        #     "Do not provide casual advice or personal opinions. "
        #     "If a question is outside legal topics, politely decline and "
        #     "redirect the user to the appropriate professional."
        # ),
        "system_content": "",
    },
    {
        "name": "Casual Cooking Helper",
        # TODO: Write a system message for a casual cooking helper.
        #   Tone: warm, friendly, conversational - contractions encouraged.
        #   Scope: recipes, ingredients, cooking techniques only.
        #   Do NOT: answer questions unrelated to food and cooking.
        #
        # Hint:
        # "system_content": (
        #     "You're a casual, friendly cooking helper who loves sharing "
        #     "kitchen tips and easy recipes. "
        #     "Keep your tone warm and conversational - use contractions freely. "
        #     "Only answer questions about food, recipes, and cooking techniques. "
        #     "If someone asks about anything else, cheerfully say that's outside "
        #     "your specialty and offer to help with a recipe instead."
        # ),
        "system_content": "",
    },
    {
        "name": "Terse Senior Engineer",
        # TODO: Write a system message for a terse senior software engineer.
        #   Tone: direct, minimal prose, code-first where relevant.
        #   Scope: software engineering and programming only.
        #   Do NOT: add pleasantries, padding, or motivational language.
        #
        # Hint:
        # "system_content": (
        #     "You are a terse senior software engineer. "
        #     "Give direct, minimal answers. Lead with code when applicable. "
        #     "No pleasantries, no padding, no motivational language. "
        #     "Only answer software engineering and programming questions. "
        #     "For anything else, say: 'Out of scope.'"
        # ),
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

    # Hint:
    # messages = [
    #     {"role": "system", "content": system_content},
    #     {"role": "user", "content": question},
    # ]
    # return get_completion(messages, tier="default", temperature=0.7)

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
