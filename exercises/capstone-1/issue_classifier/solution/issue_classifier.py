"""
SOLUTION - Capstone 1 (Chapters 1-8) Exercise 1: Driver Issue Classifier

Instructor reference. A fully working version of exercise1_issue_classifier.py.
Hand this out after learners attempt the scaffold, or use it to demo live.

Run: python3 capstone-1/solutions/exercise1_issue_classifier_solution.py
"""

import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")))

from shared import get_completion, show_config


SYSTEM_MESSAGE = """You are a fleet service triage assistant for Global.

Classify the driver's vehicle report. Respond with ONLY valid JSON
(no markdown fences, no text outside the JSON):

{
  "category": "Engine | Brakes | Tires | Electrical | HVAC | Body | Fluids | Other",
  "severity": "SAFETY_CRITICAL | HIGH | MEDIUM | LOW",
  "drivable": true or false,
  "recommended_action": "TOW_NOW | SCHEDULE_SERVICE | MONITOR",
  "summary": "one short sentence describing the issue"
}

Severity guide:
- SAFETY_CRITICAL: brakes failing, steering loss, smoke/fire, tire blowout
- HIGH: warning lights for engine/oil, overheating, fluid leaks while driving
- MEDIUM: degraded performance, intermittent faults, worn components
- LOW: cosmetic, noises with no performance impact, routine wear

Rules:
- If the vehicle is unsafe to drive, set drivable to false and action to TOW_NOW.
- A check-engine light alone, with normal driving, is HIGH and still drivable.
- Do not invent details that are not in the report.
- recommended_action follows severity: SAFETY_CRITICAL -> TOW_NOW,
  HIGH/MEDIUM -> SCHEDULE_SERVICE, LOW -> MONITOR (unless safety says otherwise)."""


# Few-shot examples that lock in the SAFETY_CRITICAL vs HIGH boundary.
FEW_SHOT = [
    {"role": "user", "content": "Report: Grinding noise from front brakes and the pedal feels soft."},
    {"role": "assistant", "content": json.dumps({
        "category": "Brakes",
        "severity": "SAFETY_CRITICAL",
        "drivable": False,
        "recommended_action": "TOW_NOW",
        "summary": "Front brakes grinding with a soft pedal, unsafe to drive.",
    })},
    {"role": "user", "content": "Report: Engine light is on but the truck runs fine."},
    {"role": "assistant", "content": json.dumps({
        "category": "Engine",
        "severity": "HIGH",
        "drivable": True,
        "recommended_action": "SCHEDULE_SERVICE",
        "summary": "Check-engine light on with normal driving behavior.",
    })},
]


SAMPLE_REPORTS = [
    "Brake pedal goes almost to the floor before it grabs. Scary on the highway.",
    "Check engine light came on this morning. Truck still drives fine otherwise.",
    "AC blows warm air. Everything else is normal.",
    "Loud grinding from the front wheels when I brake, and the wheel shakes.",
    "Small oil spot under the van every morning, level is still in range.",
    "Tire pressure light on. Front left feels a little low but holding.",
    "Steering wheel pulls hard to the right and there's a burning smell.",
    "Door rattles on bumpy roads. No other issues.",
]


def classify_issue(report_text):
    """Classify a single driver report into structured JSON."""
    messages = [{"role": "system", "content": SYSTEM_MESSAGE}]
    messages += FEW_SHOT
    messages.append({"role": "user", "content": f"Report: {report_text}"})

    response = get_completion(messages=messages, temperature=0.0)
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        cleaned = response.strip().removeprefix("```json").removeprefix("```").removesuffix("```")
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            return {"error": "invalid JSON", "raw": response}


def main():
    show_config()
    print("\n🚗 Driver Issue Classifier - Exercise 1 SOLUTION")
    print("=" * 60)

    for i, report in enumerate(SAMPLE_REPORTS, 1):
        print(f"\n[{i}] {report}")
        result = classify_issue(report)
        print(json.dumps(result, indent=2))
        print("-" * 60)


if __name__ == "__main__":
    main()
