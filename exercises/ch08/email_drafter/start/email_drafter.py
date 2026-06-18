"""
Lab 2.6 — Email Drafter Assistant (Prompt Iteration)
Day 2 — Session 4

Goal: Build a tool that drafts a professional customer email based on bullet points.
      Iterate the prompt 3 times based on observed failures.

Instructions:
1. Start with v1 of the prompt. Run it against the 3 samples. Note failures.
2. Improve to v2: fix the most common failure. Test again.
3. Improve to v3: fix the next failure. Test again.
4. Document what changed at each iteration and why.

Run: python3 lab2_6_email_drafter.py
"""

import os
import sys

# Ensure the root of the repo is in the python path
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from shared import get_completion, show_config


# --- Prompt Versions ---
# Iterate on these! Start with v1, observe failures, improve.

PROMPT_V1 = """Write an email based on these notes."""

PROMPT_V2 = """You are a professional customer success manager. Write an email to a customer based on these notes.

Requirements:
- Be polite and concise
- Have a clear call to action
- Do not make up any facts not in the notes"""

PROMPT_V3 = """You are a professional customer success manager drafting an email to a customer.

Draft the email using the following notes and strict rules:
- Structure the email with: 1. Greeting, 2. Acknowledge their situation, 3. Provide the solution, 4. Clear next steps/call to action.
- Keep the email under 150 words.
- Maintain a warm, empathetic, and professional tone.
- Do NOT invent any information, features, or deadlines not explicitly mentioned in the notes.
- Use placeholders like [Your Name] or [Company Name] where appropriate.

Respond in this exact format:

### Drafted Email
<your email draft here>

### Tone and Structure Analysis
<briefly explain how the email meets the criteria>"""


# Bullet point notes to draft into emails
SAMPLES = [
    {
        "name": "API Rate Limit Issue",
        "notes": '''
- Customer: Acme Corp
- Issue: API rate limit exceeded
- Solution: Upgrade to Pro plan or optimize API calls
- Next step: Schedule a 15-min call to discuss
''',
    },
    {
        "name": "Missing Export Button",
        "notes": '''
- Customer: John Doe
- Issue: Can't find the export button in the new UI
- Solution: It has moved under Settings -> Data -> Export
- Next step: Let us know if they need further help
''',
    },
    {
        "name": "Dashboard Performance Bug",
        "notes": '''
- Customer: BetaTesters Inc.
- Issue: The new dashboard is loading very slowly
- Solution: We deployed a hotfix today that resolves the issue
- Next step: Ask them to refresh their browser and verify if the speed has improved
''',
    },
]


def draft_email(notes, prompt_version, version_label):
    """Send notes to the LLM for email drafting using the specified prompt version."""
    # TODO: Implement this function
    # 1. Create messages with the prompt version as system and notes as user
    # 2. Call get_completion with temperature=0.7 (some creativity is good for writing)
    # 3. Return the response

    return "⚠️ TODO: Implement the draft_email function!"


def run_iteration(prompt_version, version_label):
    """Run a prompt version against all samples."""
    print(f"\n{'='*70}")
    print(f"🔄 Prompt Version: {version_label}")
    print(f"{'='*70}")

    for sample in SAMPLES:
        print(f"\n📝 Drafting for: {sample['name']}")
        print(f"{'─'*50}")
        print(f"Notes:\n{sample['notes']}")
        print(f"{'─'*50}")

        result = draft_email(sample["notes"], prompt_version, version_label)
        print(f"Result:\n{result}")
        print(f"{'='*70}")


def main():
    show_config()
    print("\n📧 Email Drafter Assistant — Lab 2.6")
    print("Running 3 iterations of prompt improvement\n")

    # Iteration 1: Basic prompt
    print(">>> ITERATION 1: Basic prompt (observe what fails)")
    run_iteration(PROMPT_V1, "v1 - Basic")

    # Iteration 2: Improved prompt
    print("\n>>> ITERATION 2: Added structure and rules")
    run_iteration(PROMPT_V2, "v2 - Structured")

    # Iteration 3: Refined prompt
    print("\n>>> ITERATION 3: Strict format and detailed rules")
    run_iteration(PROMPT_V3, "v3 - Detailed")

    # Analysis prompt
    print(f"\n{'='*70}")
    print("📊 Your Analysis:")
    print("   Compare the 3 iterations:")
    print("   - v1: What was missing? What failed?")
    print("   - v2: What improved? What still failed?")
    print("   - v3: What improved? Is it good enough to ship?")
    print("   - What would v4 look like?")
    print(f"{'='*70}")

    print("\n✅ Lab 2.6 complete!")


if __name__ == "__main__":
    main()
