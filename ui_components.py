import streamlit as st

def hero_section():

    st.markdown("""

    <div class="hero-card">

    <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;">

    <div>

    <h1 style="font-size:58px;margin:0;">
    🚀 TalentIQ ATS
    </h1>

    <p style="font-size:20px;color:#cbd5e1;">
    AI Powered Resume Screening & Hiring Platform
    </p>

    <div style="margin-top:20px;">

    <span class="success-badge">ATS Scoring</span>
    <span class="consider-badge">Resume Ranking</span>
    <span class="reject-badge">AI Hiring</span>

    </div>

    </div>

    <div class="glass">

    <div style="font-size:14px;color:#cbd5e1;">
    Today's Hiring Activity
    </div>

    <div style="font-size:52px;font-weight:800;color:#22c55e;">
    128
    </div>

    <div style="font-size:15px;color:#cbd5e1;">
    Candidates Processed
    </div>

    </div>

    </div>

    </div>

    """, unsafe_allow_html=True)


def sidebar_panel():

    with st.sidebar:

        st.title("⚡ ATS Dashboard")

        st.success("Enterprise Recruitment Platform")

        st.markdown("---")

        st.markdown("""
        ✅ Resume Ranking

        ✅ ATS Analytics

        ✅ AI Hiring

        ✅ Candidate Insights

        ✅ Skill Matching

        ✅ CSV Export
        """)