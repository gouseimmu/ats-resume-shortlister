import streamlit as st
import pandas as pd
import time

from utils import (
    read_pdf,
    read_docx,
    extract_experience,
    extract_skills,
    COMMON_SKILLS
)

from ats_engine import score_resume
from charts import score_chart, eligibility_chart
from styles import load_css
from ui_components import hero_section, sidebar_panel

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="TalentIQ ATS",
    page_icon="assets/logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# SESSION STATE
# =========================================================

if "results_df" not in st.session_state:
    st.session_state.results_df = None

# =========================================================
# LOAD CSS
# =========================================================

load_css()

# =========================================================
# SIDEBAR
# =========================================================

sidebar_panel()

# =========================================================
# HERO SECTION
# =========================================================

hero_section()

# =========================================================
# MAIN LAYOUT
# =========================================================

left, right = st.columns([3,1])

# =========================================================
# LEFT PANEL
# =========================================================

with left:

    st.subheader("📌 Upload Job Description")

    jd_file = st.file_uploader(
        "Upload JD PDF",
        type=["pdf"],
        key="jd_upload"
    )

    jd_text = ""
    role = ""
    required_exp = 0
    skills = []

    if jd_file:

        jd_text = read_pdf(jd_file)

        role_patterns = [
            "power bi developer",
            "data analyst",
            "sql developer",
            "python developer",
            "data engineer"
        ]

        for r in role_patterns:
            if r in jd_text.lower():
                role = r.title()

        required_exp = extract_experience(jd_text)
        skills = extract_skills(jd_text)

        st.success("JD Parsed Successfully")

    st.subheader("💼 Position Details")

    c1, c2 = st.columns(2)

    with c1:
        role = st.text_input(
            "Role",
            value=role
        )

    with c2:
        required_exp = st.slider(
            "Required Experience",
            0,
            20,
            int(required_exp)
        )

    skills = st.multiselect(
        "Required Skills",
        COMMON_SKILLS,
        default=skills
    )

    st.subheader("📤 Upload Resumes")

    resumes = st.file_uploader(
        "Upload Multiple Resumes",
        type=["pdf", "docx"],
        accept_multiple_files=True,
        key="resume_upload"
    )

# =========================================================
# RIGHT PANEL
# =========================================================

with right:

    st.subheader("📊 Hiring Stats")

    st.metric("Open Positions", "3")
    st.metric("Applied", "128")
    st.metric("Interviews", "12")
    st.metric("Offers", "4")

    st.divider()

    st.subheader("📅 Interview Schedule")

    st.info("""
    🕘 10:00 AM - Power BI Developer

    🕑 2:00 PM - Data Analyst

    🕓 4:30 PM - SQL Developer
    """)

# =========================================================
# ANALYZE BUTTON
# =========================================================

st.divider()

if st.button("🚀 Analyze Resumes"):

    if not jd_file:
        st.error("Please upload JD")

    elif not resumes:
        st.error("Please upload resumes")

    else:

        progress = st.progress(0)
        status = st.empty()

        results = []

        for idx, resume in enumerate(resumes):

            status.info(f"Analyzing {resume.name}...")

            time.sleep(0.4)

            text = (
                read_pdf(resume)
                if resume.name.endswith(".pdf")
                else read_docx(resume)
            )

            result = score_resume(
                text,
                jd_text,
                skills,
                required_exp
            )

            results.append({
                "Resume": resume.name,
                "Score": round(result["score"], 2),
                "Skill Match %": f"{int(result['skill_match'])}%",
                "Experience": result["experience"],
                "Eligible": result["eligibility"],
                "Recommendation": result["recommendation"],
                "Matched Skills": ", ".join(result["matched"][:5])
            })

            progress.progress((idx + 1) / len(resumes))

        st.session_state.results_df = pd.DataFrame(results)

        status.success("Analysis Completed")

# =========================================================
# RESULTS
# =========================================================

if st.session_state.results_df is not None:

    df = st.session_state.results_df.copy()

    df = df.sort_values(
        "Score",
        ascending=False
    ).reset_index(drop=True)

    df.insert(
        0,
        "Rank",
        range(1, len(df)+1)
    )

    # =====================================================
    # METRICS
    # =====================================================

    st.subheader("📊 ATS Analytics")

    m1, m2, m3, m4 = st.columns(4)

    m1.metric("Total Resumes", len(df))

    m2.metric(
        "Eligible",
        len(df[df["Eligible"] == "Eligible"])
    )

    m3.metric(
        "Average Score",
        round(df["Score"].mean(), 2)
    )

    m4.metric(
        "Top Score",
        round(df["Score"].max(), 2)
    )

    st.divider()

    # =====================================================
    # FILTERS
    # =====================================================

    st.subheader("🔍 Candidate Filters")

    f1, f2 = st.columns(2)

    with f1:
        min_score = st.slider(
            "Minimum Score",
            0,
            100,
            50
        )

    with f2:
        status_filter = st.selectbox(
            "Eligibility",
            ["All", "Eligible", "Consider", "Rejected"]
        )

    filtered_df = df[df["Score"] >= min_score]

    if status_filter != "All":
        filtered_df = filtered_df[
            filtered_df["Eligible"] == status_filter
        ]

    filtered_df = filtered_df.reset_index(drop=True)

    filtered_df["Rank"] = range(
        1,
        len(filtered_df)+1
    )

    # =====================================================
    # CHARTS
    # =====================================================

    st.subheader("📈 ATS Score Visualization")

    st.plotly_chart(
        score_chart(filtered_df),
        use_container_width=True
    )

    st.plotly_chart(
        eligibility_chart(filtered_df),
        use_container_width=True
    )

    st.divider()

    # =====================================================
    # TABLE
    # =====================================================

    st.subheader("🏆 Resume Ranking Results")

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True,
        height=450
    )

    # =====================================================
    # DOWNLOAD
    # =====================================================

    csv = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download ATS Report",
        csv,
        "ATS_Report.csv",
        "text/csv",
        use_container_width=True
    )

