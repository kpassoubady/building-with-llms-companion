"""
Capstone 1 (Chapters 1-8) - Exercise 2: Work Order Parser and Cost Checker
Complexity: mid

Goal: Parse a messy repair-shop work order into structured line items,
then have the model reason about whether the total is reasonable for the
work described. Mirrors how Global validates thousands of maintenance
invoices from independent shops.

Skills practiced (Chapters 1-8):
- Robust parsing of inconsistent free-text input
- Few-shot examples to anchor the output shape
- Chain-of-thought so the cost judgment is reasoned, not guessed
- Input preparation and token/cost estimation

Instructions:
1. Write PARSE_SYSTEM to extract structured JSON from a work order.
2. In assess_work_order(), ask the model to think step by step about
   whether the total is reasonable BEFORE giving a cost_assessment.
   Keep the reasoning out of the final JSON (or in a "reasoning" field
   you ignore downstream).
3. Use get_completion_full() to read token usage and print an estimated
   cost per call.
4. Run and confirm parsed totals match line items and the assessments
   are defensible.

Run: python3 capstone-1/exercise2_work_order_parser.py
"""

import sys
import json

sys.path.insert(0, ".")

from shared import get_completion, get_completion_full, show_config


# Rough public pricing for the estimate. Adjust to your provider/tier.
COST_PER_1K_INPUT = 0.00015
COST_PER_1K_OUTPUT = 0.00060


# TODO: Write the parsing + assessment system message.
# It must extract vehicle, mileage, line items (each with description,
# type of PART or LABOR, and cost), and total. It must also return a
# cost_assessment and a short reason. Require JSON only.
PARSE_SYSTEM = """You are a fleet maintenance invoice auditor for Global.

Read the work order and respond with ONLY valid JSON (no markdown fences):

{
  "vehicle": "make/model/year if present, else null",
  "mileage": number or null,
  "service_category": "short category, e.g. Brakes, Oil, Tires, Engine",
  "line_items": [
    {"description": "...", "type": "PART | LABOR", "cost": number}
  ],
  "total": number,
  "cost_assessment": "WITHIN_RANGE | HIGH | SUSPICIOUS",
  "reason": "one sentence justifying the assessment"
}

Before you answer, think step by step about whether the total is
reasonable for the work described, then fill in cost_assessment:
- WITHIN_RANGE: total is normal for this service and parts
- HIGH: above typical but plausible
- SUSPICIOUS: total does not match the line items, or charges look invented

Rules:
- The sum of line item costs should equal total. If it does not, that is
  a strong signal for SUSPICIOUS.
- Do not invent line items or prices that are not in the text.
- Keep "reason" to one sentence.
- TODO: add a few-shot example or two if your assessments drift."""


# Messy, inconsistent work orders, as Global actually receives them.
SAMPLE_WORK_ORDERS = [
    """SHOP: Mike's Auto  VEH: 2021 Ford Transit  ODO 84,221
    front brake pads (parts) 89.00
    rotors x2 142.50
    labor 1.5 hrs @ 120 = 180
    shop supplies 12.00
    TOTAL 423.50""",

    """Oil change synthetic, 2019 Chevy Silverado, 61k miles.
    Oil & filter 72. Labor 35. Total: 107""",

    """2020 RAM ProMaster, 110,233 mi
    Diagnostic fee .......... 150
    "engine service" ........ 1,800
    misc ..................... 600
    TOTAL: 2550""",

    """Tires - 4x replacement, 2022 Transit Connect, 47,900 miles
    tires 4 @ 165 = 660
    mount/balance 80
    disposal 16
    alignment 99
    total 855""",
]


def estimate_cost(usage):
    """Estimate USD cost of one call from a usage object."""
    # TODO: compute (prompt_tokens/1000 * input rate) + (completion_tokens/1000 * output rate)
    # Hint: usage.prompt_tokens and usage.completion_tokens
    return 0.0


def assess_work_order(work_order_text):
    """Parse and cost-assess one work order. Returns (result_dict, est_cost)."""
    # TODO: Implement this function.
    # 1. Build messages with PARSE_SYSTEM and the work order.
    # 2. Call get_completion_full(messages=..., temperature=0.0).
    # 3. Pull text from response.choices[0].message.content and parse JSON.
    # 4. Compute est_cost from response.usage via estimate_cost().
    # 5. Return (parsed_dict_or_error, est_cost).
    #
    # Hint:
    # response = get_completion_full(
    #     messages=[
    #         {"role": "system", "content": PARSE_SYSTEM},
    #         {"role": "user", "content": f"Work order:\n{work_order_text}"},
    #     ],
    #     temperature=0.0,
    # )
    # text = response.choices[0].message.content
    # est = estimate_cost(response.usage)
    # try:
    #     return json.loads(text), est
    # except json.JSONDecodeError:
    #     return {"error": "invalid JSON", "raw": text}, est

    return {"error": "TODO: implement assess_work_order()"}, 0.0


def check_total(result):
    """Sanity check: do the line items add up to the stated total?"""
    if "line_items" not in result or "total" not in result:
        return
    summed = sum(item.get("cost", 0) for item in result["line_items"])
    if abs(summed - result["total"]) > 0.5:
        print(f"  ⚠️  Line items sum to {summed} but total says {result['total']}")
    else:
        print(f"  ✅ Line items reconcile to total ({result['total']})")


def main():
    show_config()
    print("\n🧾 Work Order Parser and Cost Checker - Capstone Exercise 2")
    print("=" * 60)

    running_cost = 0.0
    for i, wo in enumerate(SAMPLE_WORK_ORDERS, 1):
        print(f"\n[{i}] Work order:\n{wo}")
        print("-" * 40)
        result, est = assess_work_order(wo)
        running_cost += est
        print(json.dumps(result, indent=2))
        if "error" not in result:
            check_total(result)
        print(f"  estimated call cost: ${est:.5f}")
        print("=" * 60)

    print(f"\nEstimated total cost for {len(SAMPLE_WORK_ORDERS)} calls: ${running_cost:.5f}")
    print("✅ Exercise 2 complete when totals reconcile and assessments are defensible.")


if __name__ == "__main__":
    main()
