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
    """Send a single factual question and return the model's answer.

    Args:
        question: The question string to ask.

    Returns:
        The model's answer as a string.
    """
    # TODO: Build a messages list where:
    #   - The system message instructs the model to answer factual questions
    #     concisely (1-2 sentences) and to say "I don't know" if uncertain.
    #   - The user message is the question.
    # Use tier="mini" and temperature=0.0 (deterministic answers).

    raise NotImplementedError("Complete ask_question() to continue.")


def check_answer(model_answer: str, expected_keywords: list[str]) -> bool:
    """Return True if all expected_keywords appear in model_answer.

    Matching is case-insensitive. Each keyword in expected_keywords is a
    phrase; the answer passes if ANY keyword phrase is found (OR logic).

    Args:
        model_answer: The string returned by the model.
        expected_keywords: A list of acceptable keyword phrases (OR logic).

    Returns:
        True if at least one keyword is found, False otherwise.
    """
    # TODO: Lowercase model_answer once, then check whether any of the
    # expected_keywords (also lowercased) appears as a substring.

    raise NotImplementedError("Complete check_answer() to continue.")


def run_audit(qa_pairs: list[dict]) -> None:
    """Run the full audit and print a report.

    Args:
        qa_pairs: The QUESTIONS_AND_ANSWERS list.
    """
    # TODO: Loop over qa_pairs, call ask_question() and check_answer() for each,
    # collect pass/fail results, print a row per question, then print overall
    # accuracy as a percentage at the end.

    raise NotImplementedError("Complete run_audit() to continue.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    print("=== Hallucination Audit ===\n")
    # TODO: call run_audit
    pass


if __name__ == "__main__":
    main()
