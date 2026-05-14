import streamlit as st

def load_css():

    st.markdown("""

    <style>

    #MainMenu {
        visibility:hidden;
    }

    footer {
        visibility:hidden;
    }

    header {
        visibility:hidden;
    }

    .block-container {
        padding-top:1rem;
        padding-bottom:1rem;
        max-width:1450px;
    }

    section[data-testid="stSidebar"] {
        background:#0f172a;
    }
                
    section[data-testid="stSidebar"] * {
        color:white;
    }

    .hero-card {
        background:linear-gradient(135deg,#020617,#172554);
        padding:40px;
        border-radius:24px;
        color:white;
        box-shadow:0 15px 35px rgba(0,0,0,0.25);
        margin-bottom:20px;
    }

    .glass {
        background:rgba(255,255,255,0.08);
        backdrop-filter:blur(10px);
        border:1px solid rgba(255,255,255,0.1);
        border-radius:20px;
        padding:18px;
    }

    .metric-card {
        background:white;
        padding:20px;
        border-radius:18px;
        box-shadow:0 6px 20px rgba(0,0,0,0.06);
        text-align:center;
    }

    .success-badge {
        background:#dcfce7;
        color:#166534;
        padding:6px 14px;
        border-radius:999px;
        font-weight:700;
    }

    .consider-badge {
        background:#fef3c7;
        color:#92400e;
        padding:6px 14px;
        border-radius:999px;
        font-weight:700;
    }

    .reject-badge {
        background:#fee2e2;
        color:#991b1b;
        padding:6px 14px;
        border-radius:999px;
        font-weight:700;
    }

    .stButton button {
        width:100%;
        border:none;
        border-radius:14px;
        height:52px;
        background:linear-gradient(135deg,#2563eb,#1d4ed8);
        color:white;
        font-size:17px;
        font-weight:700;
    }

    </style>

    """, unsafe_allow_html=True)