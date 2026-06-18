import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

SCENARIOS = [
    {
        "description": "HR FAQ Slack bot answering 'What are the office hours?'",
        "data_privacy": "internal",
        "context_tokens": 500,
        "budget_per_day_usd": 5.0,
        "latency_sensitive": True,
        "quality_critical": False,
    },
    {
        "description": "Patient record analysis for a hospital - no data leaves the private cloud",
        "data_privacy": "confidential",
        "context_tokens": 4_000,
        "budget_per_day_usd": 50.0,
        "latency_sensitive": False,
        "quality_critical": True,
    },
    {
        "description": "Summarizing 300-page manuscript into a 2-page synopsis",
        "data_privacy": "public",
        "context_tokens": 120_000,
        "budget_per_day_usd": 20.0,
        "latency_sensitive": False,
        "quality_critical": False,
    },
    {
        "description": "Real-time code autocomplete in an IDE plugin",
        "data_privacy": "internal",
        "context_tokens": 2_000,
        "budget_per_day_usd": 10.0,
        "latency_sensitive": True,
        "quality_critical": False,
    },
    {
        "description": "Legal contract review - flagging liability clauses",
        "data_privacy": "confidential",
        "context_tokens": 30_000,
        "budget_per_day_usd": 100.0,
        "latency_sensitive": False,
        "quality_critical": True,
    },
]

# Model recommendation options your selector can return
RECOMMENDATIONS = {
    "self-hosted": "Self-hosted open-source model (e.g., Llama 3)",
    "mini": "tier=mini (e.g., gpt-4o-mini / gemini-flash / claude-haiku)",
    "default": "tier=default (e.g., gpt-4o / gemini-pro / claude-sonnet)",
    "large-context-mini": "tier=mini with a large-context provider (e.g., gemini-flash 1M)",
    "large-context-default": "tier=default with a large-context provider",
}


def select_model(scenario: dict) -> tuple[str, str]:
    """Return (recommendation_key, reason) for the given scenario."""
    if scenario["data_privacy"] == "confidential":
        return "self-hosted", "Confidential data must not leave private infrastructure."
    
    if scenario["context_tokens"] > 32_000:
        key = "large-context-default" if scenario["quality_critical"] else "large-context-mini"
        return key, "Input exceeds standard context window; needs a large-context model."
    
    if scenario["budget_per_day_usd"] < 2.0:
        return "mini", "Strict budget constraint forces use of cheaper tier."
        
    if scenario["latency_sensitive"]:
        return "mini", "Latency-sensitive with simple inputs - mini tier is fast enough."
        
    if scenario["quality_critical"]:
        return "default", "Quality is critical (errors are costly) - use the most capable model."
        
    return "mini", "Default choice for standard tasks without special constraints."


def explain_selection(index: int, scenario: dict, key: str, reason: str) -> None:
    """Print the scenario and the model selection with its reasoning."""
    print(f"\nScenario {index + 1}: {scenario['description']}")
    print(f"  Constraints: privacy={scenario['data_privacy']}, "
          f"ctx={scenario['context_tokens']:,} tokens, "
          f"budget=${scenario['budget_per_day_usd']}/day, "
          f"latency={scenario['latency_sensitive']}, quality={scenario['quality_critical']}")
    print(f"  Recommendation: {RECOMMENDATIONS[key]}")
    print(f"  Reason: {reason}")


def main():
    print("Model Selector - rule-based recommendation engine")
    print("=" * 60)

    for i, scenario in enumerate(SCENARIOS):
        key, reason = select_model(scenario)
        explain_selection(i, scenario, key, reason)

    print("\nDone. Review each selection - do the recommendations match your intuition?")


if __name__ == "__main__":
    main()
