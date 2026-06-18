# Exercise 3: Fleet Service Advisor

**Capstone 1: Global Fleet Intelligence**

**Scenario:** Tie it together into one intake assistant. It ingests a driver report, produces a triage decision, and drafts a short driver-facing notification plus a dispatcher recommendation. Then you prove it works with an evaluation harness.

**Task:**
1. **Triage** the report into structured JSON (reuse and extend Exercise 1).
2. **Generate** two outputs from that triage: a calm driver notification and a terse dispatcher action line. Control tone with `temperature` and role prompting.
3. **Build a golden dataset** of at least eight labeled cases (provided as a starting set; extend it).
4. **Evaluate** with two methods:
   - Deterministic check of the classification fields against the golden labels (accuracy).
   - LLM-as-judge scoring the generated driver message against a rubric (clarity, tone, no invented facts).
5. **Version the prompt.** Run the triage with two prompt variants and compare accuracy and judge scores. Pick a winner and say why.

**Skills practiced:** The full iteration loop: write, test against a golden dataset, score with rubrics and an LLM judge, compare prompt versions, decide. This is the production prompt-engineering workflow in miniature.

## Instructions

1. Open `start/fleet_service_advisor.py`.
2. Implement the logic to triage reports, generate responses, and run the evaluation harness over the golden dataset.
3. Run the code:
   ```bash
   python exercises/capstone-1/fleet_service_advisor/start/fleet_service_advisor.py
   ```
4. Verify that the harness prints classification accuracy for each prompt version, average judge scores for the generated messages, and a one-line recommendation of which prompt version wins.

## Getting Stuck?
If you need help, check the `solution/` directory for the completed, working code.
