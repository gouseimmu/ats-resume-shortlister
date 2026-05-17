import streamlit as st


def inject_styles(sidebar_collapsed=False):
    sidebar_state_css = """
        section[data-testid="stSidebar"] {
            width: 0 !important;
            min-width: 0 !important;
            max-width: 0 !important;
            transform: translateX(-100%) !important;
            box-shadow: none !important;
            overflow: hidden !important;
        }
    """ if sidebar_collapsed else """
        section[data-testid="stSidebar"] {
            width: 280px !important;
            min-width: 280px !important;
            max-width: 280px !important;
            transform: translateX(0) !important;
            visibility: visible !important;
            flex-shrink: 0 !important;
        }
    """
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        :root {
            --bg: #f4f7fb;
            --panel: #ffffff;
            --panel-soft: #f8fafc;
            --ink: #111827;
            --muted: #667085;
            --border: #d9e2ef;
            --blue: #2563eb;
            --indigo: #4f46e5;
            --cyan: #0891b2;
            --green: #16a34a;
            --amber: #f59e0b;
            --red: #dc2626;
            --shadow: 0 16px 42px rgba(15, 23, 42, 0.08);
        }

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(37, 99, 235, 0.08), transparent 28rem),
                linear-gradient(180deg, #f8fbff 0%, var(--bg) 38%, #eef3f9 100%);
            color: var(--ink);
        }

        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        [data-testid="stStatusWidget"],
        #MainMenu,
        footer,
        .viewerBadge,
        [data-testid="stViewerBadge"],
        .stAppDeployButton,
        [data-testid="viewerBadge"],
        #connection-status,
        [data-testid="stConnectionStatus"],
        .stConnectionStatus {
            visibility: hidden !important;
            display: none !important;
            height: 0 !important;
            width: 0 !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }

        header[data-testid="stHeader"] {
            display: none !important;
            height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        button[title="View fullscreen"] {
            display: none !important;
        }

        /* ===== STREAMLIT 1.57 EXACT SIDEBAR TOGGLE KILL ===== */
        [data-testid="stExpandSidebarButton"],
        [data-testid="stSidebarCollapseButton"],
        [data-testid="stSidebarCollapseButton"] *,
        [data-testid="collapsedControl"],
        [data-testid="collapsedControl"] *,
        button[title="Close sidebar"],
        button[title="Open sidebar"],
        button[kind="headerNoPadding"],
        button[kind="header"] {
            display: none !important;
            visibility: hidden !important;
            width: 0 !important;
            height: 0 !important;
            min-width: 0 !important;
            min-height: 0 !important;
            opacity: 0 !important;
            pointer-events: none !important;
            position: absolute !important;
            left: -9999px !important;
            top: -9999px !important;
            overflow: hidden !important;
        }

        /* ===== KILL EMPTY NAV-SHELL DIV (Streamlit isolates HTML divs) ===== */
        /* The actual navbar uses st.columns which creates stHorizontalBlock */
        /* The empty .nav-shell div renders as an unwanted white capsule at top */
        .nav-shell:not(:has(*)) {
            display: none !important;
            height: 0 !important;
            padding: 0 !important;
            margin: 0 !important;
            border: none !important;
            box-shadow: none !important;
        }

        /* ===== ZERO OUT ALL STREAMLIT MAIN PADDING ===== */
        .main {
            padding-top: 0 !important;
        }
        [data-testid="stMain"] {
            padding-top: 0 !important;
            margin-top: 0 !important;
        }
        [data-testid="stAppViewBlockContainer"] {
            padding-top: 0 !important;
            margin-top: 0 !important;
        }

        div.block-container {
            max-width: 1360px;
            padding: 0 1.25rem 1.4rem;
            margin-top: 0 !important;
        }

        /* Tight vertical rhythm — 8px system */
        [data-testid="stVerticalBlock"] { gap: 0.5rem; }
        [data-testid="stHorizontalBlock"] { gap: 0.75rem !important; align-items: stretch !important; }
        .stDivider, hr { margin: 0.75rem 0 !important; border-color: var(--border) !important; }

        h1, h2, h3 {
            letter-spacing: 0;
            color: var(--ink);
        }

        h1 { font-size: 1.9rem !important; line-height: 1.15 !important; }
        h2, h3, [data-testid="stMarkdownContainer"] h2, [data-testid="stMarkdownContainer"] h3 {
            margin: 0.2rem 0 0.45rem;
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #07111f 0%, #0f172a 46%, #111827 100%) !important;
            border-right: 1px solid rgba(255,255,255,0.08);
            box-shadow: 18px 0 48px rgba(15, 23, 42, 0.18);
            position: sticky !important;
            top: 0 !important;
            height: 100vh !important;
            transition: width 0.24s ease, min-width 0.24s ease, transform 0.24s ease, margin 0.24s ease;
        }
        """
        + sidebar_state_css +
        """

        section[data-testid="stSidebar"] > div {
            padding: 1rem 1rem 1.2rem;
            height: 100vh;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            gap: 1rem;
        }

        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] span {
            color: #f8fafc !important;
        }

        .sidebar-shell {
            display: flex;
            flex-direction: column;
            gap: 0.85rem;
        }

        .sidebar-brand {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            padding: 1.5rem 1rem 1.2rem;
            border-bottom: 1px solid rgba(255,255,255,0.08);
            margin-bottom: 0.25rem;
        }

        .sidebar-logo {
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            margin-bottom: 1rem;
        }

        .sidebar-logo img {
            width: 148px;
            max-width: 100%;
            height: auto;
            object-fit: contain;
            mix-blend-mode: screen;
            filter: drop-shadow(0 2px 8px rgba(0,0,0,0.4));
        }

        .sidebar-logo-fallback {
            width: 130px;
            height: 52px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #ffffff;
            font-weight: 900;
            font-size: 2rem;
            letter-spacing: 0.05em;
        }

        .sidebar-brand-copy {
            display: flex;
            flex-direction: column;
            justify-content: center;
            gap: 0.25rem;
            margin-top: 1rem;
            width: 100%;
            max-width: 15rem;
        }

        .sidebar-brand-title {
            color: #eef2ff;
            font-size: 1.05rem;
            font-weight: 900;
            letter-spacing: 0.01em;
            margin: 0;
            line-height: 1.08;
        }

        .sidebar-brand-subtitle {
            color: #dbeafe;
            font-size: 0.78rem;
            margin: 0;
            line-height: 1.5;
            opacity: 0.9;
        }

        section[data-testid="stSidebar"] button {
            width: 100%;
            height: 2.8rem;
            font-size: 1rem;
            font-weight: 700;
            color: #0f172a;
            background: rgba(255,255,255,0.95);
            border: 1px solid rgba(148,163,184,0.35);
            border-radius: 999px;
            box-shadow: 0 12px 30px rgba(15,23,42,0.08);
            transition: transform 0.18s ease, box-shadow 0.18s ease, background 0.18s ease;
        }

        section[data-testid="stSidebar"] button:hover {
            transform: translateY(-1px);
            background: rgba(255,255,255,1);
            border-color: rgba(148,163,184,0.55);
            box-shadow: 0 18px 36px rgba(15,23,42,0.12);
        }

        .sidebar-info-card {
            padding: 1.2rem 1rem;
            border-radius: 20px;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255,255,255,0.14);
            color: #c7d2fe;
            line-height: 1.55;
            min-height: 132px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        .sidebar-info-title {
            margin: 0 0 0.35rem;
            font-size: 0.84rem;
            font-weight: 800;
            color: #ffffff;
        }

        .sidebar-info-copy {
            margin: 0;
            font-size: 0.78rem;
            color: #c7d2fe;
        }

        .sidebar-divider {
            height: 1px;
            background: rgba(255,255,255,0.08);
            margin: 0.2rem 0;
        }

        .sidebar-footer {
            padding: 1rem;
            border-radius: 18px;
            background: rgba(255, 255, 255, 0.07);
            border: 1px solid rgba(255,255,255,0.08);
            color: #c7d2fe;
            line-height: 1.5;
        }

        .sidebar-footer-title {
            margin: 0 0 0.4rem;
            font-size: 0.82rem;
            font-weight: 800;
            color: #ffffff;
        }

        .sidebar-footer-copy {
            margin: 0;
            font-size: 0.78rem;
            color: #c7d2fe;
        }

        .brand-card {
            padding: 0.78rem;
            border: 1px solid rgba(255,255,255,0.14);
            border-radius: 14px;
            background: linear-gradient(135deg, rgba(255,255,255,0.14), rgba(255,255,255,0.05));
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.16), 0 14px 28px rgba(0,0,0,0.16);
            text-align: center;
            margin-bottom: 0.7rem;
        }

        .brand-card img {
            max-width: 132px;
            max-height: 62px;
            object-fit: contain;
            filter: drop-shadow(0 8px 18px rgba(0,0,0,0.18));
        }

        .side-brand-title {
            color: #ffffff;
            font-size: 1.08rem;
            font-weight: 750;
            margin: 0.58rem 0 0.12rem;
        }

        .side-brand-subtitle {
            color: #a7b0c0;
            font-size: 0.75rem;
            margin: 0;
        }

        section[data-testid="stSidebar"] [role="radiogroup"] {
            gap: 0.35rem;
        }

        section[data-testid="stSidebar"] label[data-baseweb="radio"] {
            border: 1px solid transparent;
            border-radius: 10px;
            padding: 0.56rem 0.68rem;
            margin: 0.08rem 0;
            transition: background 0.18s ease, border 0.18s ease, transform 0.18s ease;
        }

        section[data-testid="stSidebar"] label[data-baseweb="radio"]:hover {
            background: rgba(255,255,255,0.08);
            transform: translateX(2px);
        }

        section[data-testid="stSidebar"] label[data-baseweb="radio"]:has(input:checked) {
            background: linear-gradient(135deg, rgba(37,99,235,0.28), rgba(8,145,178,0.18));
            border-color: rgba(147, 197, 253, 0.34);
        }

        .hero-shell {
            display: grid;
            grid-template-columns: minmax(0, 1fr) auto;
            align-items: center;
            gap: 1rem;
            padding: 0.85rem 1.1rem;
            margin-bottom: 0.25rem;
            border: 1px solid rgba(37, 99, 235, 0.16);
            border-radius: 14px;
            background:
                linear-gradient(135deg, rgba(255,255,255,0.96), rgba(239,246,255,0.9)),
                radial-gradient(circle at top right, rgba(37,99,235,0.16), transparent 20rem);
            box-shadow: var(--shadow);
        }

        /* ===== NAVBAR — Precision targeting via .navbar-marker sibling ===== */
        /* A hidden .navbar-marker div is injected just before the navbar st.columns. */
        /* This lets us style the exact stVerticalBlock containing the navbar columns. */
        .nav-shell {
            display: none; /* empty nav-shell div is hidden */
        }

        /* Target the stVerticalBlock that contains .navbar-marker */
        [data-testid="stVerticalBlock"]:has(> div > [data-testid="stVerticalBlock"] .navbar-marker) > div:has(.navbar-marker) ~ div [data-testid="stHorizontalBlock"],
        /* Fallback: target the stHorizontalBlock immediately after the navbar-marker stMarkdownContainer */
        [data-testid="stMarkdownContainer"]:has(.navbar-marker) ~ [data-testid="stHorizontalBlock"],
        div:has(> [data-testid="stMarkdownContainer"] .navbar-marker) + div [data-testid="stHorizontalBlock"] {
            position: sticky;
            top: 0;
            z-index: 999;
            background: rgba(255, 255, 255, 0.95) !important;
            backdrop-filter: blur(24px) !important;
            -webkit-backdrop-filter: blur(24px) !important;
            border: 1px solid rgba(203, 213, 225, 0.5) !important;
            border-radius: 20px !important;
            box-shadow: 0 4px 16px rgba(15, 23, 42, 0.07), 0 1px 3px rgba(15, 23, 42, 0.04) !important;
            padding: 0.65rem 1rem !important;
            margin-bottom: 0.75rem !important;
            align-items: center !important;
            gap: 0.75rem !important;
        }

        .topbar-brand {
            display: flex;
            flex-direction: column;
            gap: 0.2rem;
        }

        .topbar-title {
            color: #0f172a;
            font-size: 1.02rem;
            font-weight: 800;
            margin: 0;
        }

        .topbar-subtitle {
            color: #475569;
            font-size: 0.78rem;
            margin: 0;
            letter-spacing: 0.01em;
        }

        .nav-shell button[title="Show or hide sidebar"] {
            width: 3.2rem;
            min-height: 3.2rem;
            border-radius: 999px;
            border: 1px solid rgba(15, 23, 42, 0.08);
            background: rgba(255,255,255,0.88);
            color: #0f172a;
            font-size: 1.1rem;
            font-weight: 700;
            transition: transform 0.18s ease, box-shadow 0.18s ease, background 0.18s ease;
        }

        .nav-shell button[title="Show or hide sidebar"]:hover {
            transform: translateY(-1px);
            background: rgba(255,255,255,0.98);
            box-shadow: 0 14px 30px rgba(15, 23, 42, 0.14);
        }

        .nav-shell [role="radiogroup"] {
            display: flex;
            flex-wrap: wrap;
            justify-content: flex-end;
            gap: 0.5rem;
        }

        .nav-shell label[data-baseweb="radio"] {
            border: 1px solid rgba(148, 163, 184, 0.45);
            border-radius: 999px;
            padding: 0.6rem 0.95rem;
            background: #f8fbff;
            color: #475569;
            font-size: 0.88rem;
            font-weight: 700;
            transition: all 0.18s ease;
        }

        .nav-shell label[data-baseweb="radio"]:hover {
            background: rgba(59, 130, 246, 0.12);
            border-color: rgba(59, 130, 246, 0.28);
            color: #1d4ed8;
            transform: translateY(-1px);
            box-shadow: 0 8px 20px rgba(37, 99, 235, 0.12);
        }

        .nav-shell label[data-baseweb="radio"]:has(input:checked) {
            background: linear-gradient(135deg, var(--blue), var(--indigo));
            border-color: transparent;
            color: #ffffff !important;
            box-shadow: 0 20px 38px rgba(59, 130, 246, 0.18);
        }

        .nav-shell label[data-baseweb="radio"]:has(input:checked) span {
            color: #ffffff !important;
        }

        .nav-shell [role="radiogroup"] {
            display: flex;
            flex-wrap: wrap;
            justify-content: flex-end;
            gap: 0.38rem;
        }

        .nav-shell label[data-baseweb="radio"] {
            border: 1px solid #dbe7ff;
            border-radius: 999px;
            padding: 0.42rem 0.68rem;
            background: #f8fbff;
            transition: all 0.16s ease;
        }

        .nav-shell label[data-baseweb="radio"]:hover {
            transform: translateY(-1px);
            border-color: #bfdbfe;
            box-shadow: 0 8px 20px rgba(37, 99, 235, 0.12);
        }

        .nav-shell label[data-baseweb="radio"]:has(input:checked) {
            background: linear-gradient(135deg, var(--blue), var(--indigo));
            border-color: transparent;
        }

        .nav-shell label[data-baseweb="radio"]:has(input:checked) span {
            color: #ffffff !important;
        }

        .eyebrow {
            color: var(--blue);
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin: 0 0 0.25rem;
        }

        .hero-shell h1 {
            font-size: 2rem !important;
            font-weight: 800;
            margin: 0;
        }

        .hero-shell p {
            color: var(--muted);
            margin: 0.35rem 0 0;
            font-size: 0.96rem;
        }

        .hero-chip-row {
            display: flex;
            gap: 0.45rem;
            flex-wrap: wrap;
            justify-content: flex-end;
        }

        .chip {
            border-radius: 999px;
            background: #eef4ff;
            border: 1px solid #c7d7fe;
            color: #1d4ed8;
            font-size: 0.74rem;
            font-weight: 700;
            padding: 0.38rem 0.62rem;
        }

        /* ===== METRIC CARDS ===== */
        .metric-card, .panel-card, .candidate-card {
            background: #ffffff;
            border: 1px solid #e8eef7 !important;
            border-radius: 16px !important;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.06), 0 8px 24px rgba(15, 23, 42, 0.04) !important;
        }

        /* Metric row: each Streamlit column stretches equally */
        [data-testid="stHorizontalBlock"] > div:has(.metric-card) {
            flex: 1 1 0 !important;
            min-width: 0 !important;
        }

        .metric-card {
            min-height: 112px;
            padding: 1rem 1.2rem;
            border-left: 4px solid transparent !important;
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: center;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        .metric-card::before {
            content: "";
            position: absolute;
            inset: 0;
            z-index: 0;
            background: radial-gradient(circle at top left, rgba(59, 130, 246, 0.05), transparent 60%);
        }

        .metric-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.1), 0 20px 48px rgba(15, 23, 42, 0.06) !important;
        }

        .metric-card .metric-label,
        .metric-card .metric-value,
        .metric-card .metric-note {
            position: relative;
            z-index: 1;
        }

        .metric-card:nth-child(1) { border-left-color: #2563eb !important; }
        .metric-card:nth-child(2) { border-left-color: #16a34a !important; }
        .metric-card:nth-child(3) { border-left-color: #f59e0b !important; }
        .metric-card:nth-child(4) { border-left-color: #dc2626 !important; }
        .metric-card:nth-child(5) { border-left-color: #4f46e5 !important; }

        .metric-label {
            color: var(--muted);
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 0.09em;
            text-transform: uppercase;
            margin: 0;
        }

        .metric-value {
            color: var(--ink);
            font-size: 1.95rem;
            font-weight: 800;
            margin: 0.35rem 0 0.15rem;
            line-height: 1.1;
        }

        .metric-note {
            color: var(--muted);
            font-size: 0.8rem;
            margin: 0;
            font-weight: 500;
        }

        .metric-card .metric-note {
            margin-top: 0;
            color: #94a3b8;
        }

        .jd-intel-shell {
            padding: 0.35rem 0 1rem;
            margin-top: 0.4rem;
            margin-bottom: 1.4rem;
        }

        .jd-alert-banner {
            display: flex;
            align-items: flex-start;
            gap: 0.85rem;
            padding: 1rem 1.1rem;
            margin-bottom: 1.15rem;
            border-radius: 18px;
            border: 1px solid #d6f5e1;
            background: rgba(220, 248, 231, 0.28);
        }

        .jd-alert-icon {
            width: 2.4rem;
            height: 2.4rem;
            min-width: 2.4rem;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 14px;
            background: radial-gradient(circle at top left, rgba(22, 163, 74, 0.14), rgba(255, 255, 255, 0.75));
            color: #166534;
            font-size: 1rem;
            font-weight: 800;
        }

        .jd-alert-title {
            color: #134e4a;
            font-size: 0.96rem;
            font-weight: 800;
            margin: 0;
        }

        .jd-alert-copy {
            color: #334155;
            font-size: 0.88rem;
            margin: 0.25rem 0 0;
            line-height: 1.5;
        }

        .jd-intel-grid {
            display: grid;
            gap: 1rem;
            align-items: stretch;
            grid-auto-rows: minmax(170px, auto);
        }

        .jd-intel-grid.desktop-4 {
            grid-template-columns: repeat(4, minmax(0, 1fr));
        }

        .jd-intel-grid.desktop-3 {
            grid-template-columns: repeat(3, minmax(0, 1fr));
        }

        .jd-card {
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            align-items: stretch;
            min-height: 170px;
            padding: 1.15rem 1.2rem;
            border-radius: 22px;
            border: 1px solid rgba(148, 163, 184, 0.22);
            background: #ffffff;
            box-shadow: 0 20px 44px rgba(15, 23, 42, 0.08);
            transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        }

        .jd-card:hover {
            transform: translateY(-1px);
            border-color: rgba(59, 130, 246, 0.22);
            box-shadow: 0 26px 50px rgba(37, 99, 235, 0.1);
        }

        .jd-card-top {
            display: flex;
            align-items: center;
            gap: 0.85rem;
            flex-wrap: wrap;
            margin-bottom: 0.85rem;
        }

        .jd-card-icon {
            width: 2.45rem;
            height: 2.45rem;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 18px;
            background: linear-gradient(135deg, rgba(238, 242, 255, 0.96), rgba(219, 234, 254, 0.95));
            color: #2563eb;
            flex-shrink: 0;
        }

        .jd-card-icon svg {
            width: 1.15rem;
            height: 1.15rem;
        }

        .jd-card-heading {
            display: flex;
            flex-direction: column;
            gap: 0.28rem;
            min-width: 0;
        }

        .jd-card-label {
            color: #64748b;
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin: 0;
        }

        .jd-card-value {
            color: #0f172a;
            font-size: 1rem;
            font-weight: 800;
            line-height: 1.35;
            margin: 0;
            word-break: break-word;
        }

        .skill-summary-card {
            justify-content: flex-start;
        }

        .chip-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.65rem;
            margin-top: 0.85rem;
        }

        .skill-chip {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 999px;
            padding: 0.42rem 0.9rem;
            font-size: 0.75rem;
            font-weight: 700;
            line-height: 1.2;
            white-space: normal;
            max-width: 100%;
        }

        .skill-chip.primary {
            background: rgba(59, 130, 246, 0.16);
            color: #1d4ed8;
            border: 1px solid rgba(59, 130, 246, 0.2);
        }

        .skill-chip.secondary {
            background: rgba(226, 232, 240, 0.95);
            color: #475569;
            border: 1px solid rgba(203, 213, 224, 0.9);
        }

        .skill-chip.empty {
            background: rgba(241, 245, 249, 0.98);
            color: #64748b;
            border: 1px solid rgba(226, 232, 240, 1);
        }

.skill-stack {
            display: flex;
            flex-wrap: wrap;
            gap: 0.4rem;
            margin-top: 0.75rem;
            max-height: none;
            overflow: visible;
        }


        .status-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.34rem;
            border-radius: 999px;
            font-size: 0.74rem;
            font-weight: 800;
            padding: 0.32rem 0.58rem;
            white-space: nowrap;
        }

        .pill-eligible { background: #dcfce7; color: #15803d; }
        .pill-consider { background: #fef3c7; color: #b45309; }
        .pill-rejected { background: #fee2e2; color: #b91c1c; }

        .results-shell {
            border: 1px solid var(--border);
            border-radius: 16px;
            background: #ffffff;
            box-shadow: var(--shadow);
            padding: 0;
            overflow: hidden;
        }

        /* Header band — uses st.columns so it auto-aligns with data rows */
        .results-header-band {
            background: #f8fafc;
            border-bottom: 2px solid #e2e8f0;
            padding: 0 0.35rem;
        }

        /* Ensure header band stHorizontalBlock matches row stHorizontalBlock */
        .results-header-band [data-testid="stHorizontalBlock"],
        .results-row [data-testid="stHorizontalBlock"] {
            align-items: center !important;
            gap: 0.5rem !important;
            padding: 0 !important;
        }

        /* ATS row wrapper */
        .results-row {
            border-bottom: 1px solid #f1f5f9;
            padding: 0.5rem 0.35rem 0.35rem;
            transition: background 0.15s ease;
        }

        .results-row:last-child { border-bottom: none; }
        .results-row:hover { background: #fafbff; }

        .candidate-card .stColumn {
            display: flex;
            align-items: center;
        }

        .interview-card {
            padding: 1rem 1.1rem;
            border-radius: 18px;
            border: 1px solid rgba(203, 213, 225, 0.55);
            background: rgba(255,255,255,0.96);
            box-shadow: 0 18px 42px rgba(15,23,42,0.08);
            transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
        }

        .interview-card:hover {
            transform: translateY(-1px);
            border-color: rgba(59,130,246,0.24);
            box-shadow: 0 22px 48px rgba(37,99,235,0.12);
        }

        .interview-card-top {
            display: grid;
            grid-template-columns: auto 1fr auto;
            align-items: center;
            gap: 0.9rem;
        }

        .interview-avatar {
            width: 44px;
            height: 44px;
            display: grid;
            place-items: center;
            border-radius: 14px;
            background: linear-gradient(135deg, rgba(59,130,246,0.18), rgba(79,70,229,0.18));
            color: #1d4ed8;
            font-size: 0.96rem;
            font-weight: 800;
        }

        .interview-name {
            margin: 0;
            color: #0f172a;
            font-size: 0.95rem;
            font-weight: 800;
        }

        .interview-email {
            margin: 0.2rem 0 0;
            color: #6b7280;
            font-size: 0.78rem;
        }

        .interview-meta {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.9rem;
            margin: 1rem 0 0;
            border-top: 1px solid rgba(148,163,184,0.15);
            padding-top: 1rem;
        }

        .interview-meta-item {
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
        }

        .meta-label {
            color: #64748b;
            font-size: 0.72rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        .interview-meta span {
            color: #0f172a;
            font-weight: 700;
            font-size: 0.93rem;
        }

        .interview-meta-lead {
            color: #475569;
            font-size: 0.82rem;
            grid-column: span 3;
        }

        .interview-card-bottom {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.75rem;
            margin-top: 1rem;
        }

        .meeting-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            padding: 0.38rem 0.75rem;
            border-radius: 999px;
            color: #1d4ed8;
            background: rgba(59,130,246,0.12);
            border: 1px solid rgba(59,130,246,0.18);
            font-size: 0.78rem;
            font-weight: 700;
        }

        .calendar-link {
            color: #2563eb;
            font-weight: 700;
            font-size: 0.82rem;
            text-decoration: none;
        }

        .calendar-link:hover {
            text-decoration: underline;
        }

        .results-row div[data-testid="stVerticalBlockBorderWrapper"] {
            background: transparent !important;
            border: none !important;
            border-radius: 0 !important;
            box-shadow: none !important;
            padding: 0 !important;
            margin: 0 !important;
        }

        .rank-badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 2rem;
            height: 2rem;
            border-radius: 10px;
            background: #eef4ff;
            border: 1px solid #c7d7fe;
            color: #1d4ed8;
            font-weight: 800;
            font-size: 0.78rem;
        }

        .skill-label {
            color: var(--muted);
            font-size: 0.68rem;
            font-weight: 800;
            letter-spacing: 0.06em;
            margin: 0 0 0.28rem;
            text-transform: uppercase;
        }

        .candidate-name {
            color: var(--ink);
            font-weight: 800;
            line-height: 1.15;
            margin: 0;
        }

        .candidate-email {
            color: var(--muted);
            font-size: 0.76rem;
            margin-top: 0.16rem;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            display: block;
        }

        .candidate-card:hover {
            transform: translateY(-1px);
            border-color: #bfdbfe !important;
            box-shadow: 0 18px 42px rgba(37, 99, 235, 0.1);
        }

        .table-head {
            color: #344054;
            font-size: 0.68rem;
            font-weight: 800;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            white-space: nowrap;
            padding: 0.75rem 0.6rem;
        }

        .table-cell {
            color: #1e293b;
            font-size: 0.88rem;
            font-weight: 600;
            padding: 0.25rem 0;
            display: flex;
            align-items: center;
            min-height: 100%;
        }

        .table-cell strong {
            color: #0f172a;
            font-weight: 700;
        }

        .skill-tag {
            display: inline-flex;
            max-width: 100%;
            border-radius: 999px;
            background: #f1f5f9;
            border: 1px solid #e2e8f0;
            color: #334155;
            font-size: 0.72rem;
            font-weight: 700;
            padding: 0.24rem 0.48rem;
            margin: 0.12rem;
            overflow: visible;
            text-overflow: unset;
            white-space: normal;
        }

        .skill-stack {
            display: flex;
            flex-wrap: wrap;
            gap: 0.4rem;
            margin-top: 0.75rem;
            max-height: none;
            overflow: visible;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:has(.candidate-name) [data-testid="stExpander"] {
            margin-top: 0.55rem;
            border-radius: 10px !important;
            overflow: hidden;
        }

        div[data-testid="stFileUploader"] section,
        div[data-testid="stForm"] {
            border: 1px solid var(--border);
            border-radius: 12px;
            background: rgba(255,255,255,0.94);
            box-shadow: var(--shadow);
        }

        .stButton button, .stDownloadButton button {
            border-radius: 9px !important;
            border: 1px solid var(--border) !important;
            font-weight: 750 !important;
            min-height: 2.16rem;
            transition: transform 0.16s ease, box-shadow 0.16s ease, background 0.16s ease;
        }

        .stButton button:hover, .stDownloadButton button:hover {
            transform: translateY(-1px);
            box-shadow: 0 10px 26px rgba(15, 23, 42, 0.12);
        }

        div[data-testid="stButton"] button[kind="primary"] {
            background: linear-gradient(135deg, var(--blue), var(--indigo)) !important;
            color: #ffffff !important;
            border-color: transparent !important;
        }

        .analysis-cta-wrap {
            display: flex;
            justify-content: center;
            margin: 0.6rem 0 0.2rem;
        }

        .analysis-cta-wrap + div[data-testid="stHorizontalBlock"] button {
            min-height: 2.35rem !important;
            border-radius: 12px !important;
            padding: 0 1rem !important;
            font-size: 0.88rem !important;
            box-shadow: 0 12px 26px rgba(37, 99, 235, 0.18);
        }

        .schedule-preview {
            border: 1px solid #dbe7ff;
            border-radius: 12px;
            background: #f8fbff;
            padding: 0.8rem;
            color: #344054;
            white-space: pre-wrap;
            font-size: 0.84rem;
            max-height: 220px;
            overflow-y: auto;
        }

        div[data-testid="stAlert"] {
            border-radius: 11px;
            margin: 0.1rem 0 0.55rem;
        }

        .js-plotly-plot, div[data-testid="stDataFrame"] {
            border-radius: 12px;
            background: #ffffff;
            border: 1px solid var(--border);
            box-shadow: var(--shadow);
            overflow: hidden;
        }

        @media (max-width: 900px) {
            div.block-container { padding: 0.85rem 0.8rem 1.5rem; }
            .hero-shell { grid-template-columns: 1fr; }
            .hero-chip-row { justify-content: flex-start; }
            section[data-testid="stSidebar"] { width: 248px !important; min-width: 248px !important; }
            .result-header { display: none; }
            .nav-shell { position: static; }
            .jd-intel-grid.desktop-4,
            .jd-intel-grid.desktop-3 {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }
        }

        @media (max-width: 640px) {
            .jd-intel-grid.desktop-4,
            .jd-intel-grid.desktop-3 {
                grid-template-columns: 1fr;
            }
            .jd-card {
                min-height: auto;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def load_css():
    inject_styles(False)
