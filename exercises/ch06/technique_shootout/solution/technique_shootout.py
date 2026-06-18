import os
import sys
import textwrap

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from shared import get_completion

# ---------------------------------------------------------------------------
# Sample data: 10 prompts to test across all techniques
# ---------------------------------------------------------------------------

PROMPTS = [
    "Is a hot dog a sandwich? Explain your reasoning.",
    "What is the time complexity of binary search?",
    "Translate 'Good morning' to French, Spanish, and Japanese.",
    "Suggest a name for a productivity app aimed at developers.",
    "List three pros and three cons of working remotely.",
    "What does HTTP stand for?",
    "Give a one-sentence summary of the water cycle.",
    "Write a two-line rhyme about debugging code.",
    "Which is larger: 9.11 or 9.9? Explain.",
    "Name two famous scientists and their most notable discovery.",
]

# Few-shot examples for the few-shot strategy
FEW_SHOT_PAIRS = [
    (
        "Is a tomato a fruit or a vegetable?",
        "Botanically a fruit (it develops from a flower ovary); "
        "culinarily treated as a vegetable.",
    ),
    (
        "What is the capital of Australia?",
        "Canberra.",
    ),
]

# ---------------------------------------------------------------------------
# Strategy functions
# ---------------------------------------------------------------------------


def zero_shot(prompt):
    """Answer the prompt with no examples or special framing."""
    return get_completion(
        messages=[{"role": "user", "content": prompt}],
        tier="mini",
        temperature=0.3,
    )


def few_shot(prompt):
    """Answer the prompt after showing two worked examples in the system message."""
    examples = "\n".join(
        f"Q: {q}\nA: {a}" for q, a in FEW_SHOT_PAIRS
    )
    system = "Answer concisely. Here are examples:\n\n" + examples
    return get_completion(
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        tier="mini",
        temperature=0.3,
    )


def chain_of_thought(prompt):
    """Ask the model to think step by step before answering."""
    cot_prompt = prompt + "\n\nThink step by step."
    return get_completion(
        messages=[{"role": "user", "content": cot_prompt}],
        tier="mini",
        temperature=0.3,
    )


def role_prompting(prompt):
    """Ask the model to answer as a knowledgeable domain expert."""
    system = (
        "You are an expert educator who gives precise, well-structured answers "
        "suitable for a technical audience. Be clear and concise."
    )
    return get_completion(
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        tier="mini",
        temperature=0.3,
    )


# ---------------------------------------------------------------------------
# Runner and display
# ---------------------------------------------------------------------------

STRATEGIES = {
    "zero-shot": zero_shot,
    "few-shot": few_shot,
    "chain-of-thought": chain_of_thought,
    "role-prompt": role_prompting,
}

COL_WIDTH = 38


def run_shootout():
    """Run all strategies on every prompt and print a comparison table."""
    print("Chapter 6 - Technique Shootout\n")
    print("Collecting responses (this may take a moment)...\n")

    for i, prompt in enumerate(PROMPTS, start=1):
        print(f"Prompt {i:2}: {prompt}")
        print("-" * (COL_WIDTH * 2 + 5))
        results = {}
        for name, fn in STRATEGIES.items():
            results[name] = fn(prompt)

        # Print two techniques per row
        names = list(STRATEGIES.keys())
        for j in range(0, len(names), 2):
            left_name = names[j]
            right_name = names[j + 1] if j + 1 < len(names) else ""
            left_text = textwrap.fill(results[left_name], width=COL_WIDTH)
            right_text = (
                textwrap.fill(results[right_name], width=COL_WIDTH)
                if right_name
                else ""
            )
            left_lines = left_text.splitlines()
            right_lines = right_text.splitlines()
            max_lines = max(len(left_lines), len(right_lines))

            print(f"  [{left_name}]{' ' * (COL_WIDTH - len(left_name) - 3)}"
                  f"  [{right_name}]")
            for k in range(max_lines):
                l = left_lines[k] if k < len(left_lines) else ""
                r = right_lines[k] if k < len(right_lines) else ""
                print(f"  {l:<{COL_WIDTH}}  {r}")
            print()

        print("=" * (COL_WIDTH * 2 + 5))
        print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    run_shootout()


if __name__ == "__main__":
    main()
