"""
SOLUTION - Capstone 1 (Chapters 1-8) Exercise 3: Fleet Service Advisor (mini project)

Instructor reference. A fully working version of
exercise3_fleet_service_advisor.py, including a populated V2 prompt, two
extra golden cases, and the full evaluation harness.

Run: python3 capstone-1/solutions/exercise3_fleet_service_advisor_solution.py
"""

import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")))

from shared import get_completion, show_config


TRIAGE_PROMPT_V1 = """You are a fleet triage assistant. Classify the driver report.
Respond with ONLY JSON:
{"category": "...", "severity": "SAFETY_CRITICAL|HIGH|MEDIUM|LOW", "drivable": true/false}
"""

# V2 adds explicit category list, severity definitions, and two few-shot
# examples. This is what learners should converge toward.
TRIAGE_PROMPT_V2 = """You are a fleet service triage assistant for Global.
Classify the driver report. Respond with ONLY JSON, no markdown:
{"category": "...", "severity": "SAFETY_CRITICAL|HIGH|MEDIUM|LOW", "drivable": true/false}

category must be one of:
Engine, Brakes, Tires, Electrical, HVAC, Body, Fluids, Steering, Other.

severity:
- SAFETY_CRITICAL: brakes/steering failure, smoke or burning smell, blowout. drivable=false.
- HIGH: engine/oil warning lights, overheating, active fluid leaks. usually drivable.
- MEDIUM: degraded performance, intermittent faults, low-but-holding tire.
- LOW: cosmetic, rattles, noises with no performance impact.

Examples:
Report: Grinding from front wheels when braking, wheel shakes.
{"category": "Brakes", "severity": "SAFETY_CRITICAL", "drivable": false}
Report: AC blows warm, nothing else wrong.
{"category": "HVAC", "severity": "LOW", "drivable": true}
"""


GENERATE_PROMPT = """You are a Global fleet service coordinator.
Given a triage result and the original report, produce ONLY JSON:
{
  "driver_message": "calm, clear, 1-2 sentences telling the driver what to do",
  "dispatcher_line": "terse action line, e.g. 'TOW - brakes failing, unit grounded'"
}
Rules: do not invent facts not in the report or triage. Be reassuring to the
driver, direct to the dispatcher."""


JUDGE_PROMPT = """You are evaluating a driver-facing service message.
Score it 1-5 on each criterion and respond with ONLY JSON:
{"clarity": 1-5, "tone": 1-5, "faithfulness": 1-5, "comment": "one sentence"}
- clarity: is the action obvious to a non-technical driver?
- tone: calm and professional, not alarming or dismissive?
- faithfulness: does it avoid inventing facts beyond the report and triage?"""


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
    {"report": "Engine temp gauge in the red and steam from the hood.",
     "category": "Engine", "severity": "SAFETY_CRITICAL", "drivable": False},
    {"report": "Headlight out on the passenger side, daytime route only.",
     "category": "Electrical", "severity": "MEDIUM", "drivable": True},
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
    """Run triage with the given prompt version."""
    response = get_completion(
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Report: {report_text}"},
        ],
        temperature=0.0,
    )
    return parse_json(response)


def generate_messages(report_text, triage_result) -> dict:
    """Generate driver + dispatcher messages from a triage result."""
    response = get_completion(
        messages=[
            {"role": "system", "content": GENERATE_PROMPT},
            {"role": "user", "content":
                f"Report: {report_text}\nTriage: {json.dumps(triage_result)}"},
        ],
        temperature=0.4,  # a little warmth for the driver-facing text
    )
    return parse_json(response)


def judge_message(report_text, triage_result, driver_message) -> dict:
    """LLM-as-judge: score the generated driver message."""
    response = get_completion(
        messages=[
            {"role": "system", "content": JUDGE_PROMPT},
            {"role": "user", "content":
                f"Report: {report_text}\nTriage: {json.dumps(triage_result)}\n"
                f"Message to score: {driver_message}"},
        ],
        temperature=0.0,
    )
    return parse_json(response)


def score_classification(prediction, gold):
    """How many of category/severity/drivable match the gold label (0-3)."""
    if "error" in prediction:
        return 0
    hits = 0
    if str(prediction.get("category", "")).lower() == gold["category"].lower():
        hits += 1
    if str(prediction.get("severity", "")).upper() == gold["severity"]:
        hits += 1
    if bool(prediction.get("drivable")) == gold["drivable"]:
        hits += 1
    return hits


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
    print("\n🛠️  Fleet Service Advisor - Exercise 3 SOLUTION (mini project)")
    print("=" * 60)

    acc_v1 = evaluate_prompt(TRIAGE_PROMPT_V1, "V1 (baseline)")
    acc_v2 = evaluate_prompt(TRIAGE_PROMPT_V2, "V2 (improved)")
    judge_avg = evaluate_generation()

    print("\n" + "=" * 60)
    print("RESULTS")
    print(f"  Triage accuracy  V1: {acc_v1:.1%}   V2: {acc_v2:.1%}")
    print(f"  Driver message judge average: {judge_avg:.1f}/5")
    winner = "V2" if acc_v2 >= acc_v1 else "V1"
    print(f"  Recommended prompt version: {winner}")


if __name__ == "__main__":
    main()
