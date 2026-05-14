import streamlit as st

def load_css():
    st.markdown("""
    <style>
                
                /* --- HIDE TOP TOOLBAR & MENU --- */
    header[data-testid="stHeader"] {
        visibility: hidden;
        height: 0%;
    }

    /* --- HIDE BOTTOM "MANAGE APP" BUTTON --- */
    footer {
        visibility: hidden;
    }
    
    [data-testid="stStatusWidget"] {
        visibility: hidden;
    }
    /* Ensure the sidebar is visible and toggleable */
    [data-testid="stSidebarNav"] {display: block !important;}
    
    html, body, [class*="css"] {
        font-family: "Segoe UI", sans-serif;
    }

    .stApp {
        background-color: #f1f5f9;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #020617, #071330);
    }
    
    section[data-testid="stSidebar"] .stMarkdown, 
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] h2 {
        color: white !important;
    }

    /* Hero Card */
    .hero-card {
        background: linear-gradient(135deg, #020617, #172554);
        padding: 45px;
        border-radius: 32px;
        color: white;
        width: 100%;
        box-shadow: 0 20px 45px rgba(0,0,0,0.25);
        margin-bottom: 25px;
    }

    .glass {
        background: rgba(255,255,255,0.08);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 22px;
        padding: 22px;
    }

    /* Badges */
    .success-badge { background: #dcfce7; color: #166534; padding: 5px 15px; border-radius: 999px; font-weight: 700; margin-right: 5px; }
    .consider-badge { background: #fef3c7; color: #92400e; padding: 5px 15px; border-radius: 999px; font-weight: 700; margin-right: 5px; }
    .reject-badge { background: #fee2e2; color: #991b1b; padding: 5px 15px; border-radius: 999px; font-weight: 700; }

    /* Button Styling */
    .stButton button {
        width: 100%;
        height: 52px;
        border-radius: 14px;
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
        color: white;
        font-weight: 700;
    }
    </style>
    """, unsafe_allow_html=True)