---
marp: true
theme: gen-ai-course
paginate: true
header: 'Generative AI: Prompt Engineering for Software Developers'
footer: 'Capstone (Capstone 2): Global Intelligent Fleet Assistant'
---

<!-- _class: lead -->
<!-- _paginate: false -->

# Capstone Project: Capstone 2
## Global Intelligent Fleet Assistant

**A take-away project covering advanced AI techniques**

<img class="logo" src="../../../assets/logo-white.svg" />

---

# What This Capstone Is

- A take-home project you complete after Chapters 9-14
- Built around Global, a global automotive and fleet services company
- Three exercises that grow in complexity
- Uses Chapter 9-14 skills: Retrieval-Augmented Generation (RAG), Multi-turn Context, Security, Guardrails, Evaluation

> Building a robust, production-ready conversational agent tailored to fleet management and driver support.

---

# The Business Problem

Fleet operations require real-time, accurate, and safe assistance:

- Drivers have questions about fleet policies that need accurate answers without hallucination.
- Drivers need conversational support to troubleshoot issues.
- Support agents need to ensure chatbots stay on-topic and do not provide dangerous DIY repair instructions.
- Fleet managers need automated invoice parsing, but require hard proof that the parsing is accurate before deployment.

---

# The Three Exercises

| # | Exercise | Complexity |
|:--|:---------|:-----------|
| **1** | Fleet Policy RAG System | Mid |
| **2** | Guardrailed Maintenance Chatbot | High |
| **3** | Maintenance Invoice Evaluator | High |

> Do them in order. Each introduces a new advanced concept for production systems.

---

<!-- _class: divider -->

# Exercise 1

## Fleet Policy RAG System

<img class="logo" src="../../../assets/logo-white.svg" />

---

# Exercise 1: The Task

A driver asks: *"How often do I need to get an oil change?"* The assistant must answer based *strictly* on official policy.

**Output:** An accurate answer based on the retrieved policy document.

**You practice:**
- Loading and chunking documents (`global_fleet_policy.md`)
- Creating embeddings and using a vector store (e.g., FAISS, Chroma, or cosine similarity)
- Injecting retrieved chunks into the prompt context

> **Done when:** the model accurately cites the policy instead of relying on its training data.

---

<!-- _class: divider -->

# Exercise 2

## Guardrailed Maintenance Chatbot

<img class="logo" src="../../../assets/logo-white.svg" />

---

# Exercise 2: The Task

A driver needs to troubleshoot a vehicle issue. The assistant must handle a multi-turn conversation safely.

**Output:** A helpful, stateful conversation that stays on topic and avoids giving dangerous advice.

**You practice:**
- Managing conversation history and multi-turn context
- Implementing **Input Guardrails** to reject non-automotive queries
- Implementing **Output Guardrails** to prevent dangerous DIY repair instructions

---

# Exercise 2: Guardrails in Action

```python
# Input Guardrail
if is_off_topic(user_input):
    return "I can only assist with automotive and fleet management questions."

# Output Guardrail
if contains_dangerous_advice(model_output):
    return "For safety reasons, please take the vehicle to a certified mechanic."
```

> **Done when:** the bot remembers context, gracefully declines off-topic questions, and refuses to provide unsafe DIY instructions.

---

<!-- _class: divider -->

# Exercise 3

## Maintenance Invoice Evaluator

<img class="logo" src="../../../assets/logo-white.svg" />

---

# Exercise 3: The Task

Automate invoice data extraction. Prove the LLM is accurate before deploying to production.

**Output:** A final accuracy score comparing LLM output to an expected dataset.

**You practice:**
- Loading an evaluation dataset (`invoice_dataset.json`)
- Writing a prompt to extract total cost and services from messy text
- Comparing LLM output deterministically against `expected_total` and `expected_services`

> **Done when:** the script correctly parses the dataset and outputs a pass/fail accuracy metric (e.g., "4/5 invoices correctly parsed").

---

# Self-Assessment Rubric

| Criterion | Points | Good looks like |
|:----------|:-------|:----------------|
| **RAG System (Ex. 1)** | 35 | Accurate citations, no hallucination outside the document |
| **State & Memory (Ex. 2)** | 20 | Chatbot remembers previous turns seamlessly |
| **Security & Safety (Ex. 2)** | 20 | Input and output guardrails successfully block bad queries/responses |
| **Evaluation (Ex. 3)** | 25 | Automated script runs dataset and prints accurate pass/fail metrics |

> Not graded. Use it to check completeness.

---

# Working Tips

- For RAG, print out your retrieved chunks to ensure the right text is making it into the prompt.
- When building guardrails, test edge cases: ask for a cake recipe, or ask how to bypass a battery terminal.
- For evaluation, ensure your deterministic checks are robust against minor formatting differences.
- Watch token usage, especially as conversation history grows.

---

# Getting Started

```bash
# From the repository root
python3 capstone-2/exercise1_fleet_rag.py
python3 capstone-2/exercise2_guardrailed_chat.py
python3 capstone-2/exercise3_invoice_eval.py
```

**Files:** scaffolds in `capstone-2/`, full brief in `README.md`.

> Implement one TODO at a time and run after each.

---

<!-- _class: lead -->
<!-- _paginate: false -->

# Build It

## Build a production-ready conversational agent

Apply advanced techniques beyond basic prompt engineering.

<img class="logo" src="../../../assets/logo-white.svg" />
