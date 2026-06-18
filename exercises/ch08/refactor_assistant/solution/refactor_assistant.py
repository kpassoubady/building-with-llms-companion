import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from shared import get_completion

# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

SAMPLE_CODE = """
def calc(items):
    t = 0
    for i in items:
        t = t + i['price'] * i['qty']
    return t
"""

# v1: the original vague prompt - produces an output but has clear failures:
#   - no mention of keeping tests passing
#   - does not specify Python (model might switch style/language)
#   - response may be very long with unasked-for explanation
INITIAL_PROMPT = (
    "Refactor this code to be cleaner."
)


# ---------------------------------------------------------------------------
# Exercise functions
# ---------------------------------------------------------------------------


def build_prompt_v2(code: str) -> str:
    """Return a prompt that adds the 'keep existing tests passing' constraint."""
    return (
        "Refactor this code to be cleaner. "
        "The function name and signature must stay the same so existing "
        "tests keep passing."
    )


def build_prompt_v3(code: str) -> str:
    """Return a prompt that also pins the language to Python 3."""
    return (
        "Refactor this Python 3 function to follow PEP 8 naming conventions "
        "and add type hints for parameters and the return value. "
        "The function name and signature must stay the same so existing "
        "tests keep passing."
    )


def build_prompt_v4(code: str) -> str:
    """Return a prompt that constrains verbosity to code-only output."""
    return (
        "Refactor this Python 3 function to follow PEP 8 naming conventions "
        "and add type hints for parameters and the return value. "
        "The function name and signature must stay the same so existing "
        "tests keep passing. "
        "Reply with a fenced ```python code block only. No explanation."
    )


def call_refactor(prompt: str, code: str) -> str:
    """Send the refactoring request to the model and return the response."""
    messages = [
        {"role": "user", "content": f"{prompt}\n\n```python\n{code}\n```"},
    ]
    return get_completion(messages, tier="mini", temperature=0.2)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    print("=== Refactor Assistant: Prompt Iteration ===\n")

    versions = [
        ("v1 (vague)", INITIAL_PROMPT),
        ("v2 (+ tests constraint)", build_prompt_v2(SAMPLE_CODE)),
        ("v3 (+ language/type hints)", build_prompt_v3(SAMPLE_CODE)),
        ("v4 (+ code-only output)", build_prompt_v4(SAMPLE_CODE)),
    ]

    for label, prompt in versions:
        print(f"--- {label} ---")
        print(f"Prompt: {prompt}\n")
        response = call_refactor(prompt, SAMPLE_CODE)
        print(f"Response:\n{response}\n")
        print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
