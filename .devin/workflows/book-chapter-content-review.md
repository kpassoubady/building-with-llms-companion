---
description: Review book chapters to remove AI-generated formatting tells, enforce consistent style, and validate chapter structure
---

# Book Chapter Content Review

Strip LLM-style formatting patterns from book chapters. Applies to all markdown files under `book/` (chapters, front matter, back matter, and appendices).

This workflow inherits the core rules from `natural-prose-formatting` and adds book-specific constraints for chapter structure, admonitions, and cross-references.

---

## Core Rules

All rules from the `natural-prose-formatting` skill apply without exception: no em/en dashes, no antithesis patterns, no hedging filler, no sentence-internal dash asides, no bold/italic abuse, no list abuse in prose. Those rules are not repeated here.

---

## Book Chapter Structure Rules

### 1. Required chapter sections

Every chapter must include, in this order:
- Learning objectives (bulleted list with 3 items using action verbs: Explain, Build, Evaluate, Compare...)
- Opening story (section header "## Opening Story" or similar, 2-3 paragraphs)
- Content sections (multiple `##` or `###` sections)
- Try It Yourself (section header "## Try It Yourself" with 2-3 mini exercises)
- Chapter Summary (section header "## Chapter Summary" with a table)
- Common Pitfalls (section header "## Common Pitfalls" with 3+ items)
- Knowledge Check (section header "## Knowledge Check" with 5 questions in `<details>` tags)

### 2. Admonitions

Use 3-5 admonitions per chapter, distributed across sections:

| Type | When to Use | Frequency |
|:-----|:------------|:----------|
| `[!NOTE]` | "Did You Know?" facts, historical context | 1-2 per chapter |
| `[!TIP]` | Best practices, pro tips, shortcuts, cross-references | 1-2 per chapter |
| `[!WARNING]` | Common mistakes that cause real problems | 1 per chapter |
| `[!IMPORTANT]` | Must-know information (security, cost) | 0-1 per chapter |
| `[!CAUTION]` | Actions with irreversible consequences | 0-1 per chapter |

Admonitions should:
- Start with a bold label (e.g., "**Did You Know?**")
- Be concise (1-3 sentences typically)
- For cross-references, use format: `**Cross-Reference:** For a deeper dive into X, see Chapter Y: Title.`

### 3. Code blocks

Code blocks in chapters should:
- Include language specification (```python, ```bash, etc.)
- Be syntactically valid
- Be concise (5-20 lines for inline mini examples)
- Include comments for non-obvious code
- Not be truncated mid-statement
- Use the `shared/llm_client.py` pattern for LLM calls
- Show both code AND expected output

For larger exercises, point to companion repo:
```markdown
> Full exercise with starter code and solution:
> [building-with-llms-companion/exercises/chNN/exercise_name.py](https://github.com/kpassoubady/building-with-llms-companion)
```

### 4. Tables

Tables must:
- Use left-aligned headers with `:---` syntax
- Have no trailing pipes after the last column
- Keep cell content short (one line where possible)
- Use consistent column ordering across similar tables

### 5. Cross-chapter references

Cross-references should follow this format:
- `> [!TIP]` for cross-references
- Format: `**Cross-Reference:** For a deeper dive into X, see Chapter Y: Title.`
- Be accurate (referenced chapter must exist and contain the claimed content)

### 6. Diagram references

Diagrams should be referenced as:
- Inline SVG: `![Description](../dayX/diagrams/filename.svg)`
- Excalidraw inline (≤6 elements): `![Description](diagrams/chNN-name.excalidraw.png)`
- Excalidraw companion repo (>6 elements): `> See the companion repo for... [link](url)`

Excalidraw rules:
- ≤6 visual elements → inline in book as `book/diagrams/chNN-name.excalidraw.png`
- >6 visual elements → companion repo at `building-with-llms-companion/diagrams/chNN-name.excalidraw.png`
- Use hand-drawn/sketch style
- Color-code meaningfully: green = good/success, red = bad/fail, blue = neutral/info

All diagram paths must be valid files.

---

## Book-Specific Formatting Rules

### 7. No horizontal rules as section dividers

Do not use `---` to separate sections. Use headings instead. Horizontal rules are only allowed within code blocks (as delimiters in prompt examples).

### 8. Bold usage in chapters

Bold is allowed in:
- Headings (handled by `#` syntax)
- Table headers and first-column labels
- Definition-style list items (the defined term)
- Admonition labels (e.g., "**Did You Know?**")

Not allowed: bolding random words for emphasis within a sentence or paragraph.

### 9. List discipline

Use bulleted lists for 3+ parallel items. For 2 items, write them as a sentence with "and" or "or". Do not use a list to present a single argument broken across bullets.

### 10. Paragraph structure

- One idea per paragraph
- Short paragraphs (3-5 sentences max)
- If a paragraph covers two ideas, split it

### 11. Comparison tables

Include at least one comparison table per chapter with format:
```markdown
| Approach | Pros | Cons | When to Use |
|:---------|:-----|:-----|:------------|
```

### 12. Knowledge Check format

