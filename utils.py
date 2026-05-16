import re
import pdfplumber
import docx

COMMON_SKILLS = [
    "power bi", "sql", "dax", "etl", "excel", "ssrs", "ssis", "ssas", 
    "python", "azure", "adf", "databricks", "pyspark", "synapse", 
    "power query", "data modeling", "tableau", "qlik sense", "git",
    "aws", "gcp", "snowflake", "airflow", "dbt", "spark", "hadoop",
    "java", "javascript", "typescript", "react", "node.js", "django",
    "flask", "fastapi", "docker", "kubernetes", "terraform", "linux",
    "machine learning", "nlp", "statistics", "stakeholder management",
    "agile", "scrum", "jira"
]

def clean_text(text):
    """
    Normalizes text by lowercasing and removing non-alphanumeric characters.
    """
    if not text: return ""
    text = text.lower()
    # Keep '.' and '+' for tech terms like C++ or .NET
    text = re.sub(r'[^a-z0-9\s\+\.]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text

def read_pdf(file):
    """Extracts text from a PDF file object."""
    text = ""
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                content = page.extract_text()
                if content:
                    text += content + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def read_docx(file):
    """Extracts text from a DOCX file object."""
    try:
        doc = docx.Document(file)
        return "\n".join([p.text for p in doc.paragraphs])
    except Exception as e:
        print(f"Error reading DOCX: {e}")
        return ""

def extract_experience(text):
    """
    Improved extraction logic to identify years of experience.
    Specifically optimized for double-digit years like 10+.
    """
    # Use lowercase but preserve structure for regex context
    text_low = text.lower()
    
    patterns = [
        r'(\d{1,2})\s*\+?\s*(?:years?|yrs?|yr)\b', # Handles "10 years", "10+ yrs"
        r'(?:total|overall|relevant)\s*(?:exp|experience)\s*[:\-]?\s*(\d{1,2})', # Handles "total exp: 10"
        r'(\d{1,2})\s*(?:years?|yrs?)\s*(?:of)?\s*experience' # Handles "10 years of experience"
    ]
    
    found_years = []
    for pattern in patterns:
        matches = re.findall(pattern, text_low)
        for match in matches:
            if match.isdigit():
                found_years.append(int(match))
    
    # Returns the maximum numerical value found as the experience level
    return max(found_years) if found_years else 0

def extract_skills(text):
    """Identifies skills from the COMMON_SKILLS list within the text."""
    cleaned_text = clean_text(text)
    return [
        skill for skill in COMMON_SKILLS
        if re.search(rf"\b{re.escape(skill)}\b", cleaned_text)
    ]
def extract_contact_info(text):
    """
    Extracts email and phone number from raw resume text using regex.
    """
    # Email Regex: standard pattern for user@domain.com
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    
    # Phone Regex: handles +1, (123), 123-456, and spaces
    phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    
    email_match = re.search(email_pattern, text)
    phone_match = re.search(phone_pattern, text)
    
    return {
        "email": email_match.group(0) if email_match else "Not Found",
        "phone": phone_match.group(0) if phone_match else "Not Found"
    }
