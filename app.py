import streamlit as st
import pdfplumber
import docx
import pandas as pd
import re

# -------------------------------
# CLEAN TEXT
# -------------------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s\.\+\-]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text

# -------------------------------
# READ PDF
# -------------------------------
def read_pdf(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

# -------------------------------
# READ DOCX
# -------------------------------
def read_docx(uploaded_file):
    doc = docx.Document(uploaded_file)
    return "\n".join([p.text for p in doc.paragraphs])

# -------------------------------
# POSITION TITLE (JD ONLY)
# -------------------------------
def extract_role(jd_text):
    jd_lower = jd_text.lower()

    patterns = [
        r"job title\s*[:\-]\s*(.+)",
        r"position title\s*[:\-]\s*(.+)",
        r"role\s*[:\-]\s*(.+)"
    ]

    for pattern in patterns:
        match = re.search(pattern, jd_lower)
        if match:
            return match.group(1).strip()

    return ""

# -------------------------------
# EXPERIENCE FROM JD
# -------------------------------
def extract_required_experience(jd_text):
    jd_text = clean_text(jd_text)
    match = re.search(r'(\d+(\.\d+)?)\s*\+?\s*(years|year)', jd_text)
    return float(match.group(1)) if match else 0.0

# -------------------------------
# SKILLS FROM JD
# -------------------------------
def extract_skills(jd_text):
    jd_text = clean_text(jd_text)

    common_skills = [
        "power bi", "sql", "dax", "etl", "excel", "ssrs", "ssis", "ssas",
        "python", "azure", "azure data factory", "adf", "databricks",
        "pyspark", "synapse", "data modeling", "power query", "git",
        "tableau", "qlik sense", "java", "spring boot", "react", "angular",
        "microservices", "docker", "kubernetes"
    ]

    return [s for s in common_skills if s in jd_text]

# -------------------------------
# EXPERIENCE FROM RESUME
# -------------------------------
def extract_experience_years(text):
    text = clean_text(text)
    matches = re.findall(r'(\d+(\.\d+)?)(\+)?\s*(years|year)', text)

    years = [float(m[0]) for m in matches]
    return max(years) if years else 0

# -------------------------------
# SCORING ENGINE
# -------------------------------
def score_resume(resume_text, skills, jd_text, required_exp):
    resume_text = clean_text(resume_text)
    jd_text = clean_text(jd_text)

    matched = [s for s in skills if s in resume_text]
    unmatched = [s for s in skills if s not in resume_text]

    # Skill score (50)
    skill_score = (len(matched) / len(skills)) * 50 if skills else 0

    # JD similarity (30)
    jd_words = set(jd_text.split())
    resume_words = set(resume_text.split())
    jd_score = (len(jd_words & resume_words) / len(jd_words)) * 30 if jd_words else 0

    # Experience (20)
    resume_exp = extract_experience_years(resume_text)

    if required_exp == 0:
        exp_score = 20
        exp_match = 100
    else:
        exp_score = min((resume_exp / required_exp) * 20, 20)
        exp_match = min((resume_exp / required_exp) * 100, 100)

    total = skill_score + jd_score + exp_score

    return round(total, 2), matched, unmatched, resume_exp, round(exp_match, 2)

# -------------------------------
# STATUS
# -------------------------------
def get_status(score):
    if score >= 75:
        return "🟢 Eligible"
    elif score >= 50:
        return "🟠 Medium"
    else:
        return "🔴 Not Eligible"

# -------------------------------
# ROW COLOR
# -------------------------------
def color_rows(row):
    if "🟢" in row["Status"]:
        return ["background-color: #c8f7c5"] * len(row)
    elif "🟠" in row["Status"]:
        return ["background-color: #ffe5b4"] * len(row)
    else:
        return ["background-color: #ffb3b3"] * len(row)

# -------------------------------
# STREAMLIT UI
# -------------------------------
st.set_page_config(page_title="Resume Scoring AI", layout="wide")

st.title("📄 AI Resume Scoring System")

# ---------------- JD UPLOAD ----------------
st.subheader("📌 Upload Job Description")

jd_file = st.file_uploader("Upload JD PDF", type=["pdf"])

jd_text = ""
role = ""
exp = 0.0
skills = []

if jd_file:
    jd_text = read_pdf(jd_file)

    role = extract_role(jd_text)
    exp = extract_required_experience(jd_text)
    skills = extract_skills(jd_text)

    st.success("JD Loaded Successfully")

# ---------------- POSITION ----------------
st.subheader("📌 Position Details")

st.text_input("Position Title (from JD)", value=role if role else "Not Found", disabled=True)
st.number_input("Required Experience (Years)", value=exp, disabled=True)

skills_input = st.text_area("Required Skills (comma separated)", value=", ".join(skills))
skills = [s.strip().lower() for s in skills_input.split(",") if s.strip()]

# ---------------- RESUMES ----------------
st.subheader("📤 Upload Resumes")

resumes = st.file_uploader(
    "Upload PDF/DOCX Resumes",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

# ---------------- RUN ----------------
if st.button("🚀 Score Resumes"):

    if not jd_file:
        st.error("Upload JD first")
    elif not resumes:
        st.error("Upload resumes")
    elif len(skills) == 0:
        st.error("Skills missing in JD")
    else:

        results = []

        for r in resumes:

            text = read_pdf(r) if r.name.endswith(".pdf") else read_docx(r)

            score, matched, unmatched, exp_r, exp_match = score_resume(
                text, skills, jd_text, exp
            )

            status = get_status(score)

            results.append({
                "Position Title": role,
                "Resume": r.name,
                "Score": score,
                "Experience": exp_r,
                "Experience Match %": exp_match,
                "Matched Skills": ", ".join(matched),
                "Missing Skills": ", ".join(unmatched),
                "Status": status
            })

        # ---------------- FIX RANKING ISSUE ----------------
        df = pd.DataFrame(results)

        df = df.sort_values("Score", ascending=False).reset_index(drop=True)
        df.insert(0, "Rank", range(1, len(df) + 1))

        st.success("Scoring Completed")

        st.dataframe(df.style.apply(color_rows, axis=1))

        # ---------------- DOWNLOAD ----------------
        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇ Download Report",
            csv,
            "resume_scores.csv",
            "text/csv"
        )