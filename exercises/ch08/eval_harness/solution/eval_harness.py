import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from shared import get_completion

# ---------------------------------------------------------------------------
# Golden dataset
# ---------------------------------------------------------------------------

GOLDEN_DATASET = [
    {
        "input": "The app crashes when I click save",
        "expected_category": "bug_report",
    },
    {
        "input": "Can you add dark mode?",
        "expected_category": "feature_request",
    },
    {
        "input": "I was charged twice this month",
        "expected_category": "billing",
    },
    {
        "input": "How do I export my data?",
        "expected_category": "how_to",
    },
    {
        "input": "My account is locked and I cannot log in",
        "expected_category": "account",
    },
    {
        "input": "The search results are completely wrong every time",
        "expected_category": "bug_report",
    },
    {
        "input": "I would love a keyboard shortcut for the dashboard",
        "expected_category": "feature_request",
    },
    {
        "input": "Where can I find my invoice from last quarter?",
        "expected_category": "billing",
    },
    {
        "input": "",
        "expected_category": "unknown",
    },
    {
        "input": "Hmm, I am not sure, something feels off",
        "expected_category": "unknown",
    },
]

SYSTEM_PROMPT = (
    "Classify the support message into exactly one category: "
    "bug_report, feature_request, billing, how_to, account, unknown. "
    "Reply with the category label only. No punctuation, no explanation."
)


# ---------------------------------------------------------------------------
# Exercise functions
# ---------------------------------------------------------------------------


def score_response(response: str, expected_category: str) -> bool:
    """Return True if response contains the expected_category (case-insensitive)."""
    return expected_category.lower() in response.strip().lower()


def run_eval(prompt_fn, dataset=GOLDEN_DATASET):
    """Run prompt_fn against every entry in dataset and return results."""
    correct = 0
    failing_cases = []
    for entry in dataset:
        actual = prompt_fn(entry["input"])
        passed = score_response(actual, entry["expected_category"])
        if passed:
            correct += 1
        else:
            failing_cases.append({
                "input": entry["input"],
                "expected": entry["expected_category"],
                "actual": actual.strip(),
            })
    return correct / len(dataset), failing_cases


def classify(text: str) -> str:
    """Classify a single support message using SYSTEM_PROMPT."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": text if text else "(empty message)"},
    ]
    return get_completion(messages, tier="mini", temperature=0.0)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    print("=== Eval Harness ===\n")
    print(f"Dataset size: {len(GOLDEN_DATASET)} entries")
    print(f"System prompt: {SYSTEM_PROMPT}\n")
    print("Running evaluation...")

    pass_rate, failing = run_eval(classify)

    print(f"\nPass rate: {pass_rate:.0%} ({int(pass_rate * len(GOLDEN_DATASET))}/{len(GOLDEN_DATASET)})\n")

    if failing:
        print("Failing cases:")
        for case in failing:
            label = case["input"][:50] or "(empty)"
            print(f"  FAIL | expected={case['expected']!r:15} actual={case['actual']!r:15} | {label}")
    else:
        print("All cases passed.")


if __name__ == "__main__":
    main()
