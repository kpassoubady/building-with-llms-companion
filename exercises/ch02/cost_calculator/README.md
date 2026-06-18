# Exercise: Cost Calculator

**Chapter 2: The LLM Landscape**

**Goal:** Compute the cost of LLM API calls from token counts and compare costs across models and providers - no API call required, pure arithmetic.

**Skills practiced:**
- Reading a pricing table keyed by model name
- Computing per-call and per-day cost from input/output token counts
- Comparing cost tradeoffs across providers to inform model selection

## Instructions

1. Go to the `start/` directory and open `cost_calculator.py`.
2. Implement `compute_cost()` to calculate the USD cost of a single API call.
3. Implement `daily_cost()` to project costs over a full day of traffic.
4. Implement `compare_models()` to print a cost table for all models in PRICING.
5. Run the script and observe the spread between the cheapest and most expensive option:
   ```bash
   python exercises/ch02/cost_calculator/start/cost_calculator.py
   ```
6. Bonus: add a fifth model entry to PRICING (check your provider's current pricing page).

## Getting Stuck?
If you need help, check the `solution/` directory for the completed, working code.
