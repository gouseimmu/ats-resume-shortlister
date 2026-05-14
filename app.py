import streamlit as st
import pdfplumber
import docx
import pandas as pd
import re

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="ATS Resume Shortlister",
    page_icon="📄",
    layout="wide"
)

# -----------------------------------
# CUSTOM CSS
# -----------------------------------
st.markdown("""
<style>

.block-container {
    padding-top: 1.5rem;
    max-width: 1400px;
}

.stButton button {
    width: 100%;
    height: 50px;
    border-radius: 12px;
    font-size: 18px;
    font-weight: 600;
    background-color: #4CAF50;
    color: white;
}

.stDownloadButton button {
    width: 100%;
    border-radius: 12px;
}

.metric-card {
    background-color: #f8f9fa;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #ddd;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# CLEAN TEXT
# -----------------------------------
def clean_text(text):

    text = text.lower()

    text = re.sub(
        r'[^a-z0-9\s\.\+\-]',
        ' ',
        text
    )

    text = re.sub(
        r'\s+',
        ' ',
        text
    )

    return text


# -----------------------------------
# READ PDF
# -----------------------------------
def read_pdf(uploaded_file):

    text = ""

    with pdfplumber.open(uploaded_file) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


# -----------------------------------
# READ DOCX
# -----------------------------------
def read_docx(uploaded_file):

    doc = docx.Document(uploaded_file)

    return "\n".join(
        [p.text for p in doc.paragraphs]
    )


# -----------------------------------
# EXTRACT ROLE
# -----------------------------------
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


# -----------------------------------
# EXTRACT EXPERIENCE
# -----------------------------------
def extract_required_experience(jd_text):

    jd_text = clean_text(jd_text)

    match = re.search(
        r'(\d+(\.\d+)?)\s*\+?\s*(years|year)',
        jd_text
    )

    return float(match.group(1)) if match else 0.0


# -----------------------------------
# EXTRACT SKILLS
# -----------------------------------
def extract_skills(jd_text):

    jd_text = clean_text(jd_text)

    common_skills = [

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
        "azure data factory",
        "adf",
        "databricks",
        "pyspark",
        "synapse",
        "data modeling",
        "power query",
        "git",
        "tableau",
        "qlik sense",
        "java",
        "react"
    ]

    return [
        s for s in common_skills
        if s in jd_text
    ]


# -----------------------------------
# EXPERIENCE EXTRACTION
# -----------------------------------
def extract_experience_years(text):

    text = clean_text(text)

    matches = re.findall(
        r'(\d+(\.\d+)?)(\+)?\s*(years|year)',
        text
    )

    years = [
        float(m[0])
        for m in matches
    ]

    return max(years) if years else 0


# -----------------------------------
# SCORE RESUME
# -----------------------------------
def score_resume(
    resume_text,
    skills,
    jd_text,
    required_exp
):

    resume_text = clean_text(resume_text)

    jd_text = clean_text(jd_text)

    matched = [
        s for s in skills
        if s in resume_text
    ]

    unmatched = [
        s for s in skills
        if s not in resume_text
    ]

    # Skill score
    skill_score = (
        (len(matched) / len(skills)) * 50
        if skills else 0
    )

    # JD similarity
    jd_words = set(jd_text.split())

    resume_words = set(resume_text.split())

    jd_score = (
        (len(jd_words & resume_words) / len(jd_words)) * 30
        if jd_words else 0
    )

    # Experience score
    resume_exp = extract_experience_years(resume_text)

    if required_exp == 0:

        exp_score = 20

    else:

        exp_score = min(
            (resume_exp / required_exp) * 20,
            20
        )

    total = (
        skill_score +
        jd_score +
        exp_score
    )

    return (
        round(total, 2),
        matched,
        unmatched,
        int(resume_exp)
    )


# -----------------------------------
# STATUS
# -----------------------------------
def get_status(score):

    if score >= 80:
        return "🟢 Excellent"

    elif score >= 65:
        return "🟡 Good"

    elif score >= 50:
        return "🟠 Average"

    else:
        return "🔴 Weak"


# -----------------------------------
# ROW COLORS
# -----------------------------------
def color_rows(row):

    if "🟢" in row["Status"]:

        return ["background-color: #c8f7c5"] * len(row)

    elif "🟡" in row["Status"]:

        return ["background-color: #fff3b0"] * len(row)

    elif "🟠" in row["Status"]:

        return ["background-color: #ffe5b4"] * len(row)

    else:

        return ["background-color: #ffb3b3"] * len(row)


# -----------------------------------
# HEADER
# -----------------------------------
st.title("📄 ATS Resume Shortlister")

st.caption(
    "AI Powered Resume Screening & Ranking System"
)

st.divider()

# -----------------------------------
# SIDEBAR
# -----------------------------------
with st.sidebar:

    st.title("⚡ ATS Dashboard")

    st.success("Professional AI Resume Analyzer")

    st.markdown("---")

    st.markdown("""
    ### Features

    ✅ ATS Resume Scoring  
    ✅ Skill Match %  
    ✅ Resume Ranking  
    ✅ Experience Analysis  
    ✅ Resume Strength  
    ✅ Recruiter Recommendation  
    ✅ CSV Export  
    """)

# -----------------------------------
# JOB DESCRIPTION
# -----------------------------------
st.subheader("📌 Upload Job Description")

jd_file = st.file_uploader(
    "Upload JD PDF",
    type=["pdf"]
)

jd_text = ""
role = ""
exp = 0
skills = []

if jd_file:

    jd_text = read_pdf(jd_file)

    role = extract_role(jd_text)

    exp = extract_required_experience(jd_text)

    skills = extract_skills(jd_text)

    st.success("✅ JD Loaded Successfully")

st.divider()

# -----------------------------------
# POSITION DETAILS
# -----------------------------------
st.subheader("💼 Position Details")

col1, col2 = st.columns(2)

with col1:

    role = st.text_input(
        "Position Title",
        value=role
    )

with col2:

    exp = st.slider(
        "Required Experience",
        0,
        20,
        int(exp)
    )

# -----------------------------------
# SKILLS
# -----------------------------------
skill_options = [

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
    "azure data factory",
    "adf",
    "databricks",
    "pyspark",
    "synapse",
    "data modeling",
    "power query",
    "git",
    "tableau",
    "qlik sense",
    "java",
    "react"
]

skills = st.multiselect(
    "Required Skills",
    skill_options,
    default=skills
)

st.divider()

# -----------------------------------
# RESUME UPLOAD
# -----------------------------------
st.subheader("📤 Upload Resumes")

resumes = st.file_uploader(
    "Upload Multiple Resumes",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

st.divider()

# -----------------------------------
# ANALYZE BUTTON
# -----------------------------------
if st.button("🚀 Analyze Resumes"):

    if not jd_file:

        st.error("Please upload Job Description")

    elif not resumes:

        st.error("Please upload resumes")

    else:

        results = []

        for r in resumes:

            text = (
                read_pdf(r)
                if r.name.endswith(".pdf")
                else read_docx(r)
            )

            score, matched, unmatched, exp_r = score_resume(
                text,
                skills,
                jd_text,
                exp
            )

            # Skill Match %
            skill_match_percent = round(
                (len(matched) / len(skills)) * 100,
                2
            ) if skills else 0

            # Experience Gap
            exp_gap = exp_r - exp

            # Resume Strength
            if score >= 85:
                strength = "Excellent"

            elif score >= 70:
                strength = "Strong"

            elif score >= 50:
                strength = "Moderate"

            else:
                strength = "Weak"

            # Recommendation
            if score >= 75:
                recommendation = "Recommended"

            elif score >= 55:
                recommendation = "Consider"

            else:
                recommendation = "Rejected"

            status = get_status(score)

            results.append({

                "Rank": 0,

                "Resume": r.name,

                "Score": score,

                "Skill Match %": skill_match_percent,

                "Experience": exp_r,

                "Experience Gap": exp_gap,

                "Resume Strength": strength,

                "Recommendation": recommendation,

                "Matched Skills": ", ".join(matched),

                "Missing Skills": ", ".join(unmatched),

                "Status": status
            })

        # -----------------------------------
        # DATAFRAME
        # -----------------------------------
        df = pd.DataFrame(results)

        df = df.sort_values(
            "Score",
            ascending=False
        ).reset_index(drop=True)

        df["Rank"] = range(
            1,
            len(df) + 1
        )

        # -----------------------------------
        # ANALYTICS
        # -----------------------------------
        st.subheader("📊 ATS Analytics")

        eligible = len(
            df[df["Score"] >= 75]
        )

        avg_score = round(
            df["Score"].mean(),
            2
        )

        top_score = round(
            df["Score"].max(),
            2
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Total Resumes",
            len(df)
        )

        col2.metric(
            "Eligible",
            eligible
        )

        col3.metric(
            "Average Score",
            avg_score
        )

        col4.metric(
            "Top Score",
            top_score
        )

        st.divider()

        # -----------------------------------
        # FILTERS
        # -----------------------------------
        st.subheader("🔍 Filters")

        filter_score = st.slider(
            "Minimum ATS Score",
            0,
            100,
            50
        )

        filtered_df = df[
            df["Score"] >= filter_score
        ]

        # -----------------------------------
        # CHART
        # -----------------------------------
        st.subheader("📈 Score Distribution")

        chart_df = filtered_df.set_index("Resume")

        st.bar_chart(chart_df["Score"])

        st.divider()

        # -----------------------------------
        # RESULTS
        # -----------------------------------
        st.subheader("🏆 Resume Ranking Results")

        styled_df = (
            filtered_df.style
            .apply(color_rows, axis=1)
            .format({

                "Score": "{:.2f}",

                "Skill Match %": "{:.0f}%",

                "Experience": "{:.0f}",

                "Experience Gap": "{:+.0f}"
            })
        )

        st.dataframe(
            styled_df,
            use_container_width=True,
            height=600,
            hide_index=True
        )

        # -----------------------------------
        # DOWNLOAD
        # -----------------------------------
        csv = filtered_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "⬇ Download ATS Report",
            csv,
            "resume_scores.csv",
            "text/csv",
            use_container_width=True
        )