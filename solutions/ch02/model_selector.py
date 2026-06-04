"""
Exercise: Model Selector
Chapter 2: The LLM Landscape

Goal: Given a set of task scenarios with real-world constraints (privacy,
context length, budget, latency), implement rule-based logic that recommends
the most suitable model tier and provider.

Skills practiced:
- Applying the model selection decision framework from Chapter 2
- Translating business constraints into selection rules
- Understanding which constraints are hard blockers vs. soft preferences

Instructions:
1. Study the SCENARIOS list - each dict has constraint fields described below.
2. Implement `select_model()` using if/elif rules that mirror the Chapter 2
   decision tree: privacy -> context -> budget -> latency -> quality.
3. Implement `explain_selection()` to print the scenario and the reasoning.
4. Run the script and check your selections against the reasoning column.
5. Add one new scenario of your own and verify your logic handles it correctly.

Scenario fields:
  - description (str): plain-English task description
  - data_privacy (str): "public" | "internal" | "confidential"
  - context_tokens (int): estimated prompt + response size in tokens
  - budget_per_day_usd (float): max API spend per day
  - latency_sensitive (bool): True if response must be near-instant (<500ms)
  - quality_critical (bool): True if errors are costly (medical, legal, financial)

Run: python solutions/ch02/model_selector.py  (from the repo root)
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

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

    Rules applied in priority order - stops at the first rule that fires:
    1. data_privacy == "confidential"  -> "self-hosted"
    2. context_tokens > 32_000         -> large-context tier
    3. budget_per_day_usd < 2.0        -> "mini"
    4. latency_sensitive == True       -> "mini"
    5. quality_critical == True        -> "default"
    6. default fallback                -> "mini"
    """
    if scenario["data_privacy"] == "confidential":
        return "self-hosted", "Confidential data must not leave private infrastructure."

    if scenario["context_tokens"] > 32_000:
        key = "large-context-default" if scenario["quality_critical"] else "large-context-mini"
        return key, "Input exceeds standard context window; needs a large-context model."

    if scenario["budget_per_day_usd"] < 2.0:
        return "mini", "Tight budget requires the cheapest available tier."

    if scenario["latency_sensitive"]:
        return "mini", "Latency-sensitive task - mini tier responds faster."

    if scenario["quality_critical"]:
        return "default", "Quality-critical task - default tier reduces error risk."

    return "mini", "No hard constraints; mini tier is sufficient and cost-effective."


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


# Expected output (illustrative):
#
# Model Selector - rule-based recommendation engine
# ============================================================
#
# Scenario 1: HR FAQ Slack bot answering 'What are the office hours?'
#   Constraints: privacy=internal, ctx=500 tokens, budget=$5.0/day,
#                latency=True, quality=False
#   Recommendation: tier=mini (e.g., gpt-4o-mini / gemini-flash / claude-haiku)
#   Reason: Latency-sensitive task - mini tier responds faster.
#
# Scenario 2: Patient record analysis for a hospital...
#   Recommendation: Self-hosted open-source model (e.g., Llama 3)
#   Reason: Confidential data must not leave private infrastructure.
#
# Scenario 3: Summarizing 300-page manuscript into a 2-page synopsis
#   Recommendation: tier=mini with a large-context provider (e.g., gemini-flash 1M)
#   Reason: Input exceeds standard context window; needs a large-context model.
#
# Scenario 4: Real-time code autocomplete in an IDE plugin
#   Recommendation: tier=mini (e.g., gpt-4o-mini / gemini-flash / claude-haiku)
#   Reason: Latency-sensitive task - mini tier responds faster.
#
# Scenario 5: Legal contract review - flagging liability clauses
#   Recommendation: Self-hosted open-source model (e.g., Llama 3)
#   Reason: Confidential data must not leave private infrastructure.
