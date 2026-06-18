"""
Capstone 1 (Chapters 1-8) - Exercise 3: Fleet Service Advisor (mini project)
Complexity: high

Goal: Tie the course together. Ingest a driver report, triage it into
structured JSON, generate a driver notification and a dispatcher action
line, then PROVE the prompt works with an evaluation harness that
compares two prompt versions against a golden dataset.

Skills practiced (Chapters 1-8, the full iteration loop):
- Triage (structured output, role prompting) reused from Exercise 1
- Tone control via temperature on the generated driver message
- Golden dataset of labeled cases
- Deterministic accuracy scoring of classification fields
- LLM-as-judge scoring of the generated message against a rubric
- Prompt versioning: run two variants, compare, pick a winner

This file has more scaffolding because it is a small system. Implement the
TODO functions one at a time and run after each.

Run: python3 capstone-1/exercise3_fleet_service_advisor.py
"""

import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")))

from shared import get_completion, show_config


# ---------------------------------------------------------------------------
# Two prompt versions to compare. V2 should be your improved version.
# ---------------------------------------------------------------------------

TRIAGE_PROMPT_V1 = """You are a fleet triage assistant. Classify the driver report.
Respond with ONLY JSON:
{"category": "...", "severity": "SAFETY_CRITICAL|HIGH|MEDIUM|LOW", "drivable": true/false}
"""

# TODO: Write an improved V2. Ideas: add explicit severity definitions,
# add 1-2 few-shot examples inline, or tighten the category list. The point
# is to measurably beat V1 on the golden dataset below.
TRIAGE_PROMPT_V2 = """TODO: write your improved triage prompt here."""


# Message generation prompt. Produces driver + dispatcher text from a triage.
GENERATE_PROMPT = """You are a Global fleet service coordinator.
Given a triage result and the original report, produce ONLY JSON:
{
  "driver_message": "calm, clear, 1-2 sentences telling the driver what to do",
  "dispatcher_line": "terse action line, e.g. 'TOW - brakes failing, unit grounded'"
}
Rules: do not invent facts not in the report or triage. Be reassuring to the
driver, direct to the dispatcher."""


# LLM-as-judge prompt for scoring the generated driver message.
JUDGE_PROMPT = """You are evaluating a driver-facing service message.
Score it 1-5 on each criterion and respond with ONLY JSON:
{"clarity": 1-5, "tone": 1-5, "faithfulness": 1-5, "comment": "one sentence"}
- clarity: is the action obvious to a non-technical driver?
- tone: calm and professional, not alarming or dismissive?
- faithfulness: does it avoid inventing facts beyond the report and triage?"""


# ---------------------------------------------------------------------------
# Golden dataset: labeled cases. Extend this to at least 8 (10+ is better).
# Labels are the ground truth you score the model against.
# ---------------------------------------------------------------------------

GOLDEN = [
    {"report": "Brake pedal sinks to the floor, barely stops.",
     "category": "Brakes", "severity": "SAFETY_CRITICAL", "drivable": False},
    {"report": "Check engine light on, truck drives normally.",
     "category": "Engine", "severity": "HIGH", "drivable": True},
    {"report": "AC blows warm, nothing else wrong.",
     "category": "HVAC", "severity": "LOW", "drivable": True},
    {"report": "Grinding from front wheels when braking, wheel shakes.",
     "category": "Brakes", "severity": "SAFETY_CRITICAL", "drivable": False},
    {"report": "Small oil drip overnight, level still fine.",
     "category": "Fluids", "severity": "MEDIUM", "drivable": True},
    {"report": "TPMS light on, front left a bit low but holding.",
     "category": "Tires", "severity": "MEDIUM", "drivable": True},
    {"report": "Steering pulls hard right and I smell burning.",
     "category": "Steering", "severity": "SAFETY_CRITICAL", "drivable": False},
    {"report": "Interior door panel rattles on bumps, drives fine.",
     "category": "Body", "severity": "LOW", "drivable": True},
    # TODO: add at least two more of your own labeled cases.
]


