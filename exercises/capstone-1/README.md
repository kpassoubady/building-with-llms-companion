# Capstone 1: Global Fleet Intelligence

A take-away project covering the foundations of prompt engineering. Everything here uses basic skills (API calls, roles, capabilities and limits, input preparation, cost estimation) and prompt structuring (prompt building blocks, zero-shot and few-shot, chain-of-thought, role prompting, structured output, API parameters, the iteration and evaluation loop).

No RAG, no embeddings, no conversation memory, no web framework. Those come in Capstone 2. This project proves you can make an LLM produce reliable, structured, evaluated output from a single well-engineered prompt.

---

## The Business Context

[Global](#) is a global automotive services company operating since 1924. Its segments include fleet management and leasing, vehicle upfitting, powertrain and parts distribution, commercial vehicle equipment, automotive retail, and insurance services. A Global fleet customer might run anywhere from one van to thousands of trucks across North America.

A recurring problem in fleet operations is unstructured text arriving faster than humans can process it:

- Drivers report vehicle problems in plain language, by phone or app.
- Repair shops submit work orders and invoices in inconsistent formats.
- Telematics systems and dispatchers generate alerts that need triage.

Each exercise below turns one of these text streams into structured, actionable data using prompt engineering alone.

---

## The Three Exercises

Work through them in order. Each builds on the prompting skills of the one before.

| # | Exercise | Complexity | Core Chapters 1-8 Skills |
|:--|:---------|:-----------|:--------------------|
| 1 | Driver Issue Classifier | Low to mid | Role prompt, structured JSON, temperature, few-shot |
| 2 | Work Order Parser and Cost Checker | Mid | Parsing, few-shot, chain-of-thought, input prep, cost estimation |
| 3 | Fleet Service Advisor (mini project) | High | Everything above plus golden dataset, LLM-as-judge, prompt versioning |

Files:

```
capstone-1/
  README.md                          this brief
  exercise1_issue_classifier.py      start here
  exercise2_work_order_parser.py
  exercise3_fleet_service_advisor.py
```

Run any exercise from the repository root:

```bash
python3 capstone-1/exercise1_issue_classifier.py
```

---

## Exercise 1: Driver Issue Classifier (low to mid)

**Scenario.** A Global fleet driver texts a description of a vehicle problem. The service desk needs it classified instantly so safety-critical issues jump the queue.

**Task.** Given a free-text driver report, return JSON with:

- `category` (Engine, Brakes, Tires, Electrical, HVAC, Body, Fluids, Other)
- `severity` (SAFETY_CRITICAL, HIGH, MEDIUM, LOW)
- `drivable` (true or false)
- `recommended_action` (TOW_NOW, SCHEDULE_SERVICE, MONITOR)
- `summary` (one short sentence)

**What you practice.** Writing a system message that sets a role and the rules, forcing valid JSON, choosing `temperature=0.0` for consistency, and adding two or three few-shot examples to lock in the severity boundaries.

**Done when.** All eight sample reports classify sensibly and every response parses as JSON on the first try.

---

## Exercise 2: Work Order Parser and Cost Checker (mid)

**Scenario.** Repair shops send work orders as messy free text. Global needs them parsed into line items and flagged when a charge looks out of range for that service.

**Task.** Parse each work order into structured JSON (vehicle, mileage, line items with type and cost, total), then have the model reason step by step about whether the total is reasonable for the work described and return a `cost_assessment` of WITHIN_RANGE, HIGH, or SUSPICIOUS with a short justification.

**What you practice.** Robust parsing of inconsistent input, few-shot examples to anchor the output shape, chain-of-thought so the cost judgment is reasoned rather than guessed, input cleaning, and estimating the token cost of each call.

**Done when.** Parsed totals match the line items, the cost assessment is defensible for each sample, and you print an estimated per-call cost.

---

## Exercise 3: Fleet Service Advisor (high, mini project)

**Scenario.** Tie it together into one intake assistant. It ingests a driver report, produces a triage decision, and drafts a short driver-facing notification plus a dispatcher recommendation. Then you prove it works with an evaluation harness.

**Task.**

1. **Triage** the report into structured JSON (reuse and extend Exercise 1).
2. **Generate** two outputs from that triage: a calm driver notification and a terse dispatcher action line. Control tone with `temperature` and role prompting.
3. **Build a golden dataset** of at least eight labeled cases (provided as a starting set; extend it).
4. **Evaluate** with two methods:
   - Deterministic check of the classification fields against the golden labels (accuracy).
   - LLM-as-judge scoring the generated driver message against a rubric (clarity, tone, no invented facts).
5. **Version the prompt.** Run the triage with two prompt variants and compare accuracy and judge scores. Pick a winner and say why.

**What you practice.** The full iteration loop: write, test against a golden dataset, score with rubrics and an LLM judge, compare prompt versions, decide. This is the production prompt-engineering workflow in miniature.

**Done when.** The harness prints classification accuracy for each prompt version, average judge scores for the generated messages, and a one-line recommendation of which prompt version wins.

---

## Self-Assessment Rubric

This is not graded. Use it to check completeness.

| Criterion | Points | What good looks like |
|:----------|:-------|:---------------------|
| Prompt engineering | 30 | Clear role, explicit rules, few-shot where it helps, right parameters |
| Structured output | 20 | Valid JSON every time, graceful handling of malformed responses |
| Reasoning quality | 15 | Chain-of-thought used where judgment is needed, not everywhere |
| Evaluation (Ex. 3) | 25 | Golden dataset, accuracy metric, working LLM-as-judge, version comparison |
| Code clarity | 10 | Readable, runs from a clean checkout, sensible prints |

---

## Tips

- Start with the simplest prompt that works, then iterate. Do not write the perfect prompt on the first try.
- Keep `temperature=0.0` for classification and parsing. Raise it only for the driver-facing message in Exercise 3.
- When JSON parsing fails, read the raw model output before changing the prompt. The fix is usually one rule in the system message.
- Watch your token usage with `get_completion_full(...).usage` and keep a rough cost in mind. Fleet teams run thousands of these calls a day.
- Treat the LLM as confident but fallible. Never let it invent a VIN, a price, or a safety judgment that was not in the input.
