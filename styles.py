import streamlit as st

def load_css():

    st.markdown("""

    <style>

    /* =========================================
       HIDE STREAMLIT DEFAULT UI
    ========================================= */

    /* Hide top toolbar */
    [data-testid="stToolbar"] {
        display: none !important;
    }

    /* Hide top menu */
    #MainMenu {
        visibility: hidden;
    }

    /* Hide floating manage app button */
    [data-testid="stStatusWidget"] {
        display: none !important;
    }

    /* Hide fullscreen button */
    button[title="View fullscreen"] {
        display: none !important;
    }

    /* Hide header */
    header[data-testid="stHeader"] {
        display: none;
    }

    /* Hide footer */
    footer {
        visibility: hidden;
    }

    /* =========================================
       GLOBAL
    ========================================= */

    html, body, [class*="css"] {
        font-family: "Segoe UI", sans-serif;
        transition: all 0.25s ease;
    }

    body {
        background: #f1f5f9;
    }

    /* =========================================
       MAIN CONTENT
    ========================================= */

    .main .block-container {
        max-width: 1600px;
        margin: auto;
        padding-top: 1rem !important;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
        transition: all 0.35s ease-in-out;
    }

    /* Auto responsive when sidebar collapsed */

    section[data-testid="stSidebar"][aria-expanded="false"] ~ div .main .block-container {
        max-width: 1850px !important;
        padding-left: 4rem !important;
        padding-right: 4rem !important;
    }

    /* =========================================
       SIDEBAR
    ========================================= */

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg,#020617,#071330);
        width: 320px !important;
        min-width: 320px !important;
        border-right: 1px solid rgba(255,255,255,0.05);
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }

    /* Sidebar collapsed */

    section[data-testid="stSidebar"][aria-expanded="false"] {
        margin-left: -320px;
    }

    /* Sidebar toggle button */

    [data-testid="collapsedControl"] {
        position: fixed;
        top: 14px;
        left: 14px;
        z-index: 999999;
        background: rgba(15,23,42,0.95);
        border-radius: 12px;
        padding: 6px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.20);
    }

    /* =========================================
       HERO CARD
    ========================================= */

    .hero-card {
        background: linear-gradient(135deg,#020617,#172554);
        padding: 42px;
        border-radius: 30px;
        color: white;
        box-shadow: 0 20px 45px rgba(0,0,0,0.28);
        margin-bottom: 28px;
    }

    /* =========================================
       GLASS EFFECT
    ========================================= */

    .glass {
        background: rgba(255,255,255,0.08);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 22px;
        padding: 20px;
    }

    /* =========================================
       METRIC CARDS
    ========================================= */

    .metric-card {
        background: white;
        padding: 24px;
        border-radius: 20px;
        box-shadow: 0 6px 24px rgba(0,0,0,0.08);
        text-align: center;
        transition: 0.3s ease;
    }

    .metric-card:hover {
        transform: translateY(-4px);
    }

    /* =========================================
       BADGES
    ========================================= */

    .success-badge {
        background: #dcfce7;
        color: #166534;
        padding: 8px 16px;
        border-radius: 999px;
        font-weight: 700;
        margin-right: 8px;
        display: inline-block;
    }

    .consider-badge {
        background: #fef3c7;
        color: #92400e;
        padding: 8px 16px;
        border-radius: 999px;
        font-weight: 700;
        margin-right: 8px;
        display: inline-block;
    }

    .reject-badge {
        background: #fee2e2;
        color: #991b1b;
        padding: 8px 16px;
        border-radius: 999px;
        font-weight: 700;
        display: inline-block;
    }

    /* =========================================
       BUTTONS
    ========================================= */

    .stButton button {
        width: 100%;
        border: none;
        border-radius: 14px;
        height: 52px;
        background: linear-gradient(135deg,#2563eb,#1d4ed8);
        color: white;
        font-size: 17px;
        font-weight: 700;
        transition: 0.3s ease;
        box-shadow: 0 6px 18px rgba(37,99,235,0.25);
    }

    .stButton button:hover {
        transform: translateY(-2px);
        background: linear-gradient(135deg,#1d4ed8,#1e40af);
    }

    /* =========================================
       INPUTS
    ========================================= */

    .stTextInput input,
    .stNumberInput input,
    .stTextArea textarea {
        border-radius: 12px !important;
    }

    .stSelectbox div[data-baseweb="select"] {
        border-radius: 12px !important;
    }

    .stMultiSelect div[data-baseweb="select"] {
        border-radius: 12px !important;
    }

    /* =========================================
       FILE UPLOADER
    ========================================= */

    [data-testid="stFileUploader"] {
        border-radius: 20px;
        border: 2px dashed #cbd5e1;
        padding: 12px;
        background: white;
    }

    /* =========================================
       DATAFRAMES
    ========================================= */

    .stDataFrame {
        border-radius: 18px;
        overflow: hidden;
    }

    /* =========================================
       CHARTS
    ========================================= */

    .js-plotly-plot {
        border-radius: 20px;
        overflow: hidden;
    }

    /* =========================================
       SCROLLBAR
    ========================================= */

    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }

    ::-webkit-scrollbar-thumb {
        background: #94a3b8;
        border-radius: 20px;
    }

    ::-webkit-scrollbar-track {
        background: #e2e8f0;
    }

    /* =========================================
       ANIMATIONS
    ========================================= */

    .hero-card,
    .metric-card,
    [data-testid="stFileUploader"] {
        animation: fadeIn 0.5s ease;
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0px);
        }
    }

    </style>

    """, unsafe_allow_html=True)