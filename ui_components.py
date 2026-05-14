import streamlit as st

def hero_section():
    st.markdown(
        """
        <div class="hero-card">
            <div style="
                display:flex;
                justify-content:space-between;
                align-items:center;
                flex-wrap:wrap;
                gap:20px;
            ">
                <div>
                    <h1 style="font-size:58px; margin:0; font-weight:800;">
                        🚀 TalentIQ ATS
                    </h1>
                    <p style="font-size:22px; color:#cbd5e1; margin-top:10px;">
                        AI Powered Resume Screening & Hiring Platform
                    </p>
                    <div style="margin-top:24px;">
                        <span class="success-badge">ATS Scoring</span>
                        <span class="consider-badge">Resume Ranking</span>
                        <span class="reject-badge">AI Hiring</span>
                    </div>
                </div>
                <div class="glass">
                    <div style="font-size:15px; color:#cbd5e1;">
                        Today's Hiring Activity
                    </div>
                    <div style="font-size:54px; font-weight:800; color:#22c55e; margin-top:10px;">
                        128
                    </div>
                    <div style="font-size:16px; color:#cbd5e1; margin-top:5px;">
                        Candidates Processed
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def sidebar_panel():
    with st.sidebar:
        try:
            # Use local assets or a placeholder if missing
            st.image("assets/logo.png", width=180)
        except:
            st.title("💼 TalentIQ")

        st.markdown("## ⚡ ATS Dashboard")
        st.success("Enterprise Recruitment Platform")

        st.markdown("---")

        # Removed bullet points and explanations for a cleaner list
        st.markdown("""
        ✅ Resume Ranking
        
        ✅ ATS Analytics
        
        ✅ AI Hiring
        
        ✅ Candidate Insights
        
        ✅ Skill Matching
        
        ✅ CSV Export
        """)
        
        st.markdown("---")
        st.caption("v2.4.0 | All Rights Reserved © 2026")