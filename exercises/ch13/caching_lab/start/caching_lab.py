import os
import sys
import json
import time
import hashlib

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from shared import get_completion

# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------
REPEATED_QUESTION = [{"role": "user", "content": "What is the difference between a list and a tuple in Python?"}]

# Rough cost estimate used for the savings display (dollars per 1K tokens)
MINI_COST_PER_1K_TOKENS = 0.00015
ESTIMATED_TOKENS_PER_RESPONSE = 120


# ---------------------------------------------------------------------------
# Simulated exception - stands in for litellm.exceptions.RateLimitError
# ---------------------------------------------------------------------------
class SimulatedRateLimitError(Exception):
    """Raised in tests to simulate an API rate limit (HTTP 429)."""


# ---------------------------------------------------------------------------
# Step 1: Response cache
# ---------------------------------------------------------------------------
class ResponseCache:
    """In-memory cache keyed by a hash of the messages list.

    Attributes:
        hits: Number of times a cached value was returned.
        misses: Number of times the cache had no entry.
    """

    def __init__(self):
        self._store = {}
        self.hits = 0
        self.misses = 0

    def _key(self, messages):
        """Return a stable hex digest for a messages list."""
        # TODO: Implement cache key generation.
        raise NotImplementedError("Implement _key")

    def get(self, messages):
        """Return cached response or None; update hit/miss counters."""
        # TODO: Implement cache lookup.
        raise NotImplementedError("Implement get")

    def set(self, messages, response):
        """Store response under the key derived from messages."""
        # TODO: Implement cache store.
        raise NotImplementedError("Implement set")

    def stats(self):
        total = self.hits + self.misses
        rate = (self.hits / total * 100) if total else 0
        return {"hits": self.hits, "misses": self.misses, "hit_rate_pct": round(rate, 1)}


# ---------------------------------------------------------------------------
# Step 2: Retry wrapper
# ---------------------------------------------------------------------------
_cache = ResponseCache()


def completion_with_retry(messages, max_retries=3, base_delay=0.5):
    """Return a completion, using the cache and retrying on rate limit errors.

    Check the cache first. On a miss, call get_completion. If SimulatedRateLimitError
    is raised, wait base_delay * (2 ** attempt) seconds and retry up to max_retries times.
    Store successful responses in the cache before returning.

    Args:
        messages: List of message dicts.
        max_retries: Maximum retry attempts after a rate limit error.
        base_delay: Base wait time in seconds (doubles each retry).

    Returns:
        Response string.

    Raises:
        SimulatedRateLimitError: If all retries are exhausted.
    """
    # TODO: Implement completion_with_retry.
    raise NotImplementedError("Implement completion_with_retry")


# ---------------------------------------------------------------------------
# Step 3: Retry demo using a patched version that fails first
# ---------------------------------------------------------------------------
def retry_demo():
    """Show exponential backoff: fail twice, then succeed on the third try."""
    # TODO: Call get_completion but simulate failures on the first two attempts.
    raise NotImplementedError("Implement retry_demo")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("=== Caching Lab ===\n")

    # Ask the same question three times
    print("Asking the same question 3 times...\n")
    # for i in range(3):
    #     response = completion_with_retry(REPEATED_QUESTION)
    #     label = "API call" if (i == 0) else "cached"
    #     print(f"  Call {i + 1} ({label}): {response[:70]}...\n")

    # stats = _cache.stats()
    # print(f"Cache stats: {stats}")
    # tokens_saved = stats["hits"] * ESTIMATED_TOKENS_PER_RESPONSE
    # cost_saved = tokens_saved / 1000 * MINI_COST_PER_1K_TOKENS
    # print(f"Estimated tokens saved: {tokens_saved}")
    # print(f"Estimated cost saved:   ${cost_saved:.6f}\n")

    print("--- Retry demo ---")
    # retry_demo()


if __name__ == "__main__":
    main()
