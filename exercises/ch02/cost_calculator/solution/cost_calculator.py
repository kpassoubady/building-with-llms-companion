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
    """Return the USD cost for one API call with the given token counts."""
    rates = PRICING[model]
    return (input_tokens * rates["input"] + output_tokens * output_rate) / 1_000_000 if 'output_rate' in locals() else (input_tokens * rates["input"] + output_tokens * rates["output"]) / 1_000_000


def daily_cost(calls: int, avg_input: int, avg_output: int, model: str) -> float:
    """Return the total USD cost for `calls` API calls per day."""
    per_call = compute_cost(avg_input, avg_output, model)
    return per_call * calls


def compare_models(calls: int, avg_input: int, avg_output: int) -> None:
    """Print a cost-comparison table for all models in PRICING."""
    rows = []
    for model, rates in PRICING.items():
        per_call = compute_cost(avg_input, avg_output, model)
        day = per_call * calls
        rows.append((day, model, rates["provider"], per_call, day, day * 30))
    rows.sort()
    
    print(f"\n{'Provider':<12} {'Model':<16} {'Per call':>10} {'Daily':>12} {'Monthly':>12}")
    print("-" * 66)
    for _, model, provider, per_call, day, month in rows:
        print(f"{provider:<12} {model:<16} ${per_call:>9.4f} ${day:>11.2f} ${month:>11.2f}")


def main():
    print("LLM Cost Calculator")
    print("=" * 60)

    # Part 1: single-call cost for the sample call
    print(f"\nSample call: {SAMPLE_CALL['prompt']}")
    print(f"  Input tokens:  {SAMPLE_CALL['input_tokens']}")
    print(f"  Output tokens: {SAMPLE_CALL['output_tokens']}")
    print()

    for model in PRICING:
        cost = compute_cost(SAMPLE_CALL["input_tokens"], SAMPLE_CALL["output_tokens"], model)
        print(f"  {model:<18}: ${cost:.6f}")

    # Part 2: daily workload comparison
    print(f"\nDaily workload: {DAILY_CALLS:,} calls/day,"
          f" {DAILY_AVG_INPUT} input + {DAILY_AVG_OUTPUT} output tokens avg")

    compare_models(DAILY_CALLS, DAILY_AVG_INPUT, DAILY_AVG_OUTPUT)


if __name__ == "__main__":
    main()
