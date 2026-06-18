import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

# Pricing: USD per 1,000,000 tokens (as of mid-2025 - verify against provider docs)
PRICING = {
    "gpt-4o": {"input": 2.50, "output": 10.00, "provider": "OpenAI"},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60, "provider": "OpenAI"},
    "claude-sonnet": {"input": 3.00, "output": 15.00, "provider": "Anthropic"},
    "gemini-flash": {"input": 0.10, "output": 0.40, "provider": "Google"},
}

# Sample workload: a realistic production API call
SAMPLE_CALL = {
    "prompt": "Summarize this quarterly earnings report and extract key metrics.",
    "input_tokens": 1_200,
    "output_tokens": 350,
}

# Daily workload assumption from Chapter 2 exercise
DAILY_CALLS = 5_000
DAILY_AVG_INPUT = 800   # tokens per call
DAILY_AVG_OUTPUT = 400  # tokens per call


def compute_cost(input_tokens: int, output_tokens: int, model: str) -> float:
    """Return the USD cost for one API call with the given token counts.

    TODO: Implement this function.
      1. Look up the per-million rates from PRICING[model].
      2. Compute: cost = (input_tokens * input_rate + output_tokens * output_rate) / 1_000_000
      3. Return the float cost.

    Raises KeyError if model is not in PRICING.
    """
    raise NotImplementedError("Implement compute_cost()")


def daily_cost(calls: int, avg_input: int, avg_output: int, model: str) -> float:
    """Return the total USD cost for `calls` API calls per day.

    TODO: Implement this function.
      Use compute_cost() to get the per-call cost, then multiply by calls.
    """
    raise NotImplementedError("Implement daily_cost()")


def compare_models(calls: int, avg_input: int, avg_output: int) -> None:
    """Print a cost-comparison table for all models in PRICING.

    TODO: Implement this function.
      For each model, print: provider, model name, per-call cost, daily cost, monthly cost.
      Sort by daily cost ascending so the cheapest option appears first.
    """
    raise NotImplementedError("Implement compare_models()")


def main():
    print("LLM Cost Calculator")
    print("=" * 60)

    # Part 1: single-call cost for the sample call
    print(f"\nSample call: {SAMPLE_CALL['prompt']}")
    print(f"  Input tokens:  {SAMPLE_CALL['input_tokens']}")
    print(f"  Output tokens: {SAMPLE_CALL['output_tokens']}")
    print()

    # TODO: loop over PRICING and print the cost of the SAMPLE_CALL for each model
    pass

    # Part 2: daily workload comparison
    print(f"\nDaily workload: {DAILY_CALLS:,} calls/day,"
          f" {DAILY_AVG_INPUT} input + {DAILY_AVG_OUTPUT} output tokens avg")

    # TODO: call compare_models(DAILY_CALLS, DAILY_AVG_INPUT, DAILY_AVG_OUTPUT)
    pass


if __name__ == "__main__":
    main()
