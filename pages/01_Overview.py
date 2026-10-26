
import pandas as pd
import plotly.express as px
import streamlit as st

from utils.data_loader import load_data, get_dataset_summary
from utils.analytics import (
    get_club_injury_counts,
    get_injury_counts,
    get_top_performance_drops,
)


# --------------------------------------------------
# PAGE SETUP
# --------------------------------------------------

st.title("The Injury & Performance Overview")

st.markdown(
    """
    Explore how player injuries relate to individual ratings
    and football team performance across the complete dataset.
    """
)

st.caption("PITCHSIDE  /  OVERVIEW")


# --------------------------------------------------
# LOAD THE COMPLETE DATASET
# --------------------------------------------------

try:
    df = load_data()
except FileNotFoundError as error:
    st.error(str(error))
    st.info(
        "Check that football_injury_cleaned.csv is inside "
        "the project's data folder."
    )
    st.stop()

summary = get_dataset_summary(df)


# --------------------------------------------------
# KEY METRICS
# --------------------------------------------------

st.subheader("Dataset at a glance")

metric1, metric2, metric3, metric4 = st.columns(4)

metric1.metric(
    "Injury records",
    f"{summary['records']:,}",
)

metric2.metric(
    "Unique players",
    f"{summary['players']:,}",
)

metric3.metric(
    "Football clubs",
    f"{summary['clubs']:,}",
)

metric4.metric(
    "Recorded injury types",
    f"{summary['injury_types']:,}",
)

st.divider()


# --------------------------------------------------
# CHART 1: INJURIES BY CLUB
# --------------------------------------------------

left, right = st.columns([1.15, 0.85])

with left:
    st.subheader("Injury records by club")
    st.caption(
        "Every club in the dataset is included. "
        "Counts represent injury records, not unique players."
    )

    club_counts = get_club_injury_counts(df).reset_index()
    club_counts.columns = ["Club", "Injury Records"]

    club_counts = club_counts.sort_values(
        "Injury Records",
        ascending=True,
    )

    fig_clubs = px.bar(
        club_counts,
        x="Injury Records",
        y="Club",
        orientation="h",
        text="Injury Records",
        template="plotly_dark",
        color="Injury Records",
        color_continuous_scale=[
            "#183B45",
            "#267F70",
            "#65E6B4",
        ],
    )

    fig_clubs.update_traces(
        textposition="outside",
        cliponaxis=False,
    )

    fig_clubs.update_layout(
        height=430,
        showlegend=False,
        coloraxis_showscale=False,
        xaxis_title="Number of injury records",
        yaxis_title="",
        margin=dict(l=10, r=30, t=20, b=20),
    )

    st.plotly_chart(
        fig_clubs,
        use_container_width=True,
    )


# --------------------------------------------------
# CHART 2: INJURY TYPE DISTRIBUTION
# --------------------------------------------------

with right:
    st.subheader("Injury type distribution")
    st.caption(
        "Frequency of the recorded injury categories."
    )

    injury_counts = get_injury_counts(df).reset_index()
    injury_counts.columns = ["Injury", "Records"]

    injury_counts = injury_counts.head(10)

    fig_injuries = px.pie(
        injury_counts,
        names="Injury",
        values="Records",
        hole=0.62,
        template="plotly_dark",
        color_discrete_sequence=[
            "#65E6B4",
            "#39B7A5",
            "#318A91",
            "#386B8C",
            "#5865A8",
            "#8872B7",
            "#B47AA8",
            "#D49A88",
            "#D7BE7A",
            "#8FA5C0",
        ],
    )

    fig_injuries.update_traces(
        textposition="inside",
        textinfo="percent",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Records: %{value}<br>"
            "Share: %{percent}"
            "<extra></extra>"
        ),
    )

    fig_injuries.update_layout(
        height=430,
        margin=dict(l=10, r=10, t=20, b=20),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.08,
            xanchor="left",
            x=0,
        ),
    )

    st.plotly_chart(
        fig_injuries,
        use_container_width=True,
    )


st.divider()


# --------------------------------------------------
# CHART 3: TEAM PERFORMANCE IMPACT
# --------------------------------------------------

st.subheader("Which absences had the largest performance impact?")

st.markdown(
    """
    The **Team Performance Drop Index** compares average goal
    difference before an injury with average goal difference
    during the player's recorded absence. A higher positive
    value indicates a larger decline in this measure.
    """
)

top_drops = get_top_performance_drops(df, n=10).copy()

if not top_drops.empty:
    top_drops["Player / Club"] = (
        top_drops["Name"].astype(str)
        + " · "
        + top_drops["Team Name"].astype(str)
    )

    top_drops = top_drops.sort_values(
        "Team Performance Drop Index",
        ascending=True,
    )

    fig_drops = px.bar(
        top_drops,
        x="Team Performance Drop Index",
        y="Player / Club",
        orientation="h",
        text="Team Performance Drop Index",
        template="plotly_dark",
        color="Team Performance Drop Index",
        color_continuous_scale=[
            "#245B58",
            "#39B7A5",
            "#65E6B4",
        ],
        hover_data={
            "Injury": True,
            "Team Performance Drop Index": ":.2f",
            "Player / Club": False,
        },
    )

    fig_drops.update_traces(
        texttemplate="%{x:.2f}",
        textposition="outside",
        cliponaxis=False,
    )

    fig_drops.update_layout(
        height=440,
        coloraxis_showscale=False,
        xaxis_title="Team Performance Drop Index",
        yaxis_title="",
        margin=dict(l=10, r=45, t=20, b=20),
    )

    st.plotly_chart(
        fig_drops,
        use_container_width=True,
    )
else:
    st.info(
        "No valid performance-drop values are available "
        "for this chart."
    )


# --------------------------------------------------
# DATA QUALITY NOTE
# --------------------------------------------------

st.divider()

st.subheader("About the data")

missing_cells = int(df.isna().sum().sum())
total_cells = int(df.shape[0] * df.shape[1])
missing_percentage = (
    missing_cells / total_cells * 100
    if total_cells
    else 0
)

col_a, col_b = st.columns(2)

col_a.metric(
    "Columns in the loaded dataset",
    f"{df.shape[1]:,}",
)

col_b.metric(
    "Missing cells",
    f"{missing_cells:,}",
)

st.caption(
    f"{missing_percentage:.1f}% of the cells in the loaded "
    "dataset are missing. Missing values are retained where "
    "appropriate rather than automatically treated as zero."
)

st.markdown(
    """
    <div style="
        color: #8FA5C0;
        font-size: 12px;
        padding-top: 16px;
    ">
        PITCHSIDE · Football Injury Analytics
    </div>
    """,
    unsafe_allow_html=True,
)
