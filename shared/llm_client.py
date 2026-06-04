"""
Unified LLM client for all book exercises.

Set your keys in `.env`. All exercises import `get_completion()` from this
module, so no exercise code changes when you switch or reorder providers.

Provider selection (personal keys):
  - LLM_PROVIDER_PRIORITY="gemini,openai,claude" sets the fallback order.
    Each call tries providers in order and returns the first that succeeds,
    skipping any provider whose API key is not set.
  - LLM_PROVIDER="claude" forces a single provider (no fallback). Leave it
    unset (or set it to "auto") to use the priority chain.

Supported providers:
  - openai   -> GPT-4o, GPT-4o-mini
  - gemini   -> Gemini 2.5 Flash, Gemini 2.0 Flash
  - claude   -> Claude Sonnet 4, Claude Haiku 4.5

Usage:
    from shared import get_completion

    # Uses the priority chain (gemini -> openai -> claude by default):
    text = get_completion(messages=[{"role": "user", "content": "Hello!"}], tier="mini")

    # Pin one provider for a specific exercise:
    text = get_completion(messages=[...], provider="openai")

    # Pin one exact model (bypasses the chain entirely):
    text = get_completion(messages=[...], model="gpt-4o")
"""

import os
import sys

from dotenv import load_dotenv
import litellm

load_dotenv()

# Provider-to-model mapping
PROVIDER_MODELS = {
    "openai": {
        "default": "gpt-4o",
        "mini": "gpt-4o-mini",
    },
    "gemini": {
        "default": "gemini/gemini-2.5-flash",
        "mini": "gemini/gemini-2.0-flash",
    },
    "claude": {
        "default": "claude-sonnet-4-20250514",
        "mini": "claude-haiku-4-5-20251001",
    },
}

# Environment variable that holds each provider's API key.
PROVIDER_KEYS = {
    "openai": "OPENAI_API_KEY",
    "gemini": "GEMINI_API_KEY",
    "claude": "ANTHROPIC_API_KEY",
}

# Embedding models per provider. Claude has no embeddings API, so it is
# excluded from the embedding chain.
EMBEDDING_MODELS = {
    "openai": "text-embedding-3-small",
    "gemini": "gemini/text-embedding-004",
}

DEFAULT_PRIORITY = ["gemini", "openai", "claude"]

# A single forced provider, or "" / "auto" to use the priority chain.
FORCED_PROVIDER = os.getenv("LLM_PROVIDER", "").strip().lower()
VERBOSE = os.getenv("LLM_VERBOSE", "").strip().lower() in ("1", "true", "yes")


def _priority_list():
    """Parse LLM_PROVIDER_PRIORITY into a clean list, falling back to default."""
    raw = os.getenv("LLM_PROVIDER_PRIORITY", "")
    parsed = [p.strip().lower() for p in raw.split(",") if p.strip()]
    return parsed or DEFAULT_PRIORITY


def has_key(provider):
    """True if the provider's API key is present in the environment."""
    return bool(os.getenv(PROVIDER_KEYS.get(provider, ""), ""))


def get_provider_chain(provider=None, supported=None):
    """Resolve the ordered list of providers to try for a call.

    Args:
        provider: Force a single provider for this call (ignores priority).
        supported: Restrict to this set of providers (e.g. embedding providers).

    Returns:
        A list of provider names to try in order.
    """
    pool = supported if supported is not None else set(PROVIDER_MODELS)

    if provider:
        return [provider]
    if FORCED_PROVIDER and FORCED_PROVIDER not in ("auto", "priority"):
        return [FORCED_PROVIDER]

    chain = [p for p in _priority_list() if p in pool and has_key(p)]
    # If no key matches the priority list, return the keyed providers anyway so
    # the error message names a real provider instead of an empty chain.
    if not chain:
        chain = [p for p in _priority_list() if p in pool] or list(pool)
    return chain


def get_model(tier="default", provider=None):
    """Get the model string for a provider and tier.

    Args:
        tier: "default" for the capable model, "mini" for fast/cheap.
        provider: Provider name. Defaults to the first in the active chain.

    Returns:
        Model string compatible with litellm.
    """
    if provider is None:
        provider = get_provider_chain()[0]
    models = PROVIDER_MODELS.get(provider)
    if not models:
        raise ValueError(
            f"Unknown provider '{provider}'. "
            f"Choose from: {list(PROVIDER_MODELS.keys())}"
        )
    return models.get(tier, models["default"])


