import re
import pdfplumber
import docx

COMMON_SKILLS = [
    "power bi",
    "sql",
    "dax",
    "etl",
    "excel",
    "ssrs",
    "ssis",
    "ssas",
    "python",
    "azure",
    "adf",
    "databricks",
    "pyspark",
    "synapse",
    "power query",
    "data modeling",
    "tableau",
    "qlik sense",
    "git"
]

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s\+\.]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text


def read_pdf(file):
    text = ""

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"

    return text


def read_docx(file):
    doc = docx.Document(file)
    return "\n".join([p.text for p in doc.paragraphs])


def extract_experience(text):
    text = clean_text(text)

    patterns = [
        r'(\d+)\+?\s*years',
        r'(\d+)\+?\s*year',
        r'(\d+)\+?\s*yrs',
        r'(\d+)\+?\s*yr',
        r'over\s*(\d+)\s*years',
        r'experience\s*[:\-]?\s*(\d+)'
    ]

    years = []

    for pattern in patterns:
        matches = re.findall(pattern, text)

        for match in matches:
            try:
                years.append(int(match))
            except:
                pass

    return max(years) if years else 0


def extract_skills(text):
    text = clean_text(text)

    return [
        skill for skill in COMMON_SKILLS
        if skill in text
    ]