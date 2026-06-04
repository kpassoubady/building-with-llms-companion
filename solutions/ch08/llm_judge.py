"""
Exercise: LLM-as-Judge
Chapter 8: Prompt Iteration & Evaluation

Goal: Implement an LLM-as-judge evaluator that scores a candidate answer
1-5 against a rubric, then run it on three sample answers of varying quality.

Skills practiced:
- Designing a rubric-based scoring prompt
- Parsing a structured score from free-form model output
- Using tier="default" for quality-sensitive evaluation tasks

Instructions:
1. Read RUBRIC and the three entries in SAMPLE_ANSWERS.
2. Complete build_judge_prompt() to construct a prompt that asks the model
   to score the candidate answer 1-5 and give a one-sentence justification.
3. Complete parse_score() to extract the integer score from the response.
4. Complete judge() to call the model and return (score, justification).
5. Run main() and compare the three scores against your own intuition.

Run: python solutions/ch08/llm_judge.py  (from the repo root)
"""

import os
import sys
import re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from shared import get_completion

# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

QUESTION = (
    "What is the difference between a list and a tuple in Python?"
)

RUBRIC = (
    "Score 1-5 using these criteria: "
    "5 = accurate, covers mutability and typical use cases, concise; "
    "3 = mostly accurate but missing one key point; "
    "1 = inaccurate or completely off-topic."
)

SAMPLE_ANSWERS = [
    {
        "label": "weak",
        "answer": (
            "A list uses square brackets and a tuple uses parentheses. "
            "They are basically the same thing."
        ),
    },
    {
        "label": "partial",
        "answer": (
            "Lists are mutable, meaning you can change their contents after "
            "creation. Tuples are immutable. Both are ordered sequences."
        ),
    },
    {
        "label": "strong",
        "answer": (
            "Lists are mutable ordered sequences defined with square brackets; "
            "you can append, remove, or replace elements. "
            "Tuples are immutable ordered sequences defined with parentheses; "
            "once created their contents cannot change. "
            "Tuples are typically used for fixed records (coordinates, RGB "
            "values), while lists are used for collections that grow or shrink."
        ),
    },
]


# ---------------------------------------------------------------------------
# Solution functions
# ---------------------------------------------------------------------------


def build_judge_prompt(question: str, answer: str, rubric: str) -> str:
    """Return a prompt that asks the model to score the answer 1-5.

    The prompt instructs the model to reply with exactly:
      Score: <integer 1-5>
      Justification: <one sentence>

    Args:
        question: The original question posed to the answerer.
        answer: The candidate answer to evaluate.
        rubric: Scoring criteria string.

    Returns:
        A complete prompt string ready to send as a user message.
    """
    return (
        f"Question: {question}\n\n"
        f"Candidate answer: {answer}\n\n"
        f"Rubric: {rubric}\n\n"
        "Evaluate the candidate answer against the rubric and reply in "
        "exactly this format:\n"
        "Score: <integer 1-5>\n"
        "Justification: <one sentence explaining the score>"
    )


def parse_score(response: str) -> int:
    """Extract the integer score from the model's response.

    Looks for a pattern like "Score: 4" anywhere in the response.

    Args:
        response: Raw string returned by the model.

    Returns:
        Integer score 1-5, or 0 if no score is found.
    """
    match = re.search(r"Score:\s*([1-5])", response, re.IGNORECASE)
    return int(match.group(1)) if match else 0


def judge(question: str, answer: str, rubric: str):
    """Call the LLM judge and return (score, full_response).

    Args:
        question: The original question.
        answer: The candidate answer to score.
        rubric: Scoring criteria.

    Returns:
        Tuple of (score: int, response: str).
    """
    prompt = build_judge_prompt(question, answer, rubric)
    messages = [{"role": "user", "content": prompt}]
    response = get_completion(messages, tier="default", temperature=0.0)
    score = parse_score(response)
    return score, response


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    print("=== LLM-as-Judge ===\n")
    print(f"Question: {QUESTION}\n")
    print(f"Rubric: {RUBRIC}\n")
    print("-" * 60)

    for sample in SAMPLE_ANSWERS:
        score, response = judge(QUESTION, sample["answer"], RUBRIC)
        print(f"\nAnswer ({sample['label']}):\n  {sample['answer']}")
        print(f"\nJudge response:\n{response}")
        print(f"\nParsed score: {score}/5")
        print("-" * 60)


if __name__ == "__main__":
    main()


# Expected output (illustrative):
# === LLM-as-Judge ===
#
# Question: What is the difference between a list and a tuple in Python?
# Rubric: Score 1-5 ...
# ------------------------------------------------------------
#
# Answer (weak):
#   A list uses square brackets and a tuple uses parentheses. ...
# Judge response:
#   Score: 2
#   Justification: The answer correctly identifies syntax differences but
#   incorrectly states they are "basically the same thing," missing mutability.
# Parsed score: 2/5
# ------------------------------------------------------------
# Answer (strong):
#   ...
# Parsed score: 5/5
