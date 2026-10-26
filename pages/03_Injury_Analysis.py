
import pandas as pd
import plotly.express as px
import streamlit as st

from utils.data_loader import load_data
from utils.analytics import get_monthly_injury_counts


# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

st.title("Injury Analysis")

st.markdown(
    "Investigate injury frequency, injury categories, "
    "seasonal patterns, and recovery durations."
)

st.caption("PITCHSIDE  /  INJURY INTELLIGENCE")


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

try:
    df = load_data()
except FileNotFoundError as error:
    st.error(str(error))
    st.stop()

if df.empty:
    st.warning("No records are available for analysis.")
    st.stop()

required_columns = [
    "Injury",
    "Team Name",
    "Date of Injury",
    "Injury Duration (Days)",
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    st.error(
        "Missing required columns: "
        + ", ".join(missing_columns)
    )
    st.stop()


# --------------------------------------------------
# FILTERS
# --------------------------------------------------

st.subheader("Explore injury categories")

injury_options = sorted(
    df["Injury"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

injury_choice = st.selectbox(
    "Injury category",
    options=["All injury types"] + injury_options,
)

team_options = sorted(
    df["Team Name"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

team_choice = st.selectbox(
    "Club",
    options=["All clubs"] + team_options,
)

filtered = df.copy()

if injury_choice != "All injury types":
    filtered = filtered[
        filtered["Injury"].astype(str) == injury_choice
    ]

if team_choice != "All clubs":
    filtered = filtered[
        filtered["Team Name"].astype(str) == team_choice
    ]


# --------------------------------------------------
# SUMMARY METRICS
# --------------------------------------------------

st.divider()

valid_durations = pd.to_numeric(
    filtered["Injury Duration (Days)"],
    errors="coerce",
)

valid_durations = valid_durations[
    valid_durations.notna() & (valid_durations >= 0)
]

metric1, metric2, metric3 = st.columns(3)

metric1.metric(
    "Matching injury records",
    f"{len(filtered):,}",
)

metric2.metric(
    "Distinct injury categories",
    f"{filtered['Injury'].nunique():,}",
)

metric3.metric(
    "Median recovery duration",
    (
        f"{valid_durations.median():.0f} days"
        if not valid_durations.empty
        else "N/A"
    ),
)

st.caption(
    "Recovery statistics exclude missing and negative durations. "
    "The median is less sensitive to unusually long recovery records "
    "than the mean."
)


# --------------------------------------------------
# CHART 1: MOST FREQUENT INJURIES
# --------------------------------------------------

st.divider()
st.subheader("Most frequently recorded injuries")

injury_counts = (
    filtered["Injury"]
    .dropna()
    .astype(str)
    .value_counts()
    .head(12)
    .sort_values(ascending=True)
    .reset_index()
)

injury_counts.columns = ["Injury Type", "Records"]

if not injury_counts.empty:
    fig_injury = px.bar(
        injury_counts,
        x="Records",
        y="Injury Type",
        orientation="h",
        text="Records",
        template="plotly_dark",
        color="Records",
        color_continuous_scale=[
            "#183B45",
            "#267F70",
            "#65E6B4",
        ],
    )

    fig_injury.update_traces(
        textposition="outside",
        cliponaxis=False,
    )

    fig_injury.update_layout(
        height=440,
        showlegend=False,
        coloraxis_showscale=False,
        xaxis_title="Number of records",
        yaxis_title="",
        margin=dict(l=10, r=35, t=20, b=20),
    )

    st.plotly_chart(
        fig_injury,
        use_container_width=True,
    )
else:
    st.info("No injury categories match these filters.")


# --------------------------------------------------
# CHART 2: MONTHLY INJURY PATTERNS
# --------------------------------------------------

st.divider()
st.subheader("When are injuries recorded?")

st.markdown(
    "This chart groups recorded injury dates by calendar month. "
    "It shows the timing of records, not the probability that a "
    "player will get injured in a particular month."
)

dated_data = filtered.dropna(
    subset=["Date of Injury"]
).copy()

if not dated_data.empty:
    dated_data["Month"] = (
        dated_data["Date of Injury"].dt.month
    )

    monthly_counts = (
        dated_data.groupby("Month")
        .size()
        .reindex(range(1, 13), fill_value=0)
        .reset_index(name="Injury Records")
    )

    month_names = {
        1: "Jan",
        2: "Feb",
        3: "Mar",
        4: "Apr",
        5: "May",
        6: "Jun",
        7: "Jul",
        8: "Aug",
        9: "Sep",
        10: "Oct",
        11: "Nov",
        12: "Dec",
    }

    monthly_counts["Month Name"] = (
        monthly_counts["Month"].map(month_names)
    )

    fig_monthly = px.line(
        monthly_counts,
        x="Month Name",
        y="Injury Records",
        markers=True,
        template="plotly_dark",
        color_discrete_sequence=["#65E6B4"],
    )

    fig_monthly.update_traces(
        line=dict(width=3),
        marker=dict(size=9),
    )

    fig_monthly.update_layout(
        height=350,
        xaxis_title="Calendar month",
        yaxis_title="Injury records",
        margin=dict(l=10, r=20, t=20, b=20),
    )

    st.plotly_chart(
        fig_monthly,
        use_container_width=True,
    )
else:
    st.info(
        "No valid injury dates are available for the selected filters."
    )


# --------------------------------------------------
# CHART 3: CLUB-MONTH HEATMAP
# --------------------------------------------------

st.divider()
st.subheader("Injury frequency across clubs and months")

st.markdown(
    "Each cell represents the number of recorded injuries "
    "for one club in one calendar month."
)

heatmap_source = (
    dated_data
    if not dated_data.empty
    else filtered.dropna(subset=["Date of Injury"]).copy()
)

if not heatmap_source.empty:
    heatmap_data = heatmap_source.copy()
    heatmap_data["Month"] = (
        heatmap_data["Date of Injury"].dt.month
    )

    pivot = pd.pivot_table(
        heatmap_data,
        index="Team Name",
        columns="Month",
        values="Name",
        aggfunc="count",
        fill_value=0,
    )

    pivot = pivot.reindex(
        columns=range(1, 13),
        fill_value=0,
    )

    pivot.columns = [
        month_names[month]
        for month in pivot.columns
    ]

    fig_heatmap = px.imshow(
        pivot,
        aspect="auto",
        color_continuous_scale=[
            "#142238",
            "#267F70",
            "#65E6B4",
        ],
        labels={
            "x": "Month",
            "y": "Club",
            "color": "Records",
        },
        template="plotly_dark",
    )

    fig_heatmap.update_layout(
        height=max(350, 45 * len(pivot)),
        margin=dict(l=10, r=10, t=20, b=20),
    )

    st.plotly_chart(
        fig_heatmap,
        use_container_width=True,
    )
else:
    st.info("No dated records are available for the heatmap.")


# --------------------------------------------------
# CHART 4: RECOVERY DURATION DISTRIBUTION
# --------------------------------------------------

st.divider()
st.subheader("Recovery duration distribution")

duration_data = filtered.copy()

duration_data["Injury Duration (Days)"] = pd.to_numeric(
    duration_data["Injury Duration (Days)"],
    errors="coerce",
)

duration_data = duration_data[
    duration_data["Injury Duration (Days)"].notna()
    & (duration_data["Injury Duration (Days)"] >= 0)
]

if not duration_data.empty:
    fig_duration = px.histogram(
        duration_data,
        x="Injury Duration (Days)",
        nbins=30,
        template="plotly_dark",
        color_discrete_sequence=["#65E6B4"],
        labels={
            "Injury Duration (Days)": "Recovery duration (days)",
            "count": "Injury records",
        },
    )

    fig_duration.update_layout(
        height=360,
        xaxis_title="Recovery duration (days)",
        yaxis_title="Number of records",
        margin=dict(l=10, r=20, t=20, b=20),
    )

    st.plotly_chart(
        fig_duration,
        use_container_width=True,
    )
else:
    st.info(
        "No valid recovery durations match the selected filters."
    )


# --------------------------------------------------
# DATA TABLE
# --------------------------------------------------

st.divider()
st.subheader("Records behind the analysis")

table_columns = [
    "Name",
    "Team Name",
    "Injury",
    "Date of Injury",
    "Date of return",
    "Injury Duration (Days)",
]

available_columns = [
    column for column in table_columns
    if column in filtered.columns
]

st.dataframe(
    filtered[available_columns],
    use_container_width=True,
    hide_index=True,
)

st.caption(
    f"{len(filtered):,} record(s) match the current selections."
)
