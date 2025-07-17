import re

def parse_resume(text):
    # Basic extraction logic using keyword matching
    experience = 0
    education = "1"  # Default Bachelor
    role = "1"       # Default Software Engineer

    # Extract years of experience
    match = re.search(r'(\d+)\+?\s+years? of experience', text, re.I)
    if match:
        experience = int(match.group(1))

    # Check for education level
    if re.search(r'\bmaster', text, re.I):
        education = "2"
    elif re.search(r'ph\.?d', text, re.I):
        education = "3"

    # Check for job role
    if re.search(r'data scientist', text, re.I):
        role = "2"
    elif re.search(r'manager', text, re.I):
        role = "3"
    elif re.search(r'devops', text, re.I):
        role = "4"
    elif re.search(r'ml engineer|ai engineer', text, re.I):
        role = "6"

    return {
        "experience": experience,
        "education_level": education,
        "role": role
    }
