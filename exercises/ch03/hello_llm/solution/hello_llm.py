import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from shared import get_completion, show_config

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
    """Summarize `text` in 2 sentences."""
    messages = [
        {"role": "system", "content": "You are a concise summarizer. Reply in 2 sentences."},
        {"role": "user", "content": f"Summarize:\n\n{text}"},
    ]
    return get_completion(messages, tier="mini")


def task_classify(text: str) -> str:
    """Classify the sentiment of `text` as POSITIVE, NEGATIVE, or NEUTRAL."""
    messages = [
        {"role": "system", "content": "Classify sentiment. Reply with exactly one word: POSITIVE, NEGATIVE, or NEUTRAL."},
        {"role": "user", "content": text},
    ]
    return get_completion(messages, tier="mini")


def task_translate(text: str, target_language: str = "French") -> str:
    """Translate `text` into `target_language`."""
    messages = [
        {"role": "system", "content": f"Translate to {target_language}. Return the translation only."},
        {"role": "user", "content": text},
    ]
    return get_completion(messages, tier="mini")


def task_extract_entities(text: str) -> str:
    """Extract named entities (people, organizations, locations, dates) from `text`."""
    messages = [
        {"role": "system", "content": (
            "Extract named entities. Group by type: PERSON, ORG, LOCATION, DATE. "
            "One entity per line, format: TYPE: entity"
        )},
        {"role": "user", "content": text},
    ]
    return get_completion(messages, tier="default")


def task_generate(topic: str) -> str:
    """Generate 3 creative blog post title ideas for `topic`."""
    messages = [
        {"role": "system", "content": "Generate blog post titles. Return exactly 3 numbered titles."},
        {"role": "user", "content": f"Topic: {topic}"},
    ]
    return get_completion(messages, tier="mini")


def main():
    show_config()
    print()

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
        result = fn()
        print(result)


if __name__ == "__main__":
    main()
