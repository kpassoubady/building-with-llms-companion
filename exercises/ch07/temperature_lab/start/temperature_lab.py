import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from shared import get_completion_full

# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

PRODUCT_NAME = "Byte Brew"
PRODUCT_DESC = "a coffee shop that caters exclusively to software developers"

SYSTEM_PROMPT = "You are a creative copywriter for tech brands."

USER_PROMPT = (
    f"Generate 3 taglines for '{PRODUCT_NAME}', {PRODUCT_DESC}. "
    "Each tagline must be under 10 words. "
    "Return them as a numbered list."
)

TEMPERATURES = [0.0, 0.3, 0.7, 1.0, 1.3]

# ---------------------------------------------------------------------------
# Exercise functions
# ---------------------------------------------------------------------------


def generate_taglines(temperature):
    """Call the LLM at the given temperature and return the response text.

    Args:
        temperature: Float between 0.0 and 2.0.

    Returns:
        Tuple of (response_text, finish_reason) strings.
    """
    # TODO: Call get_completion_full with SYSTEM_PROMPT and USER_PROMPT at the
    #   given temperature. Use tier="mini", max_tokens=200.
    #   Return (response.choices[0].message.content, response.choices[0].finish_reason)
    raise NotImplementedError("Implement generate_taglines()")


def run_temperature_sweep():
    """Run tagline generation at every temperature in TEMPERATURES and print results."""
    print("Chapter 7 - Temperature Lab")
    print(f"Product: {PRODUCT_NAME} ({PRODUCT_DESC})\n")

    for temp in TEMPERATURES:
        print(f"--- temperature={temp} {'(deterministic)' if temp == 0.0 else ''} ---")
        text, finish_reason = generate_taglines(temp)
        print(text)
        if finish_reason != "stop":
            print(f"[finish_reason: {finish_reason}]")
        print()


def observe_stability(runs=2):
    """Run temperature 0.0 and 1.3 multiple times to compare stability.

    Args:
        runs: How many times to repeat each extreme.
    """
    print("=== Stability check: temperature 0.0 vs 1.3 ===\n")
    for temp in [0.0, 1.3]:
        print(f"temperature={temp}:")
        for run in range(1, runs + 1):
            text, _ = generate_taglines(temp)
            first_line = text.strip().splitlines()[0]
            print(f"  Run {run}: {first_line}")
        print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    # run_temperature_sweep()
    # observe_stability(runs=2)
    pass


if __name__ == "__main__":
    main()
