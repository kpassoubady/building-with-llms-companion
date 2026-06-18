import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
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
        "question": "What is the name of the sorting algorithm with worst-case O(n log n) "
            "that uses a pivot element?",
        "expected_keywords": ["quicksort", "quick sort"],
        "note": "Slightly ambiguous - model may say merge sort instead.",
    },
    {
        "question": "What does the acronym REST stand for in RESTful APIs?",
        "expected_keywords": ["representational", "state", "transfer"],
        "note": "Common web development term.",
    },
    {
        "question": "According to the CAP theorem, a distributed system can guarantee "
            "at most how many of the three properties simultaneously?",
        "expected_keywords": ["two", "2"],
        "note": "Specific technical theorem - model may hedge or state incorrectly.",
    },
]


# ---------------------------------------------------------------------------
# Exercise functions
# ---------------------------------------------------------------------------


def ask_question(question: str) -> str:
    """Send a single factual question and return the model's answer."""
    messages = [
        {"role": "system",
         "content": "Answer factual questions concisely in 1-2 sentences. "
             "If you are not confident in the answer, say 'I don't know.'"},
        {"role": "user", "content": question},
    ]
    return get_completion(messages, tier="mini", temperature=0.0)


def check_answer(model_answer: str, expected_keywords: list[str]) -> bool:
    """Return True if all expected_keywords appear in model_answer."""
    lower = model_answer.lower()
    return any(kw.lower() in lower for kw in expected_keywords)


def run_audit(qa_pairs: list[dict]) -> None:
    """Run the full audit and print a report."""
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
