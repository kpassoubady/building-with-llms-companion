import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from shared import get_completion

# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

BAD_PROMPTS = [
    {
        "topic": "Code review",
        "bad_prompt": "Make my code better",
        "anti_pattern": "No instruction verb, no context, no input, no format.",
    },
    {
        "topic": "Microservices advice",
        "bad_prompt": "Don't you think microservices are better than monoliths?",
        "anti_pattern": "Leading question that anchors the model to one view.",
    },
    {
        "topic": "Error explanation",
        "bad_prompt": "Be brief but explain everything in detail",
        "anti_pattern": "Conflicting constraints - brief AND detailed is contradictory.",
    },
    {
        "topic": "Log analysis",
        "bad_prompt": "Logs",
        "anti_pattern": "Single-word prompt with no instruction, context, or format.",
    },
    {
        "topic": "SQL query help",
        "bad_prompt": "Write a query and also explain it and optimise it and show indexes",
        "anti_pattern": "Multiple unrelated tasks in one prompt with no structure.",
    },
]

REWRITES = [
    # Topic: Code review
    "You are a senior Python developer. Review the following code snippet and identify potential issues. Return a numbered list of issues with a one-line fix for each.\n\nCode:\n```python\ndef add(a, b):\n    return a + b\n```",

    # Topic: Microservices advice
    "You are a software architect advising a 5-person startup. Create a pros/cons table comparing monoliths and microservices. The table should have the following columns: Approach, Pros, Cons, Best For.",

    # Topic: Error explanation
    "You are a technical mentor to a junior engineer. Explain the concept of a StackOverflowError in exactly 5 bullet points, one sentence each.",

    # Topic: Log analysis
    "Classify the following log lines. Return a markdown table with columns: Timestamp, Level, and Message.\n\n---\n2023-10-01 12:00:00 INFO User logged in\n2023-10-01 12:05:00 ERROR Database connection failed\n---",

    # Topic: SQL query help
    "You are a database administrator. Write a SQL query to select all users who signed up in the last 30 days. Format the query in a sql code block, followed by a 2-sentence explanation."
]


# ---------------------------------------------------------------------------
# Exercise function
# ---------------------------------------------------------------------------


def run_comparison(bad_prompt: str, rewritten_prompt: str, topic: str) -> None:
    """Call the model with both prompts and print results side-by-side."""
    bad_response = get_completion(
        [{"role": "user", "content": bad_prompt}], tier="mini"
    )
    good_response = get_completion(
        [{"role": "user", "content": rewritten_prompt}], tier="mini"
    )
    separator = "=" * 60
    print(f"\n{separator}")
    print(f"Topic: {topic}")
    print(f"{separator}")
    print(f"BEFORE:\n{bad_response[:300]}")
    print(f"\nAFTER:\n{good_response[:300]}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    print("=== Prompt Rewriter ===\n")
    for item, rewritten in zip(BAD_PROMPTS, REWRITES):
        if rewritten is None:
            print(f"[SKIP] '{item['bad_prompt']}' - fill in REWRITES first.")
            continue
        run_comparison(item["bad_prompt"], rewritten, item["topic"])


if __name__ == "__main__":
    main()
