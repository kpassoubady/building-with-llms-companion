import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from shared import get_completion

# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

SAMPLE_CODE = """
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
"""


# ---------------------------------------------------------------------------
# Exercise function
# ---------------------------------------------------------------------------


def explain_code(code: str) -> str:
    """Return a plain-English explanation of the given Python code snippet.

    Args:
        code: A string containing one or more Python functions.

    Returns:
        A string with the model's plain-English explanation.
    """
    # TODO: Build a messages list with two entries:
    #   1. A system message that sets the persona as a senior Python developer
    #      who explains code clearly to junior engineers.
    #   2. A user message asking the model to explain the code, with the code
    #      wrapped in a fenced code block.
    # Then call get_completion with tier="mini" and temperature=0.3.

    raise NotImplementedError("Complete explain_code() to continue.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    print("=== Code Explainer ===\n")
    print("Function under review:")
    print(SAMPLE_CODE)
    print("-" * 40)
    explanation = explain_code(SAMPLE_CODE)
    print("Explanation:")
    print(explanation)


if __name__ == "__main__":
    main()
