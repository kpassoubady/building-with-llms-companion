"""
Exercise: Temperature Lab
Chapter 7: API Parameters & Output Control

Goal: Generate marketing taglines for a product at five different temperature
settings and observe how diversity and determinism change with each value.

Skills practiced:
- Passing temperature to get_completion
- Using get_completion_full to inspect finish_reason
- Observing determinism (low temp) vs creativity (high temp)
- Formatting and comparing multi-run outputs

Instructions:
1. Implement generate_taglines() to call the API at a given temperature.
2. Run run_temperature_sweep() to generate taglines at all five temperatures.
3. Note which temperatures produce repetitive vs wildly varied outputs.
4. Try running the sweep twice and compare - which temperatures are stable?

Run: python solutions/ch07/temperature_lab.py  (from the repo root)
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

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
# Solution functions
# ---------------------------------------------------------------------------


def generate_taglines(temperature):
    """Call the LLM at the given temperature and return the response text.

    Args:
        temperature: Float between 0.0 and 2.0.

    Returns:
        Tuple of (response_text, finish_reason) strings.
    """
    response = get_completion_full(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_PROMPT},
        ],
        tier="mini",
        temperature=temperature,
        max_tokens=200,
    )
    return response.choices[0].message.content, response.choices[0].finish_reason


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
    run_temperature_sweep()
    observe_stability(runs=2)


if __name__ == "__main__":
    main()


# Expected output (illustrative):
# Chapter 7 - Temperature Lab
# Product: Byte Brew (a coffee shop that caters exclusively to software developers)
#
# --- temperature=0.0 (deterministic) ---
# 1. Fuel your code, one cup at a time.
# 2. Where great code meets great coffee.
# 3. Debug faster. Drink better.
#
# --- temperature=1.3 ---
# 1. Brew bold. Ship faster. Repeat.
# 2. Caffeine for coders, chaos for compilers.
# 3. From `null` to full - one sip.
#
# === Stability check: temperature 0.0 vs 1.3 ===
# temperature=0.0:
#   Run 1: 1. Fuel your code, one cup at a time.
#   Run 2: 1. Fuel your code, one cup at a time.   <- identical
