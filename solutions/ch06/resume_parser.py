"""
Exercise: Resume Parser
Chapter 6: Prompting Techniques

Goal: Extract structured data from a plain-text resume using a JSON output
prompt, then parse and display each field cleanly.

Skills practiced:
- Structured output prompting (JSON schema in prompt)
- Parsing and validating model-returned JSON
- Role prompting (HR data-extraction assistant)
- Handling optional or missing fields gracefully

Instructions:
1. Implement extract_resume_data() to prompt the model for JSON output.
2. Implement parse_and_display() to parse the JSON and print each field.
3. Run main() and verify the extracted fields match the sample resume.
4. Try replacing SAMPLE_RESUME with your own resume text and re-run.

Run: python solutions/ch06/resume_parser.py  (from the repo root)
"""

import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from shared import get_completion

# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

SAMPLE_RESUME = """
Alex Rivera
alex.rivera@example.com | (555) 234-7890 | linkedin.com/in/alexrivera

SUMMARY
Software engineer with 6 years of experience building backend services and APIs.

SKILLS
Python, Go, PostgreSQL, Redis, Docker, Kubernetes, REST APIs, gRPC

EXPERIENCE
Senior Software Engineer - Acme Corp (2021 - Present)
  - Designed a microservices platform handling 50k requests/second
  - Reduced deployment time by 40% by introducing GitOps workflows

Software Engineer - Startup XYZ (2018 - 2021)
  - Built a real-time notification service in Go serving 1M daily users

EDUCATION
B.S. Computer Science - State University, 2018
"""

EXPECTED_SCHEMA = {
    "name": "string",
    "email": "string",
    "skills": ["list of strings"],
    "years_experience": "integer",
    "last_role": "string",
}


# ---------------------------------------------------------------------------
# Solution functions
# ---------------------------------------------------------------------------


def extract_resume_data(resume_text):
    """Send the resume to the LLM and return parsed JSON as a Python dict.

    Args:
        resume_text: Plain-text resume string.

    Returns:
        Dict with keys: name, email, skills, years_experience, last_role.
    """
    schema_str = json.dumps(EXPECTED_SCHEMA, indent=2)
    system = (
        "You are an HR data extraction assistant.\n"
        "Extract resume data and return ONLY valid JSON with these fields:\n"
        + schema_str
        + "\nFor years_experience, count total years across all roles."
        + "\nReturn nothing outside the JSON object."
    )
    raw = get_completion(
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": resume_text},
        ],
        tier="default",
        temperature=0.0,
    )
    text = raw.strip()
    # Strip markdown fences if present
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text[3:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
    return json.loads(text)


def parse_and_display(data):
    """Print each extracted field in a readable format.

    Args:
        data: Dict returned by extract_resume_data().
    """
    print(f"Name:             {data.get('name', 'N/A')}")
    print(f"Email:            {data.get('email', 'N/A')}")
    print(f"Skills:           {', '.join(data.get('skills', []))}")
    print(f"Years experience: {data.get('years_experience', 'N/A')}")
    print(f"Last role:        {data.get('last_role', 'N/A')}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    print("Chapter 6 - Resume Parser\n")
    print("Extracting data from sample resume...")
    data = extract_resume_data(SAMPLE_RESUME)
    print("\nExtracted fields:")
    print("-" * 40)
    parse_and_display(data)
    print("\nRaw JSON returned:")
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()


# Expected output (illustrative):
# Extracting data from sample resume...
#
# Extracted fields:
# ----------------------------------------
# Name:             Alex Rivera
# Email:            alex.rivera@example.com
# Skills:           Python, Go, PostgreSQL, Redis, Docker, Kubernetes, REST APIs, gRPC
# Years experience: 6
# Last role:        Senior Software Engineer - Acme Corp
