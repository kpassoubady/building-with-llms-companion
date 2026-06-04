"""
Exercise: Hallucination Audit
Chapter 4: Model Capabilities & Limitations

Goal: Ask the model 10 factual questions with known correct answers, check
each response against the expected answer, and report an accuracy score.
Demonstrates why fact-critical outputs require external verification.

Skills practiced:
- Identifying hallucination-prone question types
- Programmatic answer validation (substring / keyword matching)
- Interpreting accuracy results as a capability signal

Instructions:
1. Read QUESTIONS_AND_ANSWERS. Each entry has "question", "expected_keywords",
   and a "note" explaining why it is tricky for LLMs.
2. Complete ask_question() to send one question and return the model's answer.
3. Complete check_answer() to return True when ALL expected_keywords appear
   (case-insensitive) in the model's answer.
4. Run the file. Note which categories the model gets wrong most often.
5. Add two questions of your own (one easy, one hard) and re-run.

Run: python solutions/ch04/hallucination_audit.py  (from the repo root)
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from shared import get_completion

# ---------------------------------------------------------------------------
# Sample data - 10 factual questions with known answers
# ---------------------------------------------------------------------------

QUESTIONS_AND_ANSWERS = [
    {
        "question": "What programming language was Python named after?",
        "expected_keywords": ["monty python", "comedy"],
        "note": "Well-known fact, model should know this reliably.",
    },
    {
        "question": "What does HTTP stand for?",
        "expected_keywords": ["hypertext", "transfer", "protocol"],
        "note": "Common acronym, high-reliability.",
    },
    {
        "question": "In what year was the first iPhone released?",
        "expected_keywords": ["2007"],
        "note": "Specific date, model usually knows this.",
    },
    {
        "question": "What is the time complexity of binary search?",
        "expected_keywords": ["o(log n)", "log n"],
        "note": "CS fundamentals, model should answer correctly.",
    },
    {
        "question": "What is the capital of Australia?",
        "expected_keywords": ["canberra"],
        "note": "Common misconception trap - many people (and models) say Sydney.",
    },
    {
        "question": "How many bits are in a byte?",
        "expected_keywords": ["8"],
        "note": "Fundamental computing fact.",
    },
    {
        "question": "What is the output of print(type([])) in Python?",
        "expected_keywords": ["<class 'list'>", "list"],
        "note": "Python fact, verifiable - good test of code knowledge.",
    },
    {
        "question": (
            "What is the name of the sorting algorithm with worst-case O(n log n) "
            "that uses a pivot element?"
        ),
        "expected_keywords": ["quicksort", "quick sort"],
        "note": "Slightly ambiguous - model may say merge sort instead.",
    },
    {
        "question": "What does the acronym REST stand for in RESTful APIs?",
        "expected_keywords": ["representational", "state", "transfer"],
        "note": "Common web development term.",
    },
    {
        "question": (
            "According to the CAP theorem, a distributed system can guarantee "
            "at most how many of the three properties simultaneously?"
        ),
        "expected_keywords": ["two", "2"],
        "note": "Specific technical theorem - model may hedge or state incorrectly.",
    },
]


# ---------------------------------------------------------------------------
# Solution
# ---------------------------------------------------------------------------


def ask_question(question: str) -> str:
    """Send a single factual question and return the model's answer.

    Args:
        question: The question string to ask.

    Returns:
        The model's answer as a string.
    """
    messages = [
        {
            "role": "system",
            "content": (
                "Answer factual questions concisely in 1-2 sentences. "
                "If you are not confident in the answer, say 'I don't know.'"
            ),
        },
        {"role": "user", "content": question},
    ]
    return get_completion(messages, tier="mini", temperature=0.0)


def check_answer(model_answer: str, expected_keywords: list[str]) -> bool:
    """Return True if any expected_keywords appear in model_answer.

    Matching is case-insensitive. The answer passes if ANY keyword phrase
    is found (OR logic).

    Args:
        model_answer: The string returned by the model.
        expected_keywords: A list of acceptable keyword phrases (OR logic).

    Returns:
        True if at least one keyword is found, False otherwise.
    """
    lower = model_answer.lower()
    return any(kw.lower() in lower for kw in expected_keywords)


def run_audit(qa_pairs: list[dict]) -> None:
    """Run the full audit and print a report.

    Args:
        qa_pairs: The QUESTIONS_AND_ANSWERS list.
    """
    correct = 0
    for i, qa in enumerate(qa_pairs, 1):
        answer = ask_question(qa["question"])
        passed = check_answer(answer, qa["expected_keywords"])
        correct += passed
        status = "PASS" if passed else "FAIL"
        print(f"Q{i:02d} [{status}] {qa['question'][:60]}")
        if not passed:
            print(f"       Expected keywords: {qa['expected_keywords']}")
            print(f"       Model said: {answer[:100]}")
    accuracy = correct / len(qa_pairs) * 100
    print(f"\nAccuracy: {correct}/{len(qa_pairs)} = {accuracy:.0f}%")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    print("=== Hallucination Audit ===\n")
    run_audit(QUESTIONS_AND_ANSWERS)


if __name__ == "__main__":
    main()


# Expected output (illustrative):
# === Hallucination Audit ===
#
# Q01 [PASS] What programming language was Python named after?
# Q02 [PASS] What does HTTP stand for?
# Q03 [PASS] In what year was the first iPhone released?
# Q04 [PASS] What is the time complexity of binary search?
# Q05 [FAIL] What is the capital of Australia?
#        Expected keywords: ['canberra']
#        Model said: The capital of Australia is Sydney...
# Q06 [PASS] How many bits are in a byte?
# Q07 [PASS] What is the output of print(type([])) in Python?
# Q08 [PASS] What is the name of the sorting algorithm with worst-case O(n...
# Q09 [PASS] What does the acronym REST stand for in RESTful APIs?
# Q10 [PASS] According to the CAP theorem, a distributed system can guaran...
#
# Accuracy: 9/10 = 90%
