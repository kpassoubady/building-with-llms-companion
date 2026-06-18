import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

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
# Exercise functions
# ---------------------------------------------------------------------------


def extract_resume_data(resume_text):
    """Send the resume to the LLM and return parsed JSON as a Python dict."""
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
    return json.loads(raw.strip())


def parse_and_display(data):
    """Print each extracted field in a readable format."""
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
