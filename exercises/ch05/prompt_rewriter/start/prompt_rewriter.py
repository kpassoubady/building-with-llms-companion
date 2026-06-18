import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from shared import get_completion

# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

# Each dict has: topic, bad_prompt, anti_pattern (what is wrong), and
# a rewritten key that you will fill in.
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
# TODO: Fill in each rewritten prompt below.
# Use the 4 building blocks:
#   Instruction - starts with a verb, states what done looks like
#   Context     - role, domain, audience, constraints
#   Input Data  - delimited sample input the model should work with
#   Output Format - exact structure you want back
# ---------------------------------------------------------------------------

REWRITES = [
    # Topic: Code review
    # Bad: "Make my code better"
    # TODO: Write a rewritten prompt as a string using all 4 building blocks.
    # Hint: include a persona, a clear task verb, a short sample Python
    # function as the input data (wrapped in triple backticks), and ask
    # for a numbered list of issues with a one-line fix each.
    None,  # replace None with your rewritten prompt string

    # Topic: Microservices advice
    # Bad: "Don't you think microservices are better than monoliths?"
    # TODO: Rewrite as a neutral comparison request with a structured output.
    # Hint: ask for a pros/cons table comparing the two architectures for a
    # specific context (e.g. a 5-person startup), with columns Approach,
    # Pros, Cons, Best For.
    None,

    # Topic: Error explanation
    # Bad: "Be brief but explain everything in detail"
    # TODO: Replace the contradiction with clear, non-conflicting constraints.
    # Hint: pick one: either "in 2 sentences" OR "in 5 bullet points, one
    # sentence each." Add context (junior engineer audience) and input data.
    None,

    # Topic: Log analysis
    # Bad: "Logs"
    # TODO: Turn this into a log classification request with sample log lines
    # as delimited input data and a table as the output format.
    # Hint: provide 2-3 sample log lines between --- delimiters.
    None,

    # Topic: SQL query help
    # Bad: "Write a query and also explain it and optimise it and show indexes"
    # TODO: Pick ONE task (write the query) and specify a clear output format.
    # Hint: ask for a SQL code block followed by a 2-sentence explanation.
    # Treat the other sub-tasks as follow-up prompts.
    None,
]


# ---------------------------------------------------------------------------
# Exercise function
# ---------------------------------------------------------------------------


def run_comparison(bad_prompt: str, rewritten_prompt: str, topic: str) -> None:
    """Call the model with both prompts and print results side-by-side.

    Args:
        bad_prompt: The original flawed prompt string.
        rewritten_prompt: The improved prompt using the 4 building blocks.
        topic: Label for the comparison header.
    """
    # TODO: Call get_completion for bad_prompt (user message only, tier="mini").
    # Then call get_completion for rewritten_prompt (user message only, tier="mini").
    # Print both responses with clear BEFORE / AFTER headers.

    raise NotImplementedError("Complete run_comparison() to continue.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    print("=== Prompt Rewriter ===\n")
    for item, rewritten in zip(BAD_PROMPTS, REWRITES):
        if rewritten is None:
            print(f"[SKIP] '{item['bad_prompt']}' - fill in REWRITES first.")
            continue
        run_comparison(item["bad_prompt"], rewritten, item["topic"])


if __name__ == "__main__":
    main()
