"""
Capstone 1 (Chapters 1-8) - Exercise 1: Driver Issue Classifier
Complexity: low to mid

Goal: Classify a free-text driver vehicle report into structured JSON
so the Global service desk can route safety-critical issues first.

Skills practiced (Chapters 1-8):
- Role prompting and a rules-based system message
- Forcing valid JSON output
- temperature=0.0 for consistent classification
- Few-shot examples to anchor severity boundaries

Instructions:
1. Write SYSTEM_MESSAGE: set the role, list the allowed values for each
   field, and demand JSON only.
2. Add two or three few-shot examples inside FEW_SHOT to lock in the
   difference between SAFETY_CRITICAL and HIGH.
3. Implement classify_issue(): build the messages, call get_completion
   with temperature=0.0, parse the JSON, handle malformed output.
4. Run and confirm all eight sample reports classify sensibly.

Run: python3 capstone-1/exercise1_issue_classifier.py
"""

import sys
import json

sys.path.insert(0, ".")

from shared import get_completion, show_config


# TODO: Write the system message.
# It must (a) give the model a role as a fleet service triage assistant,
# (b) list the exact allowed values for category, severity, drivable, and
# recommended_action, and (c) require JSON only with no markdown fences.
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
- Do not invent details that are not in the report.
- TODO: add any additional rules you find you need after testing."""


# TODO: Add 2-3 few-shot examples as alternating user/assistant turns.
# Pick edge cases that fixed a wrong classification during your testing,
# for example a "grinding brakes" report that must be SAFETY_CRITICAL.
FEW_SHOT = [
    # {"role": "user", "content": "Report: ..."},
    # {"role": "assistant", "content": '{"category": "...", ...}'},
]


# Eight sample driver reports spanning the severity range.
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
    # TODO: Implement this function.
    # 1. Build messages: SYSTEM_MESSAGE, then *FEW_SHOT, then the user report.
    # 2. Call get_completion with temperature=0.0.
    # 3. Parse the response with json.loads().
    # 4. On JSONDecodeError, strip markdown fences and retry once, then
    #    return {"error": "...", "raw": response} if it still fails.
    #
    # Hint:
    # messages = [{"role": "system", "content": SYSTEM_MESSAGE}]
    # messages += FEW_SHOT
    # messages.append({"role": "user", "content": f"Report: {report_text}"})
    # response = get_completion(messages=messages, temperature=0.0)
    # try:
    #     return json.loads(response)
    # except json.JSONDecodeError:
    #     cleaned = response.strip().removeprefix("```json").removeprefix("```").removesuffix("```")
    #     try:
    #         return json.loads(cleaned)
    #     except json.JSONDecodeError:
    #         return {"error": "invalid JSON", "raw": response}

    return {"error": "TODO: implement classify_issue()"}


def main():
    show_config()
    print("\n🚗 Driver Issue Classifier - Capstone Exercise 1")
    print("=" * 60)

    for i, report in enumerate(SAMPLE_REPORTS, 1):
        print(f"\n[{i}] {report}")
        result = classify_issue(report)
        print(json.dumps(result, indent=2))
        print("-" * 60)

    print("\n✅ Exercise 1 complete when every report parses and classifies sensibly.")


if __name__ == "__main__":
    main()
