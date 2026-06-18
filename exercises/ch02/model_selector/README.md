# Exercise: Model Selector

**Chapter 2: The LLM Landscape**

**Goal:** Given a set of task scenarios with real-world constraints (privacy, context length, budget, latency), implement rule-based logic that recommends the most suitable model tier and provider.

**Skills practiced:**
- Applying the model selection decision framework from Chapter 2
- Translating business constraints into selection rules
- Understanding which constraints are hard blockers vs. soft preferences

## Instructions

1. Go to the `start/` directory and open `model_selector.py`.
2. Study the `SCENARIOS` list - each dict has constraint fields described below.
3. Implement `select_model()` using if/elif rules that mirror the Chapter 2 decision tree: `privacy -> context -> budget -> latency -> quality`.
4. Implement `explain_selection()` to print the scenario and the reasoning.
5. Run the script and check your selections against the reasoning column:
   ```bash
   python exercises/ch02/model_selector/start/model_selector.py
   ```
6. Add one new scenario of your own and verify your logic handles it correctly.

### Scenario fields:
- `description` (str): plain-English task description
- `data_privacy` (str): "public" | "internal" | "confidential"
- `context_tokens` (int): estimated prompt + response size in tokens
- `budget_per_day_usd` (float): max API spend per day
- `latency_sensitive` (bool): True if response must be near-instant (<500ms)
- `quality_critical` (bool): True if errors are costly (medical, legal, financial)

## Getting Stuck?
If you need help, check the `solution/` directory for the completed, working code.
