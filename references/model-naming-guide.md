# Model Naming Guide: What Every Developer Should Know

LLM providers now ship dozens of model variants with names like "Claude Opus 4.7 High Fast" or "GPT-5.2-Codex High." This guide explains the naming conventions across providers so you can choose the right variant without trial and error.

---

## The Naming Formula

Every model name follows a pattern:

```
[Provider Family] [Version] [Variant Modifiers...]
```

**Examples:**

- `Claude Opus 4.6 Thinking Fast` → Anthropic Opus family, version 4.6, with extended reasoning, speed-optimized
- `GPT-5.1-Codex Max High` → OpenAI GPT-5.1, code-specialized, maximum reasoning effort, high quality tier
- `Gemini 3 Flash Low` → Google Gemini 3, speed-optimized family, low reasoning effort

---

## Modifier Reference

### Reasoning Effort Modifiers

These control how much internal "thinking" the model does before producing output. More thinking means better accuracy on complex tasks but higher latency and cost.

| Modifier | Reasoning Effort | Latency | Cost | Best For |
|:---------|:----------------|:--------|:-----|:---------|
| **(none)** | Standard | Normal | Base price | General-purpose tasks |
| **Low** | Minimal | Fastest | Lowest | Simple classification, extraction, FAQ |
| **Medium** | Moderate | Moderate | Mid-range | Summarization, moderate reasoning |
| **High** | Elevated | Higher | Higher | Complex analysis, production accuracy |
| **Max** | Maximum | Highest | Highest | Research, agentic multi-step workflows |
| **Thinking** | Extended chain-of-thought | Much higher | Higher (more output tokens) | Math proofs, debugging, logic puzzles |

**How "Thinking" works:** The model generates an internal reasoning trace (sometimes visible, sometimes hidden) before producing the final answer. This consumes additional output tokens, which you pay for. For example, a Thinking model might use 2,000 tokens of internal reasoning to produce a 200-token answer, so you are billed for 2,200 output tokens.

**Combining modifiers:** Some providers combine reasoning modifiers. "Low Thinking" means extended chain-of-thought reasoning but with reduced effort (fewer internal tokens). "High Thinking" means aggressive reasoning with more internal tokens.

### Speed and Size Modifiers

| Modifier | What It Means | Tradeoff |
|:---------|:-------------|:---------|
| **Fast** | Optimized for low latency. May use a distilled or smaller internal model. | Speed over depth. Some providers charge more for "Fast" variants of high-end models. |
| **Mini** | Smaller model in the family. Fewer parameters, lower cost. | Reduced capability on complex tasks, but often sufficient for simple ones. |
| **Flash** | Google's term for their speed-optimized models. Similar to "Fast" but a family name rather than a modifier. | Good balance of speed and quality for the price. |
| **Minimal** | Google's lowest-effort Flash variant. | Cheapest option within a family, minimal reasoning. |

### Specialization Modifiers

| Modifier | What It Means | When to Use |
|:---------|:-------------|:------------|
| **Codex** | Code-specialized variant. Trained or fine-tuned for code generation, editing, and understanding. | IDE integrations, automated code review, refactoring tools, code agents. |
| **1M** | Extended context window (typically 1 million tokens). | Analyzing entire codebases, very long documents, book-length inputs. |

### Routing Modifiers

| Modifier | What It Means | When to Use |
|:---------|:-------------|:------------|
| **Adaptive** | The platform automatically routes your request to the best model based on complexity. You do not choose a specific model. | When you trust the provider's routing and want automatic cost/quality optimization. |
| **SWE** | Software Engineering agent model. Designed for autonomous coding tasks (file editing, test writing, debugging). | Agentic coding workflows where the model needs to plan and execute multi-step changes. |

---

## Provider-by-Provider Breakdown

### Anthropic (Claude)

Anthropic uses **family names** for capability tiers and appends modifiers:

| Family | Tier | Description |
|:-------|:-----|:------------|
| **Haiku** | Entry-level | Fast, cheap, good for simple tasks |
| **Sonnet** | Mid-range | Best balance of quality and cost for most tasks |
| **Opus** | Premium | Highest capability, best for complex reasoning |

**Modifier patterns:**

- `Claude Opus 4.6` — Standard Opus, no special mode
- `Claude Opus 4.6 Thinking` — Opus with extended reasoning
- `Claude Opus 4.6 Fast` — Opus optimized for speed (higher cost for speed guarantee)
- `Claude Opus 4.6 Thinking Fast` — Extended reasoning + speed optimized
- `Claude Opus 4.6 1M` — Extended context window variant
- `Claude Sonnet 4.5 Thinking` — Mid-range with extended reasoning

**Pricing pattern:** Opus > Sonnet > Haiku. "Fast" variants of Opus cost significantly more ($30 input vs $5 for standard). "Thinking" variants cost the same per token but consume more output tokens.

### OpenAI (GPT)

OpenAI uses **version numbers** and **suffixes**:

| Pattern | Example | Description |
|:--------|:--------|:------------|
| `GPT-{version}` | GPT-4o, GPT-4.1, GPT-5.5 | Base model, general purpose |
| `GPT-{version}-Codex` | GPT-5.1-Codex | Code-specialized variant |
| `+ Low/High` | GPT-5.5 Low Thinking | Reasoning effort level |
| `+ Thinking` | GPT-5.5 Low Thinking | Extended reasoning mode |
| `o{version}` | o3 | Reasoning-first models (always "thinking") |
| `o{version} High Reasoning` | o3 High Reasoning | Maximum reasoning effort |

**Codex sub-variants:**

- `GPT-5.1-Codex Low` — Code model, minimal reasoning
- `GPT-5.1-Codex Max High` — Code model, maximum effort, high quality
- `GPT-5.1-Codex Max Medium` — Code model, maximum effort, medium quality
- `GPT-5.2-Codex High Fast` — Code model, high quality, speed optimized

