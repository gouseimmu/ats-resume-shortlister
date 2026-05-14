import plotly.express as px


def score_chart(df):

    fig = px.bar(
        df,
        x="Resume",
        y="Score",
        color="Eligible",
        text="Score",
        height=420,
        template="plotly_dark"
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_title="Candidates",
        yaxis_title="ATS Score"
    )

    return fig


def eligibility_chart(df):

    counts = df["Eligible"].value_counts().reset_index()
    counts.columns = ["Status", "Count"]

    fig = px.pie(
        counts,
        names="Status",
        values="Count",
        hole=0.5,
        template="plotly_dark"
    )

    return fig