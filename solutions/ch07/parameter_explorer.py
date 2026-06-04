"""
Exercise: Parameter Explorer
Chapter 7: API Parameters & Output Control

Goal: Build an interactive tool that lets you set API parameters via prompts,
send a user message, and immediately see how the output changes.

Skills practiced:
- Reading and validating user input with sensible defaults
- Passing temperature, top_p, max_tokens, stop, presence_penalty,
  frequency_penalty, and seed to get_completion
- Observing the effect of each parameter on model output
- Using seed to reproduce identical outputs for comparison

Instructions:
1. Implement collect_parameters() to read each parameter from stdin.
2. Implement run_with_parameters() to call get_completion with those params.
3. Run main() and experiment: try seed=42 twice to see reproducibility.
4. Try stop=[".", "!"] to see how the response truncates.

Run: python solutions/ch07/parameter_explorer.py  (from the repo root)
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from shared import get_completion_full

# ---------------------------------------------------------------------------
# Parameter defaults
# ---------------------------------------------------------------------------

DEFAULTS = {
    "temperature": 0.7,
    "top_p": 1.0,
    "max_tokens": 256,
    "stop": None,           # e.g. "." or "STOP" - leave blank for none
    "presence_penalty": 0.0,
    "frequency_penalty": 0.0,
    "seed": None,           # integer or blank for random
}

SYSTEM_PROMPT = "You are a helpful assistant. Answer clearly and concisely."

# ---------------------------------------------------------------------------
# Solution functions
# ---------------------------------------------------------------------------


def parse_float(value, default):
    """Parse a float from user input, returning default if blank or invalid."""
    value = value.strip()
    if not value:
        return default
    try:
        return float(value)
    except ValueError:
        print(f"  Invalid float - using default {default}")
        return default


def parse_int_or_none(value, default):
    """Parse an int from user input, returning default if blank or invalid."""
    value = value.strip()
    if not value:
        return default
    try:
        return int(value)
    except ValueError:
        print(f"  Invalid integer - using default {default}")
        return default


def parse_stop(value):
    """Parse a comma-separated stop string into a list, or None if blank.

    Args:
        value: Raw input string, e.g. '.,!' or 'STOP,END' or ''.

    Returns:
        List of stop strings, or None.
    """
    value = value.strip()
    if not value:
        return None
    return [tok.strip() for tok in value.split(",") if tok.strip()]


def collect_parameters():
    """Prompt the user for each parameter value and return a params dict.

    Returns:
        Dict with keys matching DEFAULTS, values overridden by user input.
    """
    params = {}
    print("Press Enter to accept the default shown in brackets.\n")

    raw = input(f"  temperature [{DEFAULTS['temperature']}]: ")
    params["temperature"] = parse_float(raw, DEFAULTS["temperature"])

    raw = input(f"  top_p [{DEFAULTS['top_p']}]: ")
    params["top_p"] = parse_float(raw, DEFAULTS["top_p"])

    raw = input(f"  max_tokens [{DEFAULTS['max_tokens']}]: ")
    params["max_tokens"] = int(parse_float(raw, DEFAULTS["max_tokens"]))

    raw = input(f"  stop (comma-separated, blank=none) [{DEFAULTS['stop']}]: ")
    params["stop"] = parse_stop(raw)

    raw = input(f"  presence_penalty [{DEFAULTS['presence_penalty']}]: ")
    params["presence_penalty"] = parse_float(raw, DEFAULTS["presence_penalty"])

    raw = input(f"  frequency_penalty [{DEFAULTS['frequency_penalty']}]: ")
    params["frequency_penalty"] = parse_float(raw, DEFAULTS["frequency_penalty"])

    raw = input(f"  seed (integer, blank=random) [{DEFAULTS['seed']}]: ")
    params["seed"] = parse_int_or_none(raw, DEFAULTS["seed"])

    return params


def run_with_parameters(user_prompt, params):
    """Send user_prompt to the LLM using the given parameter dict.

    Args:
        user_prompt: The user's question or instruction string.
        params: Dict from collect_parameters().

    Returns:
        Tuple of (response_text, usage_dict, finish_reason).
    """
    kwargs = {k: v for k, v in params.items() if v is not None}
    response = get_completion_full(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        tier="mini",
        **kwargs,
    )
    content = response.choices[0].message.content
    usage = {
        "prompt_tokens": response.usage.prompt_tokens,
        "completion_tokens": response.usage.completion_tokens,
        "total_tokens": response.usage.total_tokens,
    }
    finish_reason = response.choices[0].finish_reason
    return content, usage, finish_reason


def print_summary(params, response_text, usage, finish_reason):
    """Print the active parameters and the model response."""
    print("\n" + "=" * 60)
    print("Active parameters:")
    for k, v in params.items():
        print(f"  {k:<20} {v}")
    print("-" * 60)
    print("Response:")
    print(response_text)
    print("-" * 60)
    print(f"Tokens used: {usage.get('total_tokens', '?')} "
          f"(prompt={usage.get('prompt_tokens', '?')}, "
          f"completion={usage.get('completion_tokens', '?')})")
    print(f"Finish reason: {finish_reason}")
    print("=" * 60)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    print("Chapter 7 - Parameter Explorer\n")
    print("Configure the API parameters, then send a prompt.\n")

    params = collect_parameters()
    print()
    user_prompt = input("Your prompt: ").strip()
    if not user_prompt:
        user_prompt = "Tell me something interesting about black holes."
        print(f"(Using default prompt: {user_prompt})")

    print("\nSending request...")
    response_text, usage, finish_reason = run_with_parameters(user_prompt, params)
    print_summary(params, response_text, usage, finish_reason)


if __name__ == "__main__":
    main()


# Expected output (illustrative):
# Chapter 7 - Parameter Explorer
#
# Configure the API parameters, then send a prompt.
#
# Press Enter to accept the default shown in brackets.
#   temperature [0.7]: 0.0
#   top_p [1.0]:
#   max_tokens [256]: 100
#   stop (comma-separated, blank=none) [None]: .
#   presence_penalty [0.0]:
#   frequency_penalty [0.0]:
#   seed (integer, blank=random) [None]: 42
#
# Your prompt: Explain recursion in one sentence.
#
# ============================================================
# Active parameters:
#   temperature          0.0
#   top_p                1.0
#   max_tokens           100
#   stop                 ['.']
#   presence_penalty     0.0
#   frequency_penalty    0.0
#   seed                 42
# ------------------------------------------------------------
# Response:
# Recursion is when a function calls itself to solve a smaller version of the same problem
# ------------------------------------------------------------
# Tokens used: 87 (prompt=28, completion=59)
# Finish reason: stop
# ============================================================
