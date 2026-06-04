"""
Exercise: Refactor Assistant
Chapter 8: Prompt Iteration & Evaluation

Goal: Practise the prompt iteration loop by refining a vague refactoring
prompt three times, each time fixing a single observed failure.

Skills practiced:
- Identifying specific prompt failures and writing targeted fixes
- Comparing v1/v2/v3 outputs to see measurable improvement
- Using tier="mini" for rapid iteration

Instructions:
1. Read INITIAL_PROMPT and understand why it is too vague.
2. Complete build_prompt_v2() by adding the missing constraint (tests).
3. Complete build_prompt_v3() by specifying the target language explicitly.
4. Complete build_prompt_v4() by adding a length/format constraint.
5. Run main() and read each version's output to observe improvement.
6. Optional: add a v5 that incorporates all your fixes in one prompt.

Run: python exercises/ch08/refactor_assistant.py  (from the repo root)
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
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
    """Return a prompt that adds the 'keep existing tests passing' constraint.

    Fix applied: v1 never mentioned tests, so the model felt free to change
    the function signature or rename it. Add one sentence about tests.

    Returns:
        A prompt string with the tests constraint added.
    """
    # TODO: Start from INITIAL_PROMPT and append a sentence that tells the
    #   model it must not break existing tests (same function name/signature).

    # Hint:
    # return (
    #     "Refactor this code to be cleaner. "
    #     "The function name and signature must stay the same so existing "
    #     "tests keep passing."
    # )

    raise NotImplementedError("Complete build_prompt_v2() to continue.")


def build_prompt_v3(code: str) -> str:
    """Return a prompt that also pins the language to Python 3.

    Fix applied: v2 still produced a JavaScript-flavoured variable name style
    on some runs. Add an explicit language constraint.

    Returns:
        A prompt string with language and tests constraints.
    """
    # TODO: Extend v2's prompt by specifying Python 3 style (PEP 8 names,
    #   type hints for parameters and return value).

    # Hint:
    # return (
    #     "Refactor this Python 3 function to follow PEP 8 naming conventions "
    #     "and add type hints for parameters and the return value. "
    #     "The function name and signature must stay the same so existing "
    #     "tests keep passing."
    # )

    raise NotImplementedError("Complete build_prompt_v3() to continue.")


def build_prompt_v4(code: str) -> str:
    """Return a prompt that constrains verbosity to code-only output.

    Fix applied: v3 returned a long explanation alongside the code. Ask for
    code only inside a fenced block, no prose.

    Returns:
        A prompt string with language, tests, and format constraints.
    """
    # TODO: Extend v3's prompt by asking for a fenced Python code block only,
    #   with no surrounding explanation.

    # Hint:
    # return (
    #     "Refactor this Python 3 function to follow PEP 8 naming conventions "
    #     "and add type hints for parameters and the return value. "
    #     "The function name and signature must stay the same so existing "
    #     "tests keep passing. "
    #     "Reply with a fenced ```python code block only. No explanation."
    # )

    raise NotImplementedError("Complete build_prompt_v4() to continue.")


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


# Expected output (illustrative):
# === Refactor Assistant: Prompt Iteration ===
#
# --- v1 (vague) ---
# Prompt: Refactor this code to be cleaner.
# Response:
# Here's a cleaner version of your code:
# def calc(items):
#     return sum(item['price'] * item['qty'] for item in items)
# (no type hints, function renamed in some runs, long explanation)
#
# --- v4 (+ code-only output) ---
# Prompt: Refactor this Python 3 function ...
# Response:
# ```python
# def calc(items: list[dict]) -> float:
#     return sum(item["price"] * item["qty"] for item in items)
# ```
