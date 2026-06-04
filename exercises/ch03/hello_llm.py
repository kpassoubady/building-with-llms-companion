"""
Exercise: Hello LLM
Chapter 3: Working with LLM APIs

Goal: Make 5 get_completion calls covering 5 different NLP tasks and print
each result, gaining confidence with the message format and API flow.

Skills practiced:
- Constructing messages lists with "user" and "system" roles
- Calling get_completion() for varied NLP tasks
- Interpreting and printing model responses

Instructions:
1. Implement each of the 5 task functions below (one per NLP task).
2. Each function must build a messages list and call get_completion().
3. Run the file - you should see 5 labeled outputs.
4. Experiment: swap tier="mini" for tier="default" on the quality-sensitive tasks
   and compare the output.

Run: python exercises/ch03/hello_llm.py  (from the repo root)
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from shared import get_completion

# Sample inputs for each task
ARTICLE = (
    "NASA's James Webb Space Telescope has captured the deepest infrared image "
    "of the universe ever taken, showing thousands of galaxies including some of "
    "the faintest objects ever observed. The image covers a patch of sky "
    "approximately the size of a grain of sand held at arm's length and reveals "
    "galaxies that formed less than a billion years after the Big Bang."
)

REVIEW = (
    "I ordered the noise-cancelling headphones and they arrived three days late. "
    "The sound quality is decent, but the ear cushions feel cheap and the "
    "Bluetooth drops every 20 minutes. For $250 I expected better build quality."
)

SENTENCE_EN = "The early bird catches the worm."

NEWS_SNIPPET = (
    "Apple Inc. announced its Q3 earnings on Tuesday in Cupertino, California. "
    "CEO Tim Cook reported record revenue of $81 billion, driven by iPhone sales "
    "in Europe and strong App Store growth in India."
)

TOPIC = "renewable energy storage"


def task_summarize(text: str) -> str:
    """Summarize `text` in 2 sentences.

    TODO: Implement this function.
      Build a messages list with a system message setting the summarization role
      and a user message containing the text. Call get_completion() with tier="mini".

    # Hint:
    # messages = [
    #     {"role": "system", "content": "You are a concise summarizer. Reply in 2 sentences."},
    #     {"role": "user", "content": f"Summarize:\n\n{text}"},
    # ]
    # return get_completion(messages, tier="mini")
    """
    raise NotImplementedError("Implement task_summarize()")


def task_classify(text: str) -> str:
    """Classify the sentiment of `text` as POSITIVE, NEGATIVE, or NEUTRAL.

    TODO: Implement this function.
      Instruct the model to respond with only one word: POSITIVE, NEGATIVE, or NEUTRAL.

    # Hint:
    # messages = [
    #     {"role": "system", "content": "Classify sentiment. Reply with exactly one word: "
    #         "POSITIVE, NEGATIVE, or NEUTRAL."},
    #     {"role": "user", "content": text},
    # ]
    # return get_completion(messages, tier="mini")
    """
    raise NotImplementedError("Implement task_classify()")


def task_translate(text: str, target_language: str = "French") -> str:
    """Translate `text` into `target_language`.

    TODO: Implement this function.
      Build messages instructing the model to translate and return only
      the translated text, no explanation.

    # Hint:
    # messages = [
    #     {"role": "system", "content": f"Translate to {target_language}. Return the translation only."},
    #     {"role": "user", "content": text},
    # ]
    # return get_completion(messages, tier="mini")
    """
    raise NotImplementedError("Implement task_translate()")


def task_extract_entities(text: str) -> str:
    """Extract named entities (people, organizations, locations, dates) from `text`.

    TODO: Implement this function.
      Ask the model to return a simple list of entities grouped by type.
      Use tier="default" for better accuracy on structured extraction.

    # Hint:
    # messages = [
    #     {"role": "system", "content": (
    #         "Extract named entities. Group by type: PERSON, ORG, LOCATION, DATE. "
    #         "One entity per line, format: TYPE: entity"
    #     )},
    #     {"role": "user", "content": text},
    # ]
    # return get_completion(messages, tier="default")
    """
    raise NotImplementedError("Implement task_extract_entities()")


def task_generate(topic: str) -> str:
    """Generate 3 creative blog post title ideas for `topic`.

    TODO: Implement this function.
      Ask for exactly 3 numbered titles, no additional commentary.

    # Hint:
    # messages = [
    #     {"role": "system", "content": "Generate blog post titles. Return exactly 3 numbered titles."},
    #     {"role": "user", "content": f"Topic: {topic}"},
    # ]
    # return get_completion(messages, tier="mini")
    """
    raise NotImplementedError("Implement task_generate()")


def main():
    tasks = [
        ("1. Summarize", lambda: task_summarize(ARTICLE)),
        ("2. Classify sentiment", lambda: task_classify(REVIEW)),
        ("3. Translate", lambda: task_translate(SENTENCE_EN, "French")),
        ("4. Extract entities", lambda: task_extract_entities(NEWS_SNIPPET)),
        ("5. Generate titles", lambda: task_generate(TOPIC)),
    ]

    print("Hello LLM - 5 NLP tasks via get_completion()")
    print("=" * 60)

    for label, fn in tasks:
        print(f"\n[{label}]")
        # TODO: uncomment the next two lines once the functions are implemented
        # result = fn()
        # print(result)


if __name__ == "__main__":
    main()


# Expected output (illustrative):
#
# Hello LLM - 5 NLP tasks via get_completion()
# ============================================================
#
# [1. Summarize]
# NASA's Webb Telescope has taken the deepest infrared image of the universe,
# revealing thousands of galaxies. Some of those galaxies formed less than a
# billion years after the Big Bang.
#
# [2. Classify sentiment]
# NEGATIVE
#
# [3. Translate]
# L'oiseau matinal attrape le ver.
#
# [4. Extract entities]
# ORG: Apple Inc.
# DATE: Tuesday
# LOCATION: Cupertino, California
# PERSON: Tim Cook
# LOCATION: Europe
# LOCATION: India
#
# [5. Generate titles]
# 1. The Battery That Could Save the Grid: Inside Next-Gen Energy Storage
# 2. Why Renewable Energy Needs Better Batteries - and What's Coming
# 3. From Solar Panels to Full-Grid Power: The Storage Problem Solved