def parse_json(text) -> dict:
    """Best-effort JSON parse with markdown-fence stripping."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        cleaned = text.strip().removeprefix("```json").removeprefix("```").removesuffix("```")
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            return {"error": "invalid JSON", "raw": text}


def triage(report_text, prompt) -> dict:
    """Run triage with the given prompt version. Returns parsed dict."""
    # TODO: build messages [system=prompt, user=report], temperature=0.0,
    # return parse_json(response).
    return {"error": "TODO: implement triage()"}


def generate_messages(report_text, triage_result) -> dict:
    """Generate driver + dispatcher messages from a triage result."""
    # TODO: call get_completion with GENERATE_PROMPT. Use a slightly higher
    # temperature (e.g. 0.4) so the driver message reads naturally, but keep
    # it grounded. Return parse_json(response).
    return {"error": "TODO: implement generate_messages()"}


def judge_message(report_text, triage_result, driver_message) -> dict:
    """LLM-as-judge: score the generated driver message. Returns dict of scores."""
    # TODO: send JUDGE_PROMPT plus the report, triage, and driver_message.
    # Use temperature=0.0. Return parse_json(response).
    return {"error": "TODO: implement judge_message()"}


# ---------------------------------------------------------------------------
# Evaluation harness
# ---------------------------------------------------------------------------

def score_classification(prediction, gold):
    """Return how many of category/severity/drivable match the gold label."""
    # TODO: compare prediction["category"], ["severity"], ["drivable"] to gold.
    # Return an int 0-3. Be defensive about missing keys.
    return 0


def evaluate_prompt(prompt, label):
    """Run triage for every golden case, return mean field accuracy (0-1)."""
    print(f"\n=== Evaluating triage prompt: {label} ===")
    total, correct = 0, 0
    for case in GOLDEN:
        pred = triage(case["report"], prompt)
        hits = score_classification(pred, case)
        correct += hits
        total += 3
        print(f"  {hits}/3  {case['report'][:50]}")
    accuracy = correct / total if total else 0.0
    print(f"  -> field accuracy: {accuracy:.1%}")
    return accuracy


def evaluate_generation():
    """Generate and judge messages for a few cases, return mean judge score."""
    print("\n=== Evaluating generated driver messages (LLM-as-judge) ===")
    scores = []
    for case in GOLDEN[:4]:
        tr = triage(case["report"], TRIAGE_PROMPT_V2)
        msgs = generate_messages(case["report"], tr)
        driver_msg = msgs.get("driver_message", "")
        verdict = judge_message(case["report"], tr, driver_msg)
        avg = 0.0
        if all(k in verdict for k in ("clarity", "tone", "faithfulness")):
            avg = (verdict["clarity"] + verdict["tone"] + verdict["faithfulness"]) / 3
            scores.append(avg)
        print(f"  judge {avg:.1f}/5  msg: {driver_msg[:60]}")
    return sum(scores) / len(scores) if scores else 0.0


def main():
    show_config()
    print("\n🛠️  Fleet Service Advisor - Capstone Exercise 3 (mini project)")
    print("=" * 60)

    # Step 1-2: prompt versioning comparison on the golden dataset.
    acc_v1 = evaluate_prompt(TRIAGE_PROMPT_V1, "V1 (baseline)")
    acc_v2 = evaluate_prompt(TRIAGE_PROMPT_V2, "V2 (your improvement)")

    # Step 3: generation + LLM-as-judge.
    judge_avg = evaluate_generation()

    # Step 4: decide.
    print("\n" + "=" * 60)
    print("RESULTS")
    print(f"  Triage accuracy  V1: {acc_v1:.1%}   V2: {acc_v2:.1%}")
    print(f"  Driver message judge average: {judge_avg:.1f}/5")
    winner = "V2" if acc_v2 > acc_v1 else "V1"
    print(f"  Recommended prompt version: {winner}")
    print("\n✅ Exercise 3 complete when the harness reports accuracy for both")
    print("   versions, a judge score, and a justified winner.")


if __name__ == "__main__":
    main()
