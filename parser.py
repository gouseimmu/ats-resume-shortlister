import os
import re
from collections import Counter

from utils import COMMON_SKILLS, clean_text, extract_contact_info, extract_experience


EMPLOYMENT_TYPES = [
    "Full-time",
    "Part-time",
    "Contract",
    "Permanent",
    "Internship",
    "Temporary",
    "Remote",
    "Hybrid",
]


JOB_TITLE_HINTS = [
    "developer",
    "engineer",
    "analyst",
    "architect",
    "manager",
    "consultant",
    "specialist",
    "administrator",
    "lead",
    "scientist",
]


NAME_STOPWORDS = {
    "resume",
    "curriculum",
    "vitae",
    "cv",
    "profile",
    "email",
    "phone",
    "mobile",
    "contact",
    "address",
    "linkedin",
    "github",
    "portfolio",
    "summary",
    "objective",
    "experience",
    "education",
    "skills",
    "project",
    "projects",
}


def normalize_lines(text):
    return [re.sub(r"\s+", " ", line).strip() for line in (text or "").splitlines() if line.strip()]


def extract_experience_range(text):
    text_low = (text or "").lower()
    range_patterns = [
        r"(\d{1,2})\s*(?:to|-|–|—)\s*(\d{1,2})\s*\+?\s*(?:years?|yrs?)",
        r"experience\s*[:\-]?\s*(\d{1,2})\s*(?:to|-|–|—)\s*(\d{1,2})",
        r"(\d{1,2})\s*\+\s*(?:years?|yrs?)",
    ]
    for pattern in range_patterns:
        match = re.search(pattern, text_low)
        if match and len(match.groups()) >= 2:
            start, end = int(match.group(1)), int(match.group(2))
            return (min(start, end), max(start, end))
        if match:
            years = int(match.group(1))
            return (years, min(years + 3, 25))

    years = extract_experience(text_low)
    return (years, min(years + 3, 25)) if years else (2, 5)


def _line_after_label(lines, labels):
    label_re = "|".join(re.escape(label) for label in labels)
    pattern = re.compile(rf"^(?:{label_re})\s*[:\-]\s*(.+)$", re.I)
    for line in lines:
        match = pattern.search(line)
        if match:
            return match.group(1).strip()
    return ""


def extract_job_title(text):
    lines = normalize_lines(text)
    labelled = _line_after_label(lines[:25], ["job title", "role", "position", "designation"])
    if labelled:
        return labelled[:80]

    for line in lines[:18]:
        low = line.lower()
        if any(hint in low for hint in JOB_TITLE_HINTS) and len(line.split()) <= 9:
            return re.sub(r"^(we are hiring|hiring for|opening for)\s+", "", line, flags=re.I)[:80]

    return "Auto Parsed Role"


def extract_location(text):
    lines = normalize_lines(text)
    labelled = _line_after_label(lines, ["location", "job location", "work location"])
    if labelled:
        return labelled[:90]

    match = re.search(r"\b(?:remote|hybrid|onsite|on-site)\b(?:\s*[-,]\s*[A-Za-z ,]+)?", text or "", re.I)
    return match.group(0).strip().title() if match else "Not specified"


def extract_employment_type(text):
    text_low = (text or "").lower()
    for option in EMPLOYMENT_TYPES:
        if re.search(rf"\b{re.escape(option.lower())}\b", text_low):
            return option
    return "Not specified"


def extract_notice_period(text):
    match = re.search(r"notice\s*period\s*[:\-]?\s*([A-Za-z0-9\s+\-]+?)(?:\.|\n|,|$)", text or "", re.I)
    if match:
        return match.group(1).strip()[:60]
    return "Not specified"


def extract_section_items(text, headings, max_items=7):
    lines = normalize_lines(text)
    heading_re = re.compile(rf"^({'|'.join(re.escape(h) for h in headings)})\s*[:\-]?$", re.I)
    stop_re = re.compile(r"^(requirements|qualifications|skills|experience|education|benefits|about|location|employment|responsibilities|role|summary)\b", re.I)
    collecting = False
    items = []

    for line in lines:
        if heading_re.search(line):
            collecting = True
            continue
        if collecting and stop_re.search(line) and len(items) > 0:
            break
        if collecting:
            clean = re.sub(r"^[\-•*\d.)\s]+", "", line).strip()
            if clean and len(clean) > 12:
                items.append(clean[:180])
        if len(items) >= max_items:
            break
    return items


def parse_job_description(text):
    skills = extract_skills_by_frequency(text)
    primary = skills[:6]
    secondary = skills[6:14]
    return {
        "job_title": extract_job_title(text),
        "experience_range": extract_experience_range(text),
        "required_skills": skills,
        "primary_skills": primary,
        "secondary_skills": secondary,
        "location": extract_location(text),
        "employment_type": extract_employment_type(text),
        "responsibilities": extract_section_items(text, ["responsibilities", "key responsibilities", "what you will do"]),
        "notice_period": extract_notice_period(text),
    }


def extract_skills_by_frequency(text):
    cleaned = clean_text(text)
    found = []
    for skill in COMMON_SKILLS:
        if re.search(rf"\b{re.escape(skill)}\b", cleaned):
            found.append(skill)

    counts = Counter()
    for skill in found:
        counts[skill] = cleaned.count(skill)
    return [skill for skill, _ in counts.most_common()] or found


def _looks_like_person_name(line):
    if not line or len(line) > 70:
        return False
    if any(token in line.lower() for token in NAME_STOPWORDS):
        return False
    if re.search(r"[@:/\\]|www\.|\.com|\d", line.lower()):
        return False
    words = [w for w in re.split(r"\s+", line.strip()) if w]
    if not 2 <= len(words) <= 5:
        return False
    valid_words = 0
    for word in words:
        clean = re.sub(r"[^A-Za-z]", "", word)
        if len(clean) < 2:
            continue
        if clean[0].isupper() or clean.isupper():
            valid_words += 1
    return valid_words >= max(2, len(words) - 1)


def extract_candidate_name(text, filename="", email=""):
    lines = normalize_lines(text)
    header_lines = lines[:12]

    uppercase_candidates = []
    title_candidates = []
    for line in header_lines:
        compact = re.sub(r"\s+", " ", line).strip()
        if _looks_like_person_name(compact):
            if compact.isupper():
                uppercase_candidates.append(compact.title())
            else:
                title_candidates.append(compact)

    if uppercase_candidates:
        return uppercase_candidates[0]
    if title_candidates:
        return title_candidates[0]

    if email and "@" in email and email.lower() not in {"not found", "n/a"}:
        username = email.split("@")[0]
        username = re.sub(r"[\d_]+", " ", username)
        words = [w.capitalize() for w in re.split(r"[.\-\s]+", username) if len(w) > 1]
        if len(words) >= 2:
            return " ".join(words[:4])

    base = os.path.splitext(os.path.basename(filename or ""))[0]
    base = re.sub(r"(?i)\b(resume|cv|updated|latest|final|profile)\b", " ", base)
    base = re.sub(r"[_\-.]+", " ", base)
    base = re.sub(r"\d+", " ", base)
    words = [w.capitalize() for w in base.split() if len(w) > 1]
    return " ".join(words[:5]) if words else "Unknown Candidate"


def parse_resume_identity(text, filename=""):
    contact = extract_contact_info(text)
    name = extract_candidate_name(text, filename, contact.get("email", ""))
    return {
        "name": name,
        "email": contact.get("email", "Not Found"),
        "phone": contact.get("phone", "Not Found"),
    }

