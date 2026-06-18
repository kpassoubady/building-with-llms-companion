# Exercise 2: Work Order Parser and Cost Checker

**Capstone 1: Global Fleet Intelligence**

**Scenario:** Repair shops send work orders as messy free text. Global needs them parsed into line items and flagged when a charge looks out of range for that service.

**Task:** Parse each work order into structured JSON (vehicle, mileage, line items with type and cost, total), then have the model reason step by step about whether the total is reasonable for the work described and return a `cost_assessment` of WITHIN_RANGE, HIGH, or SUSPICIOUS with a short justification.

**Skills practiced:** Robust parsing of inconsistent input, few-shot examples to anchor the output shape, chain-of-thought so the cost judgment is reasoned rather than guessed, input cleaning, and estimating the token cost of each call.

## Instructions

1. Open `start/work_order_parser.py`.
2. Implement the `SYSTEM_PROMPT` to parse the work order text and assess the cost.
3. Run the code:
   ```bash
   python exercises/capstone-1/work_order_parser/start/work_order_parser.py
   ```
4. Verify that parsed totals match the line items, the cost assessment is defensible for each sample, and it prints an estimated per-call cost.

## Getting Stuck?
If you need help, check the `solution/` directory for the completed, working code.
