from datetime import date, datetime
import importlib

import pandas as pd
import streamlit as st

from ats_engine import score_resume
from charts import (
    ats_score_distribution,
    candidate_funnel,
    eligibility_chart,
    experience_distribution,
    score_chart,
    shortlisted_vs_rejected,
    skill_match_heatmap,
    top_skills_chart,
)
from database import delete_interview, get_interviews, init_db, save_interview
from parser import parse_job_description, parse_resume_identity
import scheduler as scheduler_module
from styles import inject_styles
from ui_components import (
    APP_NAME,
    NAV_ITEMS,
    candidate_row,
    hero_section,
    interview_card,
    render_insight_cards,
    render_jd_summary,
    render_results_header,
    sidebar_panel,
)
from utils import read_docx, read_pdf


scheduler_module = importlib.reload(scheduler_module)
INTERVIEW_MODES = scheduler_module.INTERVIEW_MODES
TIME_SLOTS = scheduler_module.TIME_SLOTS
build_interview_payload = scheduler_module.build_interview_payload
default_body = scheduler_module.default_body
default_subject = scheduler_module.default_subject
generate_ics = scheduler_module.generate_ics
google_calendar_url = scheduler_module.google_calendar_url
is_valid_email = scheduler_module.is_valid_email
send_interview_email = scheduler_module.send_interview_email
validate_email_payload = scheduler_module.validate_email_payload


