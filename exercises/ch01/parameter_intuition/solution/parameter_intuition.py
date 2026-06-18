import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from shared import get_completion, get_model

PROMPTS = [
    "What is 17 multiplied by 83?",
    "Write a haiku about debugging code.",
    "Explain recursion in one sentence, as if speaking to a 12-year-old.",
    "List 3 pros and 3 cons of using microservices.",
    "What are the SOLID principles in object-oriented design? Give a one-line summary of each.",
]

# After running the script, fill in your observations here.
LOG_NOTES = {
    0: "",  # math question
    1: "",  # creative writing
    2: "",  # explanation / analogy
    3: "",  # structured list
    4: "",  # technical depth
}

SEPARATOR = "-" * 70


def query_both_tiers(prompt: str) -> tuple[str, str]:
    """Send `prompt` to both tiers and return (mini_response, default_response)."""
    mini_resp = get_completion([{"role": "user", "content": prompt}], tier="mini")
    default_resp = get_completion([{"role": "user", "content": prompt}], tier="default")
    return mini_resp, default_resp


def print_comparison(index: int, prompt: str, mini: str, default: str) -> None:
    """Print the prompt and both responses in a readable side-by-side block."""
    print(f"\nPrompt {index + 1}: {prompt}")
    print(SEPARATOR)
    print(f"[mini  - {get_model('mini')}]")
    print(mini)
    print(SEPARATOR)
    print(f"[default - {get_model('default')}]")
    print(default)
    print(SEPARATOR)


def main():
    print("Parameter Intuition - mini vs. default model comparison")
    print(f"Mini model:    {get_model('mini')}")
    print(f"Default model: {get_model('default')}")
    print()

    for i, prompt in enumerate(PROMPTS):
        mini_resp, default_resp = query_both_tiers(prompt)
        print_comparison(i, prompt, mini_resp, default_resp)

    print("\nObservations (fill in LOG_NOTES at the top of this file):")
    for i, note in LOG_NOTES.items():
        label = PROMPTS[i][:50]
        print(f"  [{i + 1}] {label!r}: {note or '(not yet filled in)'}")


if __name__ == "__main__":
    main()
