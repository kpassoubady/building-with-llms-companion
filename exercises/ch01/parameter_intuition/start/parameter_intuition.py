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
    """Send `prompt` to both tiers and return (mini_response, default_response).

    TODO: Implement this function.
      1. Call get_completion() with tier="mini" and store the result.
      2. Call get_completion() with tier="default" and store the result.
      3. Return both as a tuple.
    """
    raise NotImplementedError("Implement query_both_tiers()")


def print_comparison(index: int, prompt: str, mini: str, default: str) -> None:
    """Print the prompt and both responses in a readable side-by-side block.

    TODO: Implement this function.
      Print the prompt number, the prompt text, then each response labeled
      with its model name (get_model("mini") / get_model("default")).
      Use SEPARATOR to visually divide sections.
    """
    raise NotImplementedError("Implement print_comparison()")


def main():
    print("Parameter Intuition - mini vs. default model comparison")
    print(f"Mini model:    {get_model('mini')}")
    print(f"Default model: {get_model('default')}")
    print()

    for i, prompt in enumerate(PROMPTS):
        # TODO: call query_both_tiers and print_comparison
        pass

    print("\nObservations (fill in LOG_NOTES at the top of this file):")
    for i, note in LOG_NOTES.items():
        label = PROMPTS[i][:50]
        print(f"  [{i + 1}] {label!r}: {note or '(not yet filled in)'}")


if __name__ == "__main__":
    main()
