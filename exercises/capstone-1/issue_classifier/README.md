# Exercise 1: Driver Issue Classifier

**Capstone 1: Global Fleet Intelligence**

**Scenario:** A Global fleet driver texts a description of a vehicle problem. The service desk needs it classified instantly so safety-critical issues jump the queue.

**Task:** Given a free-text driver report, return JSON with:
- `category` (Engine, Brakes, Tires, Electrical, HVAC, Body, Fluids, Other)
- `severity` (SAFETY_CRITICAL, HIGH, MEDIUM, LOW)
- `drivable` (true or false)
- `recommended_action` (TOW_NOW, SCHEDULE_SERVICE, MONITOR)
- `summary` (one short sentence)

**Skills practiced:** Writing a system message that sets a role and the rules, forcing valid JSON, choosing `temperature=0.0` for consistency, and adding two or three few-shot examples to lock in the severity boundaries.

## Instructions

1. Open `start/issue_classifier.py`.
2. Implement the `SYSTEM_PROMPT` to classify the issue according to the task above.
3. Run the code:
   ```bash
   python exercises/capstone-1/issue_classifier/start/issue_classifier.py
   ```
4. Verify that all eight sample reports classify sensibly and every response parses as JSON on the first try.

## Getting Stuck?
If you need help, check the `solution/` directory for the completed, working code.
