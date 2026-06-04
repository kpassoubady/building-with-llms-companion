"""
Exercise: Prompt Rewriter
Chapter 5: Prompt Engineering Fundamentals

Goal: Fix 5 deliberately bad prompts by rewriting each one using the 4
building blocks (Instruction, Context, Input Data, Output Format), then run
both versions and compare the outputs side-by-side.

Skills practiced:
- Recognising common prompt anti-patterns
- Applying all 4 building blocks to a real rewrite
- Comparing model outputs to see the quality difference

Instructions:
1. Read BAD_PROMPTS. Each entry describes what is wrong with the prompt.
2. For each entry, complete the "rewritten" field in REWRITES using all
   4 building blocks. Keep the same underlying topic as the bad prompt.
3. Complete run_comparison() to call the model with both versions and print
   the responses side-by-side.
4. Run the file and note how much the rewrite improves output quality.
5. (Stretch) Add a sixth entry of your own, with a bad prompt you have
   actually written before.

Run: python solutions/ch05/prompt_rewriter.py  (from the repo root)
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from shared import get_completion

# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

BAD_PROMPTS = [
    {
        "topic": "Code review",
        "bad_prompt": "Make my code better",
        "anti_pattern": "No instruction verb, no context, no input, no format.",
    },
    {
        "topic": "Microservices advice",
        "bad_prompt": "Don't you think microservices are better than monoliths?",
        "anti_pattern": "Leading question that anchors the model to one view.",
    },
    {
        "topic": "Error explanation",
        "bad_prompt": "Be brief but explain everything in detail",
        "anti_pattern": "Conflicting constraints - brief AND detailed is contradictory.",
    },
    {
        "topic": "Log analysis",
        "bad_prompt": "Logs",
        "anti_pattern": "Single-word prompt with no instruction, context, or format.",
    },
    {
        "topic": "SQL query help",
        "bad_prompt": "Write a query and also explain it and optimise it and show indexes",
        "anti_pattern": "Multiple unrelated tasks in one prompt with no structure.",
    },
]

# ---------------------------------------------------------------------------
# Rewritten prompts using all 4 building blocks
# ---------------------------------------------------------------------------

REWRITES = [
    # Topic: Code review
    # Instruction: review and list issues
    # Context: senior Python developer, junior audience
    # Input data: sample function in triple backticks
    # Output format: numbered list, one-line fix per issue
    (
        "You are a senior Python developer reviewing code written by a junior engineer.\n\n"
        "Review the function below and list up to 5 specific issues. "
        "For each issue, provide a one-line fix.\n\n"
        "Format each item as:\n"
        "N. [Issue description] - Fix: [one-line fix]\n\n"
        "Code to review:\n"
        "```python\n"
        "def get_user(id):\n"
        "    data = db.query('SELECT * FROM users WHERE id=' + id)\n"
        "    return data[0]\n"
        "```"
    ),

    # Topic: Microservices advice
    # Instruction: compare two architectures neutrally
    # Context: 5-person startup, early-stage product
    # Input data: the two architectures named explicitly
    # Output format: pros/cons table with defined columns
    (
        "Compare microservices and monolithic architecture for a 5-person startup "
        "building an early-stage web product.\n\n"
        "Present a balanced view of both options. "
        "Format your answer as a table with four columns: "
        "Approach | Pros | Cons | Best For\n\n"
        "Use one row per architecture. Keep each cell to one sentence."
    ),

    # Topic: Error explanation
    # Instruction: explain in exactly 5 bullet points
    # Context: audience is a junior engineer with 6 months of Python experience
    # Input data: a specific Python error message
    # Output format: 5 bullets, one sentence each, no jargon
    (
        "You are a Python tutor. "
        "Explain the error message below to a junior engineer with 6 months of Python experience.\n\n"
        "Format your answer as exactly 5 bullet points, one sentence each. "
        "Avoid jargon. Define any technical term you use.\n\n"
        "Error:\n"
        "---\n"
        "TypeError: unsupported operand type(s) for +: 'int' and 'str'\n"
        "---"
    ),

    # Topic: Log analysis
    # Instruction: classify each log line by severity
    # Context: production web application
    # Input data: 3 sample log lines between delimiters
    # Output format: table with Severity and Summary columns
    (
        "You are a site reliability engineer. "
        "Classify each log line below by severity (CRITICAL / HIGH / MEDIUM / LOW) "
        "and write a one-sentence summary of what it means.\n\n"
        "Format your answer as a table: Severity | Summary | Log (first 50 chars)\n\n"
        "Log lines:\n"
        "---\n"
        "FATAL: Database connection pool exhausted after 30 retries.\n"
        "WARNING: Response time exceeded 2000ms for /api/search.\n"
        "INFO: Scheduled cache flush completed. 1204 entries removed.\n"
        "---"
    ),

    # Topic: SQL query help - ONE task only (write the query)
    # Instruction: write a SELECT query
    # Context: PostgreSQL, orders table schema provided
    # Input data: schema definition
    # Output format: SQL code block followed by 2-sentence explanation
    (
        "You are a PostgreSQL expert. "
        "Write a SELECT query that returns the top 10 customers by total order value "
        "in the last 30 days.\n\n"
        "Table schema:\n"
        "```sql\n"
        "orders(id, customer_id, total_amount, created_at)\n"
        "```\n\n"
        "Output format:\n"
        "1. A SQL code block with the query.\n"
        "2. A 2-sentence explanation of what the query does.\n\n"
        "Do not include index suggestions or performance analysis in this response."
    ),
]


# ---------------------------------------------------------------------------
# Solution
# ---------------------------------------------------------------------------


def run_comparison(bad_prompt: str, rewritten_prompt: str, topic: str) -> None:
    """Call the model with both prompts and print results side-by-side.

    Args:
        bad_prompt: The original flawed prompt string.
        rewritten_prompt: The improved prompt using the 4 building blocks.
        topic: Label for the comparison header.
    """
    bad_response = get_completion(
        [{"role": "user", "content": bad_prompt}],
        tier="mini",
    )
    good_response = get_completion(
        [{"role": "user", "content": rewritten_prompt}],
        tier="mini",
    )
    separator = "=" * 60
    print(f"\n{separator}")
    print(f"Topic: {topic}")
    print(f"{separator}")
    print(f"BEFORE:\n{bad_response[:300]}")
    print(f"\nAFTER:\n{good_response[:300]}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    print("=== Prompt Rewriter ===\n")
    for item, rewritten in zip(BAD_PROMPTS, REWRITES):
        run_comparison(item["bad_prompt"], rewritten, item["topic"])


if __name__ == "__main__":
    main()


# Expected output (illustrative):
# === Prompt Rewriter ===
#
# ============================================================
# Topic: Code review
# ============================================================
# BEFORE:
# Here are some suggestions to make your code better:
# 1. Use meaningful variable names...
# (generic, no context, no code to review)
#
# AFTER:
# Code Review Results:
# 1. SQL injection vulnerability on line 3. Fix: use parameterised queries.
# 2. Missing error handling for empty result. Fix: check len(data) before index.
# ...
# (specific, actionable, structured)
