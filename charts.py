import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


STATUS_COLORS = {
    "Eligible": "#16a34a",
    "Shortlisted": "#16a34a",
    "Consider": "#f59e0b",
    "Rejected": "#dc2626",
}

PALETTE = ["#2563eb", "#0891b2", "#7c3aed", "#0f766e", "#f59e0b", "#dc2626"]


def apply_enterprise_layout(fig, height=340):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", size=12, color="#1f2937"),
        margin=dict(t=42, b=28, l=34, r=24),
        hoverlabel=dict(bgcolor="#111827", font_color="#ffffff", bordercolor="#111827"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    fig.update_xaxes(showgrid=False, zeroline=False, linecolor="#e5e7eb")
    fig.update_yaxes(gridcolor="#eef2f7", zeroline=False, linecolor="#e5e7eb")
    return fig


def score_chart(df):
    data = df.sort_values("Score", ascending=False).head(12)
    fig = px.bar(
        data,
        x="Candidate",
        y="Score",
        color="Eligible",
        text="Score",
        color_discrete_map=STATUS_COLORS,
        title="ATS Score Distribution",
    )
    fig.update_traces(texttemplate="%{text:.0f}", textposition="outside", marker_line_width=0)
    fig.update_yaxes(range=[0, 105], title="")
    fig.update_xaxes(title="", tickangle=-20)
    return apply_enterprise_layout(fig, 360)


def eligibility_chart(df):
    counts = df["Eligible"].value_counts().reset_index()
    counts.columns = ["Status", "Count"]
    fig = px.pie(
        counts,
        names="Status",
        values="Count",
        hole=0.64,
        color="Status",
        color_discrete_map=STATUS_COLORS,
        title="Eligibility Mix",
    )
    fig.update_traces(textinfo="percent+label", marker=dict(line=dict(color="#ffffff", width=3)))
    fig.update_layout(annotations=[dict(text="Pipeline", x=0.5, y=0.5, showarrow=False, font_size=17)])
    return apply_enterprise_layout(fig, 340)


def skill_match_heatmap(df):
    rows = []
    for _, row in df.iterrows():
        matched = set(row.get("Matched Skills", []))
        missing = set(row.get("Missing Skills", []))
        skills = list(matched | missing)[:12]
        for skill in skills:
            rows.append({"Candidate": row["Candidate"], "Skill": skill, "Match": 1 if skill in matched else 0})

    heat = pd.DataFrame(rows)
    if heat.empty:
        return empty_chart("Skill Match Heatmap")

    pivot = heat.pivot_table(index="Candidate", columns="Skill", values="Match", fill_value=0)
    fig = px.imshow(
        pivot,
        color_continuous_scale=[[0, "#fee2e2"], [1, "#16a34a"]],
        aspect="auto",
        title="Skill Match Heatmap",
    )
    fig.update_coloraxes(showscale=False)
    return apply_enterprise_layout(fig, 360)


def ats_score_distribution(df):
    fig = px.histogram(
        df,
        x="Score",
        color="Eligible",
        nbins=10,
        color_discrete_map=STATUS_COLORS,
        title="ATS Score Bands",
    )
    fig.update_xaxes(title="Score")
    fig.update_yaxes(title="Candidates")
    return apply_enterprise_layout(fig, 330)


def experience_distribution(df):
    fig = px.histogram(
        df,
        x="Experience",
        color="Eligible",
        nbins=8,
        color_discrete_map=STATUS_COLORS,
        title="Experience Distribution",
    )
    fig.update_xaxes(title="Years")
    fig.update_yaxes(title="Candidates")
    return apply_enterprise_layout(fig, 330)


def top_skills_chart(df):
    counter = {}
    for skills in df.get("Matched Skills", []):
        for skill in skills:
            counter[skill] = counter.get(skill, 0) + 1
    data = pd.DataFrame(sorted(counter.items(), key=lambda x: x[1], reverse=True)[:10], columns=["Skill", "Count"])
    if data.empty:
        return empty_chart("Top Matched Skills")
    fig = px.bar(data, y="Skill", x="Count", orientation="h", color_discrete_sequence=["#2563eb"], title="Top Matched Skills")
    fig.update_yaxes(title="", categoryorder="total ascending")
    fig.update_xaxes(title="Candidates")
    return apply_enterprise_layout(fig, 340)


def candidate_funnel(df):
    total = len(df)
    considered = len(df[df["Eligible"].isin(["Eligible", "Consider"])])
    eligible = len(df[df["Eligible"] == "Eligible"])
    scheduled = len(df[df.get("Scheduled", False) == True]) if "Scheduled" in df else 0
    fig = go.Figure(go.Funnel(
        y=["Applicants", "Qualified Review", "Shortlisted", "Scheduled"],
        x=[total, considered, eligible, scheduled],
        marker={"color": ["#2563eb", "#0891b2", "#16a34a", "#7c3aed"]},
        textinfo="value+percent initial",
    ))
    fig.update_layout(title="Candidate Funnel")
    return apply_enterprise_layout(fig, 340)


def shortlisted_vs_rejected(df):
    counts = {
        "Shortlisted": len(df[df["Eligible"] == "Eligible"]),
        "Consider": len(df[df["Eligible"] == "Consider"]),
        "Rejected": len(df[df["Eligible"] == "Rejected"]),
    }
    data = pd.DataFrame({"Status": list(counts.keys()), "Count": list(counts.values())})
    fig = px.bar(data, x="Status", y="Count", color="Status", color_discrete_map=STATUS_COLORS, title="Shortlisted vs Rejected")
    fig.update_xaxes(title="")
    fig.update_yaxes(title="Candidates")
    return apply_enterprise_layout(fig, 320)


def empty_chart(title):
    fig = go.Figure()
    fig.update_layout(title=title, annotations=[dict(text="No data yet", x=0.5, y=0.5, showarrow=False)])
    return apply_enterprise_layout(fig, 320)

