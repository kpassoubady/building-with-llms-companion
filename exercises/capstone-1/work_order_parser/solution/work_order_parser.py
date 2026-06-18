"""
SOLUTION - Capstone 1 (Chapters 1-8) Exercise 2: Work Order Parser and Cost Checker

Instructor reference. A fully working version of exercise2_work_order_parser.py.

Run: python3 capstone-1/solutions/exercise2_work_order_parser_solution.py
"""

import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")))

from shared import get_completion_full, show_config


COST_PER_1K_INPUT = 0.00015
COST_PER_1K_OUTPUT = 0.00060


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

Reason step by step internally about whether the total is reasonable for
the work described, then set cost_assessment:
- WITHIN_RANGE: total is normal for this service and parts
- HIGH: above typical but plausible
- SUSPICIOUS: total does not match the line items, or charges look invented
  or vague (e.g. a large "misc" or unexplained "engine service" line)

Rules:
- The sum of line item costs should equal total. If it does not, that is a
  strong signal for SUSPICIOUS.
- Do not invent line items or prices that are not in the text.
- Keep "reason" to one sentence.

Example of a SUSPICIOUS case: a $2,550 invoice whose only detail is a $150
diagnostic, a vague "engine service" for $1,800, and "misc" for $600 has no
itemized justification for the bulk of the cost."""


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
    return (usage.prompt_tokens / 1000 * COST_PER_1K_INPUT
            + usage.completion_tokens / 1000 * COST_PER_1K_OUTPUT)


def assess_work_order(work_order_text):
    """Parse and cost-assess one work order. Returns (result_dict, est_cost)."""
    response = get_completion_full(
        messages=[
            {"role": "system", "content": PARSE_SYSTEM},
            {"role": "user", "content": f"Work order:\n{work_order_text}"},
        ],
        temperature=0.0,
    )
    text = response.choices[0].message.content
    est = estimate_cost(response.usage)
    try:
        return json.loads(text), est
    except json.JSONDecodeError:
        cleaned = text.strip().removeprefix("```json").removeprefix("```").removesuffix("```")
        try:
            return json.loads(cleaned), est
        except json.JSONDecodeError:
            return {"error": "invalid JSON", "raw": text}, est


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
    print("\n🧾 Work Order Parser and Cost Checker - Exercise 2 SOLUTION")
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


if __name__ == "__main__":
    main()