st.set_page_config(
    page_title=f"{APP_NAME} | Enterprise Recruitment",
    page_icon="assets/logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

def init_state():
    defaults = {
        "results_df": None,
        "jd_text": "",
        "parsed_jd": None,
        "selected_candidate": None,
        "active_role": "Auto Parsed Role",
        "sidebar_collapsed": False,
        "invite_notice": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_state()
inject_styles(st.session_state.sidebar_collapsed)
init_db()

# Runtime JS: Eliminate all Streamlit branding, force custom tab title/favicon, and hide developer widgets
st.markdown(
    """
    <script>
    (function() {
        // 1. Force custom tab title without 'Streamlit' prefix
        function enforceTitle() {
            const targetTitle = "JLL Talent Hub | Enterprise Recruitment";
            if (document.title !== targetTitle) {
                document.title = targetTitle;
            }
        }
        
        // 2. Force high-quality custom JLL Red SVG Favicon
        function enforceFavicon() {
            let links = document.querySelectorAll("link[rel*='icon']");
            links.forEach(el => el.remove());
            
            const link = document.createElement('link');
            link.type = 'image/svg+xml';
            link.rel = 'icon';
            // Custom clean enterprise JLL Red styled SVG
            link.href = 'data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><rect width=%22100%22 height=%22100%22 rx=%2224%22 fill=%22%23dc2626%22/><text y=%22.95em%22 x=%22.1em%22 font-size=%2265%22 fill=%22white%22 font-family=%22Inter, sans-serif%22 font-weight=%22800%22>J</text></svg>';
            document.getElementsByTagName('head')[0].appendChild(link);
        }

        // 3. Forcibly nuke all default Streamlit branding, deployment, viewer badges, and floating controls
        function killStreamlitBranding() {
            // Sidebar buttons, developer viewer badge, deploy button, status indicator, toolbar
            const selectors = [
                '[data-testid="stExpandSidebarButton"]',
                '[data-testid="stSidebarCollapseButton"]',
                '[data-testid="collapsedControl"]',
                '.viewerBadge',
                '[data-testid="stViewerBadge"]',
                '.stAppDeployButton',
                '[data-testid="viewerBadge"]',
                '#connection-status',
                '[data-testid="stConnectionStatus"]',
                '.stConnectionStatus',
                '[data-testid="stToolbar"]',
                '[data-testid="stDecoration"]',
                '[data-testid="stStatusWidget"]',
                'footer',
                '#MainMenu'
            ];
            selectors.forEach(sel => {
                document.querySelectorAll(sel).forEach(el => {
                    el.style.cssText = 'display:none!important;visibility:hidden!important;opacity:0!important;width:0!important;height:0!important;pointer-events:none!important;position:absolute!important;left:-9999px!important;top:-9999px!important;overflow:hidden!important;';
                });
            });
        }

        // Run immediately
        enforceTitle();
        enforceFavicon();
        killStreamlitBranding();

        // Run on every single DOM mutation to ensure React re-renders do not revert these changes
        const observer = new MutationObserver(() => {
            enforceTitle();
            enforceFavicon();
            killStreamlitBranding();
        });
        observer.observe(document.body, { childList: true, subtree: true });
        
        // Also observe the document title element specifically
        const titleEl = document.querySelector('title');
        if (titleEl) {
            const titleObserver = new MutationObserver(enforceTitle);
            titleObserver.observe(titleEl, { childList: true, characterData: true });
        }
    })();
    </script>
    """,
    unsafe_allow_html=True,
)


def render_navbar():
    # Streamlit isolates HTML div wrappers into empty React nodes.
    # Instead: inject a unique marker BEFORE the columns, then CSS targets
    # [data-testid="stVerticalBlock"]:has(.navbar-marker) > div [data-testid="stHorizontalBlock"]
    st.markdown('<div class="navbar-marker" style="display:none;height:0;"></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([0.14, 1.15, 1.5], gap="small")
    with c1:
        if st.button("☰", key="sidebar_toggle", help="Show or hide sidebar", use_container_width=True):
            st.session_state.sidebar_collapsed = not st.session_state.sidebar_collapsed
            st.rerun()
    with c2:
        st.markdown(
            f"""
            <div class="topbar-brand">
                <div class="topbar-title">{APP_NAME}</div>
                <div class="topbar-subtitle">Enterprise hiring intelligence</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        nav_value = st.radio(
            "Primary navigation",
            NAV_ITEMS,
            horizontal=True,
            label_visibility="collapsed",
            key="top_nav",
        )
    return nav_value


@st.dialog("Schedule Interview")
def schedule_modal(candidate, role):
    candidate_name = candidate.get("Candidate", "")
    candidate_email = candidate.get("Email", "")
    st.markdown("### Schedule Interview")
    st.markdown(f"**{candidate_name}**")
    if is_valid_email(candidate_email):
        st.caption(f"To: {candidate_email}")
    else:
        st.error("Candidate email is missing or invalid. Recheck resume parsing before sending.")

    today = date.today()
    default_mode = INTERVIEW_MODES[0]
    default_link = "https://teams.microsoft.com/l/meetup-join/"

    with st.form("schedule_interview_form", clear_on_submit=False):
        c1, c2 = st.columns(2, gap="medium")
        interview_date = c1.date_input("Interview Date", today)
        time_slot = c2.selectbox("Time Slot", TIME_SLOTS)

        c3, c4 = st.columns(2, gap="medium")
        mode = c3.selectbox("Interview Mode", INTERVIEW_MODES, index=0)
        link = c4.text_input("Teams/Zoom Link", default_link)

        interviewer = st.text_input("Recruiter / Interviewer", "Talent Acquisition Lead")
        notes = st.text_area("Recruiter Notes", placeholder="Panel, round type, prep notes, evaluation focus...")

        subject = st.text_input("Email Subject", default_subject(candidate_name, role))
        body = st.text_area(
            "Email Body",
            default_body(candidate_name, role, interview_date, time_slot, default_mode, default_link),
            height=180,
        )

        c5, c6 = st.columns(2, gap="medium")
        from_email = c5.text_input("From Email", "gouseimmugh@gmail.com")
        cc_email = c6.text_input("CC Email", placeholder="hiring.manager@company.com")

        st.caption("Email preview")
        st.markdown(f'<div class="schedule-preview">{body}</div>', unsafe_allow_html=True)

        submitted = st.form_submit_button("Send & Schedule Interview", type="primary", use_container_width=False)

    if submitted:
        payload = build_interview_payload(
            candidate,
            role,
            {
                "date": interview_date,
                "time": time_slot,
                "mode": mode,
                "link": link,
                "interviewer": interviewer,
                "notes": notes,
                "subject": subject,
                "body": body,
                "from_email": from_email,
                "cc_email": cc_email,
            },
        )
        payload["google_calendar_url"] = google_calendar_url(payload)
        errors = validate_email_payload(payload)
        if errors:
            for error in errors:
                st.error(error)
            return

        with st.spinner("Scheduling interview and sending candidate invite..."):
            email_sent, message = send_interview_email(payload)
            save_interview(payload)

        if email_sent:
            st.success(message)
            st.session_state.invite_notice = f"Invite sent to {candidate_email}"
        else:
            st.warning(f"Interview saved, but email was not sent. {message}")
            st.session_state.invite_notice = f"Interview saved, email failed: {message}"
        st.download_button(
            "Download ICS Invite",
            data=generate_ics(payload),
            file_name="interview-invite.ics",
            mime="text/calendar",
        )
        st.link_button("Open Google Calendar", payload["google_calendar_url"])
        st.session_state.selected_candidate = None


def read_uploaded_file(file):
    if file.name.lower().endswith(".pdf"):
        return read_pdf(file)
    return read_docx(file)


def analyze_resumes(resumes, jd_text, parsed_jd):
    required_skills = parsed_jd.get("required_skills", [])
    required_exp = parsed_jd.get("experience_range", (2, 5))
    results = []
    seen = set()

    for resume in resumes:
        text = read_uploaded_file(resume)
        identity = parse_resume_identity(text, resume.name)
        key = (identity["email"].lower(), identity["name"].lower())
        if key in seen:
            continue
        seen.add(key)

        analysis = score_resume(text, jd_text, required_skills, required_exp)
        results.append(
            {
                "Candidate": identity["name"],
                "Email": identity["email"],
                "Phone": identity["phone"],
                "Experience": analysis["experience"],
                "Score": analysis["score"],
                "Eligible": analysis["eligibility"],
                "Recommendation": analysis["recommendation"],
                "Skill Match %": analysis["skill_match"],
                "Matched Skills": analysis["matched"],
                "Missing Skills": analysis["missing"],
                "Summary": f"{analysis['recommendation']} based on {analysis['skill_match']}% skill match and {analysis['experience']} years of extracted experience.",
            }
        )

    if not results:
        return pd.DataFrame()

    df = pd.DataFrame(results).sort_values("Score", ascending=False).reset_index(drop=True)
    df.insert(0, "Rank", range(1, len(df) + 1))
    return df


def render_dashboard():
    hero_section()
    interviews = get_interviews()

    if st.session_state.results_df is not None and not st.session_state.results_df.empty:
        render_insight_cards(st.session_state.results_df, len(interviews))
    else:
        render_insight_cards(pd.DataFrame(columns=["Eligible", "Score"]), len(interviews))

    left, right = st.columns([1.55, 1], gap="large")

    with left:
        st.subheader("JD Intelligence")
        jd_file = st.file_uploader("Upload Job Description PDF", type=["pdf"], label_visibility="collapsed")
        if jd_file:
            jd_text = read_pdf(jd_file)
            parsed = parse_job_description(jd_text)
            st.session_state.jd_text = jd_text
            st.session_state.parsed_jd = parsed
            st.session_state.active_role = parsed.get("job_title", "Auto Parsed Role")
        st.markdown(
            """
            <div class="jd-alert-banner">
                <span class="jd-alert-icon">✔</span>
                <div>
                    <p class="jd-alert-title">Job description parsed and fields auto-populated.</p>
                    <p class="jd-alert-copy">AI extracted role, experience, location, notice period, employment type, and skills for your hiring workflow.</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        parsed_jd = st.session_state.parsed_jd
        if parsed_jd:
            render_jd_summary(parsed_jd)
            exp = parsed_jd.get("experience_range", (2, 5))
            st.slider("Auto Extracted Experience Range", 0, 25, exp, disabled=True)
        else:
            st.info("Upload a JD PDF to auto extract title, experience, skills, location, responsibilities, employment type, and notice period.")

    with right:
        st.subheader("Interview Schedule")
        if not interviews.empty:
            for _, row in interviews.tail(4).iterrows():
                interview_card(row)
        else:
            st.info("No interviews scheduled yet.")

    st.divider()
    st.subheader("Resume Intake")
    resumes = st.file_uploader(
        "Batch Upload Resumes",
        type=["pdf", "docx"],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )

    ready = bool(st.session_state.jd_text and st.session_state.parsed_jd and resumes)
    st.markdown('<div class="analysis-cta-wrap"></div>', unsafe_allow_html=True)
    cta_left, cta_mid, cta_right = st.columns([1.2, 0.8, 1.2])
    with cta_mid:
        run_analysis = st.button("Run ATS Analysis", type="primary", use_container_width=True, disabled=not ready)

    if run_analysis:
        with st.status("Parsing resumes, extracting candidate identity, and ranking matches...", expanded=True) as status:
            df = analyze_resumes(resumes, st.session_state.jd_text, st.session_state.parsed_jd)
            st.session_state.results_df = df
            status.update(label="Analysis complete", state="complete", expanded=False)
        st.rerun()

    if not ready:
        st.caption("Upload a JD and at least one resume to enable automated scoring.")

    render_results()
    render_analytics()


def render_results():
    df = st.session_state.results_df
    if df is None or df.empty:
        return

    st.divider()
    st.subheader("ATS Results Grid")
    st.markdown('<div class="results-shell">', unsafe_allow_html=True)
    render_results_header()

    for _, row in df.iterrows():
        action, _ = candidate_row(row, int(row["Rank"]))
        if action:
            st.session_state.selected_candidate = row.to_dict()
            schedule_modal(row.to_dict(), st.session_state.active_role)
    st.markdown("</div>", unsafe_allow_html=True)


def render_analytics():
    df = st.session_state.results_df
    if df is None or df.empty:
        return

    st.divider()
    st.subheader("Recruitment Analytics")
    tab1, tab2, tab3 = st.tabs(["Pipeline", "Skills", "Experience"])
    with tab1:
        c1, c2 = st.columns(2, gap="large")
        c1.plotly_chart(score_chart(df), use_container_width=True)
        c2.plotly_chart(eligibility_chart(df), use_container_width=True)
        c3, c4 = st.columns(2, gap="large")
        c3.plotly_chart(candidate_funnel(df), use_container_width=True)
        c4.plotly_chart(shortlisted_vs_rejected(df), use_container_width=True)
    with tab2:
        c1, c2 = st.columns(2, gap="large")
        c1.plotly_chart(skill_match_heatmap(df), use_container_width=True)
        c2.plotly_chart(top_skills_chart(df), use_container_width=True)
    with tab3:
        c1, c2 = st.columns(2, gap="large")
        c1.plotly_chart(experience_distribution(df), use_container_width=True)
        c2.plotly_chart(ats_score_distribution(df), use_container_width=True)


def render_calendar():
    st.title("Interview Calendar")
    interviews = get_interviews()
    if interviews.empty:
        st.info("No interviews scheduled yet.")
        return

    today_str = str(date.today())
    todays = interviews[interviews["date"] == today_str]
    upcoming = interviews[interviews["date"] >= today_str]

    c1, c2, c3 = st.columns(3, gap="medium")
    with c1:
        st.metric("Today's Interviews", len(todays))
    with c2:
        st.metric("Upcoming", len(upcoming))
    with c3:
        st.metric("Total Scheduled", len(interviews))

    st.subheader("Today's Interviews")
    if todays.empty:
        st.caption("No interviews today.")
    else:
        for _, row in todays.iterrows():
            interview_card(row)

    st.subheader("Recruiter Schedule")
    for day, group in upcoming.groupby("date"):
        with st.expander(f"{day} · {len(group)} interview(s)", expanded=(day == today_str)):
            for _, row in group.iterrows():
                cols = st.columns([2.1, 1.1, 1.2, 1.1, 0.8], gap="small")
                cols[0].markdown(f"**{row['name']}**")
                cols[0].caption(row["email"])
                cols[1].write(row["time"])
                cols[2].write(row["mode"])
                cols[3].write(row["status"])
                if cols[4].button("Cancel", key=f"cancel_{row['id']}"):
                    delete_interview(row["id"])
                    st.rerun()

    st.subheader("Calendar Data")
    st.dataframe(
        interviews,
        use_container_width=True,
        hide_index=True,
        column_config={
            "link": st.column_config.LinkColumn("Meeting Link"),
            "email": st.column_config.TextColumn("Candidate Email"),
            "date": st.column_config.DateColumn("Date"),
        },
    )


def render_settings():
    st.title("System Settings")
    st.info("Email sending uses secure environment variables. For Gmail, enable 2-step verification and use an app password.")
    with st.expander("Email Defaults", expanded=True):
        st.text_input("Default From Email", "gouseimmugh@gmail.com")
        st.text_input("Default Meeting Provider", "Microsoft Teams")
        st.toggle("Require recruiter notes before scheduling", value=False)
    with st.expander("SMTP Configuration", expanded=False):
        st.code(
            "SMTP_HOST=smtp.gmail.com\n"
            "SMTP_PORT=587\n"
            "SMTP_USERNAME=gouseimmugh@gmail.com\n"
            "SMTP_PASSWORD=<gmail_app_password>\n"
            "SMTP_USE_SSL=false",
            language="bash",
        )


sidebar_panel()
nav = render_navbar()

if st.session_state.invite_notice:
    st.toast(st.session_state.invite_notice)
    st.session_state.invite_notice = None

if nav == "Dashboard":
    render_dashboard()
elif nav == "Interview Calendar":
    render_calendar()
elif nav == "Analytics":
    if st.session_state.results_df is None or st.session_state.results_df.empty:
        st.title("Recruitment Analytics")
        st.info("Run ATS analysis to populate analytics.")
    else:
        render_analytics()
else:
    render_settings()