def _complete(messages, tier, temperature, max_tokens, provider, model, **kwargs):
    """Core completion call with provider fallback. Returns the full response."""
    # An explicit model pins one exact call with no fallback.
    if model:
        return litellm.completion(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs,
        )

    chain = get_provider_chain(provider=provider)
    errors = []
    for p in chain:
        try:
            return litellm.completion(
                model=get_model(tier, p),
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs,
            )
        except Exception as exc:  # try the next provider in the chain
            errors.append(f"{p}: {type(exc).__name__}: {exc}")
            if VERBOSE:
                print(f"[llm_client] {p} failed, trying next: {exc}", file=sys.stderr)

    detail = "\n  ".join(errors) if errors else "no providers available"
    raise RuntimeError(
        "All providers in the chain failed.\n  " + detail
    )


def get_completion(messages, tier="default", temperature=0.7, max_tokens=1024,
        provider=None, model=None, **kwargs):
    """Send a chat completion request, with provider fallback.

    Args:
        messages: List of message dicts, e.g. [{"role": "user", "content": "Hi"}].
        tier: "default" or "mini".
        temperature: Sampling temperature (0.0 - 2.0).
        max_tokens: Maximum tokens in the response.
        provider: Force one provider for this call (skips the chain).
        model: Force one exact model string (skips the chain).
        **kwargs: Extra parameters passed to litellm.completion().

    Returns:
        The response message content as a string.
    """
    response = _complete(
        messages, tier, temperature, max_tokens, provider, model, **kwargs
    )
    return response.choices[0].message.content


def get_completion_full(messages, tier="default", temperature=0.7, max_tokens=1024,
        provider=None, model=None, **kwargs):
    """Same as get_completion() but returns the full response object.

    Useful when you need usage, finish_reason, etc.
    """
    return _complete(
        messages, tier, temperature, max_tokens, provider, model, **kwargs
    )


def get_embedding(texts, model=None, provider=None):
    """Embed one or more texts, with provider fallback (gemini -> openai).

    Claude has no embeddings API and is excluded from the chain.

    Args:
        texts: A string or list of strings to embed.
        model: Force one exact embedding model (skips the chain).
        provider: Force one provider for this call (skips the chain).

    Returns:
        A list of embedding vectors (one per input text).
    """
    if isinstance(texts, str):
        texts = [texts]

    if model:
        resp = litellm.embedding(model=model, input=texts)
        return [d["embedding"] for d in resp["data"]]

    chain = get_provider_chain(provider=provider, supported=set(EMBEDDING_MODELS))
    errors = []
    for p in chain:
        try:
            resp = litellm.embedding(model=EMBEDDING_MODELS[p], input=texts)
            return [d["embedding"] for d in resp["data"]]
        except Exception as exc:
            errors.append(f"{p}: {type(exc).__name__}: {exc}")
            if VERBOSE:
                print(f"[llm_client] embedding {p} failed, trying next: {exc}",
                    file=sys.stderr)

    detail = "\n  ".join(errors) if errors else "no embedding providers available"
    raise RuntimeError("All embedding providers failed.\n  " + detail)


def show_config():
    """Print the current LLM configuration and resolved provider chain."""
    if FORCED_PROVIDER and FORCED_PROVIDER not in ("auto", "priority"):
        print(f"Mode:          forced provider = {FORCED_PROVIDER}")
    else:
        print(f"Mode:          priority chain = {','.join(_priority_list())}")

    chat_chain = get_provider_chain()
    embed_chain = get_provider_chain(supported=set(EMBEDDING_MODELS))
    print(f"Chat chain:    {chat_chain}  (first = {chat_chain[0]})")
    print(f"Embed chain:   {embed_chain}")
    print(f"Default model: {get_model('default', chat_chain[0])}")
    print(f"Mini model:    {get_model('mini', chat_chain[0])}")

    print("Keys detected:")
    for provider, key_var in PROVIDER_KEYS.items():
        value = os.getenv(key_var, "")
        status = f"...{value[-4:]}" if value else "NOT set"
        print(f"  {provider:<7} {key_var:<18} {status}")


if __name__ == "__main__":
    show_config()
