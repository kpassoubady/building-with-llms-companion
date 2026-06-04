"""
Unified LLM client for all book exercises.

Set your provider and API key in `.env`.
All exercises import `get_completion()` from this module —
no code changes needed when switching providers.

Supported providers:
  - openai   → GPT-4o, GPT-4o-mini
  - gemini   → Gemini 2.5 Flash, Gemini 2.0 Flash
  - claude   → Claude Sonnet 4, Claude Haiku 4.5

Usage:
    from shared import get_completion

    response = get_completion(
        messages=[{"role": "user", "content": "Hello!"}],
        tier="mini",
    )
    print(response)
"""

import os
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

# Read from .env — defaults to openai
PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()


def get_model(tier="default"):
    """Get the model string for the active provider.

    Args:
        tier: "default" for capable model, "mini" for fast/cheap model.

    Returns:
        Model string compatible with litellm.
    """
    models = PROVIDER_MODELS.get(PROVIDER)
    if not models:
        raise ValueError(
            f"Unknown provider '{PROVIDER}'. "
            f"Set LLM_PROVIDER to one of: {list(PROVIDER_MODELS.keys())}"
        )
    return models.get(tier, models["default"])


def get_completion(messages, tier="default", temperature=0.7, max_tokens=1024, **kwargs):
    """Send a chat completion request to the active LLM provider.

    Args:
        messages: List of message dicts, e.g. [{"role": "user", "content": "Hello"}]
        tier: "default" or "mini" — maps to provider-specific model.
        temperature: Sampling temperature (0.0 - 2.0).
        max_tokens: Maximum tokens in the response.
        **kwargs: Additional parameters passed to litellm.completion().

    Returns:
        The response message content as a string.
    """
    model = get_model(tier)
    response = litellm.completion(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        **kwargs,
    )
    return response.choices[0].message.content


def get_completion_full(messages, tier="default", temperature=0.7, max_tokens=1024, **kwargs):
    """Same as get_completion() but returns the full response object.

    Useful when you need to inspect usage, finish_reason, etc.
    """
    model = get_model(tier)
    return litellm.completion(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        **kwargs,
    )


def show_config():
    """Print the current LLM configuration."""
    model = get_model("default")
    mini = get_model("mini")
    print(f"Provider:      {PROVIDER}")
    print(f"Default model: {model}")
    print(f"Mini model:    {mini}")

    # Check the credential is set (without revealing it)
    key_vars = {
        "openai": "OPENAI_API_KEY",
        "gemini": "GEMINI_API_KEY",
        "claude": "ANTHROPIC_API_KEY",
    }
    key_var = key_vars.get(PROVIDER, "UNKNOWN")
    key_value = os.getenv(key_var, "")
    if key_value:
        print(f"Credential:    {key_var} = ...{key_value[-4:]}")
    else:
        print(f"Credential:    ⚠️  {key_var} is NOT set")


if __name__ == "__main__":
    show_config()
