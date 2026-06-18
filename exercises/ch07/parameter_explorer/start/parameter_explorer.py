import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from shared import get_completion_full

# ---------------------------------------------------------------------------
# Parameter defaults
# ---------------------------------------------------------------------------

DEFAULTS = {
    "temperature": 0.7,
    "top_p": 1.0,
    "max_tokens": 256,
    "stop": None,        # e.g. "." or "STOP" - leave blank for none
    "presence_penalty": 0.0,
    "frequency_penalty": 0.0,
    "seed": None,        # integer or blank for random
}

SYSTEM_PROMPT = "You are a helpful assistant. Answer clearly and concisely."

# ---------------------------------------------------------------------------
# Exercise functions
# ---------------------------------------------------------------------------


def parse_float(value, default):
    """Parse a float from user input, returning default if blank or invalid."""
    # TODO: Strip value; if empty return default. Otherwise try float(value).
    #   On ValueError, print a warning and return default.
    raise NotImplementedError("Implement parse_float()")


def parse_int_or_none(value, default):
    """Parse an int from user input, returning default if blank or invalid."""
    # TODO: Same pattern as parse_float but for int. Return None if value is
    #   blank AND default is None; return int(value) otherwise.
    raise NotImplementedError("Implement parse_int_or_none()")


def parse_stop(value):
    """Parse a comma-separated stop string into a list, or None if blank.

    Args:
        value: Raw input string, e.g. '.,!' or 'STOP,END' or ''.

    Returns:
        List of stop strings, or None.
    """
    # TODO: Strip value. If empty return None.
    #   Otherwise split on ',' and strip each token. Return the list.
    raise NotImplementedError("Implement parse_stop()")


def collect_parameters():
    """Prompt the user for each parameter value and return a params dict.

    Returns:
        Dict with keys matching DEFAULTS, values overridden by user input.
    """
    # TODO: For each key in DEFAULTS, call input() showing the key name and
    #   default value. Parse the input with the appropriate helper.
    #   Return the assembled dict.
    raise NotImplementedError("Implement collect_parameters()")


def run_with_parameters(user_prompt, params):
    """Send user_prompt to the LLM using the given parameter dict.

    Args:
        user_prompt: The user's question or instruction string.
        params: Dict from collect_parameters().

    Returns:
        Tuple of (response_text, usage_dict, finish_reason).
    """
    # TODO: Build kwargs from params, skipping None values.
    #   Call get_completion_full with SYSTEM_PROMPT, user_prompt, and all kwargs.
    #   Return (content, usage as dict, finish_reason).
    raise NotImplementedError("Implement run_with_parameters()")


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

    # params = collect_parameters()
    # print()
    # user_prompt = input("Your prompt: ").strip()
    # if not user_prompt:
    #     user_prompt = "Tell me something interesting about black holes."
    #     print(f"(Using default prompt: {user_prompt})")

    # print("\nSending request...")
    # response_text, usage, finish_reason = run_with_parameters(user_prompt, params)
    # print_summary(params, response_text, usage, finish_reason)


if __name__ == "__main__":
    main()