**The "o" series:** Models like `o3` are reasoning-first models. They always use extended thinking. "High Reasoning" increases the internal reasoning budget further.

### Google (Gemini)

Google uses **family names** for speed tiers and appends reasoning effort:

| Family | Tier | Description |
|:-------|:-----|:------------|
| **Flash** | Speed-optimized | Fast and cheap, good for most tasks |
| **Pro** | Quality-optimized | Best quality, higher cost |

**Modifier patterns:**

- `Gemini 3 Flash Low` — Speed model, minimal reasoning
- `Gemini 3 Flash Medium` — Speed model, moderate reasoning
- `Gemini 3 Flash High` — Speed model, elevated reasoning
- `Gemini 3 Flash Minimal` — Speed model, absolute minimum effort
- `Gemini 3.1 Pro High Thinking` — Quality model, elevated reasoning with chain-of-thought
- `Gemini 3.1 Pro Low Thinking` — Quality model, reduced reasoning with chain-of-thought
- `Gemini 2.5 Pro` — Previous generation, quality model

**Pricing pattern:** Flash variants all share the same per-token price regardless of reasoning level (you pay more only in output tokens when Thinking is enabled). Pro costs 4x more than Flash per token.

### xAI (Grok)

xAI uses simpler naming:

- `Grok Code Fast 1` — Code-specialized, speed-optimized
- `xAI Grok-3` — General purpose, premium
- `xAI Grok-3 mini Thinking` — Smaller model with extended reasoning

### DeepSeek

- `DeepSeek V4` — General purpose, competitive pricing

---

## Decision Flowchart

Use this when choosing a model variant:

```
Start
  │
  ├─ Is it a simple task (classification, extraction, FAQ)?
  │   └─ YES → Use Mini/Flash/Low variant
  │       └─ Done
  │
  ├─ Does it require complex reasoning (math, logic, debugging)?
  │   └─ YES → Use a Thinking variant
  │       ├─ Budget-sensitive? → Low Thinking
  │       └─ Accuracy-critical? → High Thinking or Max
  │
  ├─ Is latency critical (real-time chat, autocomplete)?
  │   └─ YES → Use a Fast or Flash variant
  │       └─ Done
  │
  ├─ Is it a code-specific task (generation, review, refactoring)?
  │   └─ YES → Use a Codex variant (OpenAI) or code-tuned model
  │       └─ Done
  │
  ├─ Do you need to process very long documents (100K+ tokens)?
  │   └─ YES → Use 1M variant or Gemini Pro
  │       └─ Done
  │
  └─ Default → Use the standard base model (no modifiers)
      └─ Done
```

---

## Cost Implications of Modifiers

Modifiers affect cost in two ways:

1. **Per-token price changes.** "Fast" and "Max" variants of premium models often have higher per-token rates.
2. **Token consumption changes.** "Thinking" variants consume more output tokens (internal reasoning), increasing total cost even if the per-token rate is unchanged.

### Example: Same Task, Different Variants

Assume a task with 1,000 input tokens and a 500-token answer.

| Variant | Input Cost (per 1M) | Output Tokens Used | Output Cost (per 1M) | Total Cost |
|:--------|:-------------------|:-------------------|:--------------------|:-----------|
| Claude Sonnet 4.5 | $3.00 | 500 | $15.00 | $0.0105 |
| Claude Sonnet 4.5 Thinking | $3.00 | 2,500 (500 answer + 2,000 reasoning) | $15.00 | $0.0405 |
| Claude Opus 4.6 | $5.00 | 500 | $25.00 | $0.0175 |
| Claude Opus 4.6 Fast | $30.00 | 500 | $150.00 | $0.1050 |

The "Thinking" variant costs 4x more because of the reasoning tokens. The "Fast" Opus variant costs 6x more per token for the speed guarantee.

---

## Practical Guidelines

1. **Start with the cheapest variant.** For any new feature, begin with Mini/Flash/Low. Only upgrade when you can measure a quality gap.

2. **"Thinking" is not always better.** Extended reasoning helps with complex multi-step problems but actually hurts simple tasks (the model overthinks). It also increases latency significantly.

3. **"Fast" is a latency guarantee, not a quality boost.** Fast variants prioritize response time. They may use a more expensive infrastructure tier to deliver low latency. Use them only when you have measured latency requirements.

4. **"Adaptive" is a black box.** When a platform offers an Adaptive model, it routes your request to whichever model it deems appropriate. This is convenient but gives you less control over cost and consistency. Avoid it for production workloads where you need predictable behavior.

5. **Codex variants are not general-purpose.** They are optimized for code tasks and may underperform on natural language tasks like summarization or creative writing.

6. **Context window variants (1M) cost the same per token** but allow larger inputs. You pay more only because you send more tokens, not because the rate is higher.

7. **Watch for compound modifiers.** "Codex Max High Fast" stacks three modifiers. Read each one: code-specialized + maximum effort + high quality + speed-optimized. This is a premium variant for latency-sensitive, high-accuracy code generation.

---

## Quick Reference: Modifier Cheat Sheet

| I need... | Look for this modifier |
|:----------|:----------------------|
| Cheapest option | Mini, Flash, Low, Minimal |
| Best accuracy | High, Max, Thinking, Opus/Pro |
| Fastest response | Fast, Flash, Mini |
| Code tasks | Codex, Code, SWE |
| Long documents | 1M, Pro (Gemini) |
| Auto-optimization | Adaptive |
| Complex reasoning | Thinking, o-series (OpenAI), High Reasoning |

---

*Last updated: June 2025. Model names and pricing change frequently. Check your provider's documentation for the latest catalog.*