Knowledge Check sections should:
- Have exactly 5 questions mixing: multiple choice, true/false, fill-in-the-blank, scenario
- Use numbered questions (1., 2., 3., etc.)
- Include multiple choice options in parentheses: `(a) option (b) option (c) option (d) option`
- For true/false questions: format as "**True or false:** statement"
- For fill-in-the-blank: format as "**Fill in the blank:** ______ in the sentence"
- Hide answers using `<details>` tags:
```markdown
<details>
<summary><strong>Click to Reveal Answers</strong></summary>

1. **Answer** - Explanation.
2. ...

</details>
```

---

## LLM-Tell Detection Checklist

When reviewing, scan for these patterns and flag each:

| Pattern | Category | Fix |
|:--------|:---------|:----|
| `—` anywhere | em dash | Replace with comma, period, or parentheses |
| `–` anywhere | en dash | Replace with hyphen or "to" |
| "not just X, it's Y" | antithesis | Rewrite directly |
| "It's worth noting" | hedging | Delete the filler, keep the point |
| "In essence" / "At its core" | hedging | Delete |
| "Furthermore" / "Moreover" | hedging | Delete or replace with a real transition |
| Random **bold** mid-sentence | bold abuse | Remove bold, rewrite if needed |
| "powerful", "game-changing", "revolutionary" | hyperbole | Use specific language instead |
| "Let's dive in" / "Let's explore" | LLM opener | Delete or replace with the actual topic |
| "In today's world" / "In the ever-evolving" | cliche opener | Delete, start with the subject |
| `---` as section divider | horizontal rule abuse | Remove, use headings instead |
| Missing required section | structure gap | Add the missing section |
| Invalid cross-reference | reference error | Fix or remove the reference |
| Paragraph > 5 sentences | paragraph length | Split into shorter paragraphs |
| Missing comparison table | content gap | Add at least one comparison table |
| Word count outside 3,000-5,000 | length issue | Adjust content length |

---

## Part 2: Reference Integrity

### 2.1 File Existence

For every file path mentioned in chapters, verify the file exists:
- Diagram files (`day*/diagrams/*.svg`)
- Exercise files in companion repo (`building-with-llms-companion/exercises/ch*/...`)
- Cross-referenced chapters (`book/XX-chapter-title.md`)
- Shared code references (`shared/llm_client.py`)

### 2.2 Cross-Chapter References

When a chapter references content from another chapter, verify:
- The referenced chapter exists
- The chapter number is correct
- The description matches what the referenced chapter actually contains

### 2.3 Diagram References

- Every SVG image link must point to an existing file
- Every Excalidraw placeholder should have a corresponding PNG in `book/diagrams/` or the companion repo
- Mermaid diagram references should point to existing `.svg` files

### Flag Format

```
[REF] file:line — "referenced path" → missing or mismatched
```

---

## Part 3: Content Consistency

### 3.1 Opening Story Validation

- Must be 2-3 paragraphs
- Must be factual or clearly hypothetical ("Imagine...")
- Must connect naturally to the chapter topic
- Must end with a sentence that scopes the chapter: "In this chapter, you will learn..."
- No filler or fluff; every sentence earns its place

### 3.2 Terminology Consistency

Verify that the same concept uses the same term throughout all chapters:
- "context window" vs "context length"
- "prompt injection" vs "prompt hijacking"
- API parameter names should be consistent across all chapters

### 3.3 Learning Progression

Check that concepts are introduced before they are used:
- No chapter should reference a technique that hasn't been explained in an earlier chapter
- Cross-references should point backward (to earlier chapters) or forward (to later chapters) appropriately

### 3.4 Code Consistency

- Code examples should use the same function signatures as `shared/llm_client.py`
- Import statements should reference packages from `requirements.txt`
- Variable naming should be consistent across code examples
- All inline examples must be immediately runnable (include imports)

---

## Output Format

### Per-File Report

For each reviewed file, produce:

```
## file-path

### Formatting Issues
- [FORMAT] line N — pattern description

### Structure Issues
- [STRUCT] section description

### References
- [REF] line N — ...

### Consistency
- [CONSIST] term inconsistency

### Verdict: clean / N issues found
```

### Summary Table

After all files, produce:

| Chapter | Structure | Formatting | References | Consistency | Issues |
|:--------|:---------|:-----------|:-----------|:------------|:-------|
| 1 | clean | clean | clean | clean | 0 |
| 2 | missing section | 2 issues | clean | 1 issue | 3 |

---

## How to Run This Review

1. Specify which chapters or files to review (e.g., `book/05-prompt-fundamentals.md` or `book/`)
2. For each file, list every violation with line number, category, and the offending text
3. Provide the corrected version for each violation
4. After listing violations, apply fixes if the user approves

---

## Scope

This workflow applies to all files under:

- `book/*.md` (chapters, front matter, back matter)
- `book/cover-info/*.md`
- `book/appendix-*.md`

---

## Reference Files

These files are the source of truth for validation:

- **Book structure:** `book/builder/book-order.json`
- **LLM client interface:** `shared/llm_client.py`
- **Dependencies:** `requirements.txt`
- **Companion exercises:** External repo `building-with-llms-companion`
