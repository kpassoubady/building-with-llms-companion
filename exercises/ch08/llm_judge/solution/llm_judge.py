import os
import sys
import re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
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
# Exercise functions
# ---------------------------------------------------------------------------


def build_judge_prompt(question: str, answer: str, rubric: str) -> str:
    """Return a prompt that asks the model to score the answer 1-5."""
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
    """Extract the integer score from the model's response."""
    match = re.search(r"Score:\s*([1-5])", response, re.IGNORECASE)
    return int(match.group(1)) if match else 0


def judge(question: str, answer: str, rubric: str):
    """Call the LLM judge and return (score, full_response)."""
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
