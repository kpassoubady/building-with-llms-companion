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
    """Return (recommendation_key, reason) for the given scenario.

    TODO: Implement this function using the Chapter 2 decision framework.
    Apply rules in this order - stop at the first rule that fires:

    1. data_privacy == "confidential"  -> "self-hosted"
    2. context_tokens > 32_000         -> "large-context-mini" or "large-context-default"
       (use default if quality_critical, mini otherwise)
    3. budget_per_day_usd < 2.0        -> "mini"
    4. latency_sensitive == True       -> "mini"
    5. quality_critical == True        -> "default"
    6. default fallback                -> "mini"

    Return a tuple: (key from RECOMMENDATIONS, one-sentence reason).
    """
    raise NotImplementedError("Implement select_model()")


def explain_selection(index: int, scenario: dict, key: str, reason: str) -> None:
    """Print the scenario and the model selection with its reasoning.

    TODO: Implement this function.
      Print the scenario number, description, the recommended model string
      from RECOMMENDATIONS[key], and the reason.
    """
    raise NotImplementedError("Implement explain_selection()")


def main():
    print("Model Selector - rule-based recommendation engine")
    print("=" * 60)

    for i, scenario in enumerate(SCENARIOS):
        # TODO: call select_model and explain_selection
        pass

    print("\nDone. Review each selection - do the recommendations match your intuition?")


if __name__ == "__main__":
    main()
