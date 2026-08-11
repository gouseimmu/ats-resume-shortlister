import base64
import os

import streamlit as st


APP_NAME = "Coforge Talent Hub"
APP_TAGLINE = "AI hiring intelligence for enterprise talent teams"
HERO_TITLE = "Recruiting command center for faster, cleaner hiring decisions"
HERO_SUBTITLE = "Parse JDs, rank candidates, schedule interviews, and monitor pipeline health from one polished workspace."
NAV_ITEMS = ["Dashboard", "Interview Calendar", "Analytics", "Settings"]


def _image_as_base64(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def status_class(status):
    value = (status or "").lower()
    if value == "eligible":
        return "pill-eligible"
    if value == "consider":
        return "pill-consider"
    return "pill-rejected"


def status_pill(status):
    return f'<span class="status-pill {status_class(status)}">&bull; {status}</span>'


def sidebar_panel():
    with st.sidebar:
        logo_path = os.path.join("assets", "coforge-logo.jpg")
        if os.path.exists(logo_path):
            logo_html = f'<img src="data:image/jpeg;base64,{_image_as_base64(logo_path)}" alt="Coforge logo" />'
        else:
            logo_html = '<div class="sidebar-logo-fallback">Coforge</div>'

        st.markdown(
            f"""
            <div class="sidebar-shell">
                <div class="sidebar-brand">
                    <div class="sidebar-logo">{logo_html}</div>
                    <div class="sidebar-brand-copy">
                        <p class="sidebar-brand-title">Coforge Talent Hub</p>
                        <p class="sidebar-brand-subtitle">AI-driven enterprise recruitment command center</p>
                    </div>
                </div>
                <div class="sidebar-info-card">
                    <p class="sidebar-info-title">AI sourcing engine</p>
                    <p class="sidebar-info-copy">Parse JDs, identify fit, and keep hiring operations focused on enterprise-ready talent.</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def hero_section():
    st.markdown(
        f"""
        <section class="hero-shell">
            <div>
                <p class="eyebrow">{APP_NAME}</p>
                <h1>{HERO_TITLE}</h1>
                <p>{HERO_SUBTITLE}</p>
            </div>
            <div class="hero-chip-row">
                <span class="chip">JD Intelligence</span>
                <span class="chip">ATS Scoring</span>
                <span class="chip">Interview Ops</span>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_metric(label, value, note="", color="#2563eb"):
    st.markdown(
        f"""
        <div class="metric-card">
            <p class="metric-label" style="color:{color};">{label}</p>
            <div class="metric-value">{value}</div>
            <p class="metric-note">{note}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_jd_card(icon, label, value):
    st.markdown(
        f"""
        <div class="jd-card">
            <div class="jd-icon">{icon}</div>
            <p class="jd-label">{label}</p>
            <div class="jd-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_insight_cards(df, interviews_count=0):
    total = len(df) if df is not None else 0
    eligible = len(df[df["Eligible"] == "Eligible"]) if total else 0
    consider = len(df[df["Eligible"] == "Consider"]) if total else 0
    rejected = len(df[df["Eligible"] == "Rejected"]) if total else 0
    avg_score = round(df["Score"].mean(), 1) if total else 0

    cols = st.columns(5, gap="large")
    with cols[0]:
        render_metric("Applicants", total, "parsed resumes", "#2563eb")
    with cols[1]:
        render_metric("Shortlisted", eligible, "eligible candidates", "#16a34a")
    with cols[2]:
        render_metric("Consider", consider, "needs review", "#f59e0b")
    with cols[3]:
        render_metric("Rejected", rejected, "screened out", "#dc2626")
    with cols[4]:
        render_metric("Avg Score", f"{avg_score}%", f"{interviews_count} scheduled", "#4f46e5")


def render_skill_tags(skills, limit=8):
    visible = list(skills or [])[:limit]
    tags = "".join(f'<span class="skill-tag">{skill}</span>' for skill in visible)
    if skills and len(skills) > limit:
        tags += f'<span class="skill-tag">+{len(skills) - limit}</span>'
    if not tags:
        tags = '<span class="skill-tag">No skills parsed</span>'
    st.markdown(f'<div class="skill-stack">{tags}</div>', unsafe_allow_html=True)


def _jd_icon(icon_name):
    icons = {
        "role": "<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'><rect x='3' y='7' width='18' height='13' rx='2'/><path d='M16 7V4H8v3'/></svg>",
        "experience": "<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'><path d='M12 8v5l3 3'/><circle cx='12' cy='12' r='9'/></svg>",
        "location": "<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'><path d='M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 1 1 18 0z'/><circle cx='12' cy='10' r='3'/></svg>",
        "notice": "<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'><path d='M21 12v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-8'/><path d='M7 8V5a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v3'/><path d='M16 2v4M8 2v4'/><path d='M12 13v2'/><path d='M12 17h.01'/></svg>",
        "employment": "<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'><path d='M3 7h18v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V7z'/><path d='M16 3h-8v4h8V3z'/><path d='M7 12h10'/></svg>",
        "skills": "<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'><path d='M4 7h16'/><path d='M4 12h16'/><path d='M4 17h16'/></svg>",
    }
    return icons.get(icon_name, icons["role"])


def _skill_chip_row(skills, flavor):
    if not skills:
        return '<div class="chip-row"><span class="skill-chip empty">Not parsed</span></div>'
    chips = "".join(f'<span class="skill-chip {flavor}">{skill}</span>' for skill in skills)
    return f'<div class="chip-row">{chips}</div>'


def render_jd_summary(jd):
    exp = jd.get("experience_range", (2, 5))
    primary_html = _skill_chip_row(jd.get("primary_skills", []), "primary")
    secondary_html = _skill_chip_row(jd.get("secondary_skills", []), "secondary")

    st.markdown(
        f"""
        <div class="jd-intel-shell">
            <div class="jd-intel-grid desktop-4">
                <div class="jd-card">
                    <div class="jd-card-top">
                        <div class="jd-card-icon">{_jd_icon('role')}</div>
                        <div class="jd-card-heading">
                            <p class="jd-card-label">Role</p>
                            <div class="jd-card-value">{jd.get('job_title', 'Not parsed')}</div>
                        </div>
                    </div>
                </div>
                <div class="jd-card">
                    <div class="jd-card-top">
                        <div class="jd-card-icon">{_jd_icon('experience')}</div>
                        <div class="jd-card-heading">
                            <p class="jd-card-label">Experience</p>
                            <div class="jd-card-value">{exp[0]}–{exp[1]} years</div>
                        </div>
                    </div>
                </div>
                <div class="jd-card">
                    <div class="jd-card-top">
                        <div class="jd-card-icon">{_jd_icon('location')}</div>
                        <div class="jd-card-heading">
                            <p class="jd-card-label">Location</p>
                            <div class="jd-card-value">{jd.get('location', 'Not specified')}</div>
                        </div>
                    </div>
                </div>
                <div class="jd-card">
                    <div class="jd-card-top">
                        <div class="jd-card-icon">{_jd_icon('notice')}</div>
                        <div class="jd-card-heading">
                            <p class="jd-card-label">Notice Period</p>
                            <div class="jd-card-value">{jd.get('notice_period', 'Not specified')}</div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="jd-intel-grid desktop-3">
                <div class="jd-card skill-summary-card">
                    <div class="jd-card-top">
                        <div class="jd-card-icon">{_jd_icon('employment')}</div>
                        <div class="jd-card-heading">
                            <p class="jd-card-label">Employment Type</p>
                            <div class="jd-card-value">{jd.get('employment_type', 'Not specified')}</div>
                        </div>
                    </div>
                </div>
                <div class="jd-card skill-summary-card">
                    <div class="jd-card-top">
                        <div class="jd-card-icon">{_jd_icon('skills')}</div>
                        <div class="jd-card-heading">
                            <p class="jd-card-label">Primary Skills</p>
                        </div>
                    </div>
                    {primary_html}
                </div>
                <div class="jd-card skill-summary-card">
                    <div class="jd-card-top">
                        <div class="jd-card-icon">{_jd_icon('skills')}</div>
                        <div class="jd-card-heading">
                            <p class="jd-card-label">Secondary Skills</p>
                        </div>
                    </div>
                    {secondary_html}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    responsibilities = jd.get("responsibilities", [])
    if responsibilities:
        with st.expander("Parsed Responsibilities", expanded=False):
            for item in responsibilities:
                st.markdown(f"- {item}")


def render_results_header():
    # Use EXACT same column proportions as candidate_row — ensures headers align with data
    st.markdown('<div class="results-header-band">', unsafe_allow_html=True)
    hcols = st.columns([0.5, 2.2, 0.75, 0.75, 1.0, 1.15, 1.1], gap="small")
    for col, label in zip(hcols, ["Rank", "Candidate", "Exp", "ATS Score", "Status", "Decision", "Action"]):
        col.markdown(f'<div class="table-head">{label}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def candidate_row(row, rank):
    missing = row.get("Missing Skills", [])
    matched = row.get("Matched Skills", [])
    st.markdown('<div class="results-row">', unsafe_allow_html=True)
    # Column proportions deliberately match the results-header-grid CSS columns:
    # 52px / 2fr / 80px / 80px / 110px / 130px / 120px → approximated as ratios
    cols = st.columns([0.5, 2.2, 0.75, 0.75, 1.0, 1.15, 1.1], gap="small")
    cols[0].markdown(f'<span class="rank-badge">#{rank}</span>', unsafe_allow_html=True)
    cols[1].markdown(
        f"""
        <div class="candidate-meta">
            <p class="candidate-name">{row['Candidate']}</p>
            <div class="candidate-email">{row['Email']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    cols[2].markdown(f'<div class="table-cell">{row["Experience"]} yrs</div>', unsafe_allow_html=True)
    cols[3].markdown(f'<div class="table-cell"><strong>{row["Score"]}%</strong></div>', unsafe_allow_html=True)
    cols[4].markdown(status_pill(row["Eligible"]), unsafe_allow_html=True)
    cols[5].markdown(f'<div class="table-cell"><strong>{row["Recommendation"]}</strong></div>', unsafe_allow_html=True)
    with cols[6]:
        st.markdown('<div class="action-stack">', unsafe_allow_html=True)
        action = st.button("Schedule", key=f"schedule_{rank}_{row['Email']}", type="primary", use_container_width=True)
        menu = st.selectbox("Actions", ["View", "Hold", "Reject"], key=f"action_{rank}_{row['Email']}", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="candidate-skill-grid">', unsafe_allow_html=True)
    skill_cols = st.columns([1, 1], gap="large")
    with skill_cols[0]:
        st.markdown('<div class="skill-panel"><p class="skill-label">Matched Skills</p>', unsafe_allow_html=True)
        render_skill_tags(matched, limit=6)
        st.markdown('</div>', unsafe_allow_html=True)
    with skill_cols[1]:
        st.markdown('<div class="skill-panel"><p class="skill-label">Missing Skills</p>', unsafe_allow_html=True)
        render_skill_tags(missing, limit=6)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    with st.expander(f"Candidate details - {row['Candidate']}", expanded=False):
        st.markdown('<div class="candidate-skill-grid expander-skill-grid">', unsafe_allow_html=True)
        d1, d2 = st.columns(2, gap="large")
        with d1:
            st.markdown('<div class="skill-panel"><p class="skill-label">Matched Skills</p>', unsafe_allow_html=True)
            render_skill_tags(matched, limit=20)
            st.markdown('</div>', unsafe_allow_html=True)
        with d2:
            st.markdown('<div class="skill-panel"><p class="skill-label">Missing Skills</p>', unsafe_allow_html=True)
            render_skill_tags(missing, limit=20)
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="candidate-summary">{row.get("Summary", "No summary available.")} Decision: {row["Recommendation"]}.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    return action, menu


def interview_card(row):
    calendar_url = row.get("google_calendar_url", "") if hasattr(row, "get") else ""
    if not isinstance(calendar_url, str) or calendar_url.lower() == "nan":
        calendar_url = ""
    meeting_badge = f"<span class=\"meeting-badge\">{row.get('mode', '')}</span>" if row.get('mode') else ""
    st.markdown(
        f"""
        <div class="interview-card">
            <div class="interview-card-top">
                <div class="interview-avatar">{row.get('name', '')[:2].upper()}</div>
                <div>
                    <p class="interview-name">{row.get('name', '')}</p>
                    <p class="interview-email">{row.get('email', '')}</p>
                </div>
                <span class="status-pill pill-eligible">{row.get('status', 'Scheduled')}</span>
            </div>
            <div class="interview-meta">
                <div class="interview-meta-item">
                    <span class="meta-label">Date</span>
                    <span>{row.get('date', '')}</span>
                </div>
                <div class="interview-meta-item">
                    <span class="meta-label">Time</span>
                    <span>{row.get('time', '')}</span>
                </div>
                <div class="interview-meta-lead">{row.get('interviewer', '')}</div>
            </div>
            <div class="interview-card-bottom">
                {meeting_badge}
                {f'<a class="calendar-link" href="{calendar_url}" target="_blank">Add to Google Calendar</a>' if calendar_url else ''}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
