
import pandas as pd
import plotly.express as px
import streamlit as st

from utils.data_loader import load_data


# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

st.title("Team Performance")

st.markdown(
    """
    Examine recorded goal-difference patterns during player absences
    and compare performance-drop indicators across football clubs.
    """
)

st.caption("PITCHSIDE  /  CLUB INTELLIGENCE")


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

try:
    df = load_data()
except FileNotFoundError as error:
    st.error(str(error))
    st.stop()

required_columns = [
    "Name",
    "Team Name",
    "Injury",
    "Average GD Before Injury",
    "Average GD During Absence",
    "Team Performance Drop Index",
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    st.error(
        "The dataset is missing required columns: "
        + ", ".join(missing_columns)
    )
    st.stop()


# --------------------------------------------------
# CLUB FILTER
# --------------------------------------------------

st.subheader("Choose your comparison")

clubs = sorted(
    df["Team Name"].dropna().astype(str).unique().tolist()
)

selected_clubs = st.multiselect(
    "Clubs to compare",
    options=clubs,
    default=clubs,
    help=(
        "All clubs are selected by default. "
        "Remove clubs to focus on a smaller comparison."
    ),
)

if selected_clubs:
    filtered = df[
        df["Team Name"].astype(str).isin(selected_clubs)
    ].copy()
else:
    filtered = df.iloc[0:0].copy()
    st.warning("Select at least one club to display comparisons.")


# --------------------------------------------------
# SUMMARY METRICS
# --------------------------------------------------

valid_drop = pd.to_numeric(
    filtered["Team Performance Drop Index"],
    errors="coerce",
).dropna()

valid_before = pd.to_numeric(
    filtered["Average GD Before Injury"],
    errors="coerce",
).dropna()

valid_during = pd.to_numeric(
    filtered["Average GD During Absence"],
    errors="coerce",
).dropna()

st.divider()
st.subheader("Performance snapshot")

metric1, metric2, metric3, metric4 = st.columns(4)

metric1.metric(
    "Injury records",
    f"{len(filtered):,}",
)

metric2.metric(
    "Clubs selected",
    f"{filtered['Team Name'].nunique():,}",
)

metric3.metric(
    "Mean performance-drop index",
    f"{valid_drop.mean():.2f}"
    if not valid_drop.empty
    else "N/A",
    help=(
        "Calculated across records with a valid index. "
        "Positive values indicate a decline in average goal difference."
    ),
)

metric4.metric(
    "Records with valid index",
    f"{len(valid_drop):,}",
)


# --------------------------------------------------
# CHART 1: AVERAGE GOAL DIFFERENCE
# --------------------------------------------------

st.divider()
st.subheader("Before injury vs. during absence")

st.markdown(
    """
    Each point represents a club. The two averages are calculated
    across the available injury records for that club. Differences
    describe the dataset and do not, by themselves, prove that
    injuries caused the change.
    """
)

if not filtered.empty:
    comparison = (
        filtered.groupby("Team Name", as_index=False)
        .agg(
            Average_Before=(
                "Average GD Before Injury",
                "mean",
            ),
            Average_During=(
                "Average GD During Absence",
                "mean",
            ),
            Injury_Records=("Name", "size"),
        )
        .dropna(
            subset=["Average_Before", "Average_During"]
        )
    )

    if not comparison.empty:
        fig_comparison = px.scatter(
            comparison,
            x="Average_Before",
            y="Average_During",
            size="Injury_Records",
            hover_name="Team Name",
            hover_data={
                "Average_Before": ":.2f",
                "Average_During": ":.2f",
                "Injury_Records": True,
            },
            template="plotly_dark",
            color="Team Name",
            labels={
                "Average_Before": "Average goal difference before injury",
                "Average_During": "Average goal difference during absence",
                "Injury_Records": "Injury records",
                "Team Name": "Club",
            },
        )

        # Reference line: equal averages before and during absence.
        all_values = pd.concat(
            [
                comparison["Average_Before"],
                comparison["Average_During"],
            ],
            ignore_index=True,
        )

        lower = float(all_values.min())
        upper = float(all_values.max())

        fig_comparison.add_shape(
            type="line",
            x0=lower,
            y0=lower,
            x1=upper,
            y1=upper,
            line=dict(
                color="#8FA5C0",
                dash="dash",
                width=1,
            ),
        )

        fig_comparison.update_layout(
            height=480,
            xaxis_title="Goal difference before injury",
            yaxis_title="Goal difference during absence",
            legend_title="Club",
            margin=dict(l=10, r=10, t=25, b=20),
        )

        st.plotly_chart(
            fig_comparison,
            use_container_width=True,
        )
    else:
        st.info(
            "Not enough valid before-and-during averages "
            "are available for this comparison."
        )


# --------------------------------------------------
# CHART 2: CLUB PERFORMANCE-DROP INDEX
# --------------------------------------------------

st.divider()
st.subheader("Which clubs have the largest average drop?")

st.markdown(
    """
    The index is defined as average goal difference before injury
    minus average goal difference during the player's absence.
    Positive values indicate a decline; negative values indicate
    a higher average goal difference during absence.
    """
)

if not filtered.empty:
    club_drop = (
        filtered.groupby("Team Name", as_index=False)
        .agg(
            Average_Drop=(
                "Team Performance Drop Index",
                "mean",
            ),
            Valid_Records=(
                "Team Performance Drop Index",
                "count",
            ),
        )
        .dropna(subset=["Average_Drop"])
        .sort_values("Average_Drop", ascending=True)
    )

    if not club_drop.empty:
        fig_drop = px.bar(
            club_drop,
            x="Average_Drop",
            y="Team Name",
            orientation="h",
            text="Average_Drop",
            color="Average_Drop",
            color_continuous_scale=[
                "#4C80A5",
                "#267F70",
                "#65E6B4",
            ],
            template="plotly_dark",
            hover_data={
                "Average_Drop": ":.2f",
                "Valid_Records": True,
            },
            labels={
                "Average_Drop": "Mean performance-drop index",
                "Team Name": "Club",
                "Valid_Records": "Records with valid index",
            },
        )

        fig_drop.update_traces(
            texttemplate="%{x:.2f}",
            textposition="outside",
            cliponaxis=False,
        )

        fig_drop.update_layout(
            height=max(350, 48 * len(club_drop)),
            coloraxis_showscale=False,
            xaxis_title="Mean performance-drop index",
            yaxis_title="",
            margin=dict(l=10, r=45, t=20, b=20),
        )

        st.plotly_chart(
            fig_drop,
            use_container_width=True,
        )
    else:
        st.info(
            "No valid performance-drop indices are available "
            "for the selected clubs."
        )


# --------------------------------------------------
# CHART 3: LARGEST INDIVIDUAL RECORD DROPS
# --------------------------------------------------

st.divider()
st.subheader("Largest recorded performance drops")

if not filtered.empty:
    record_drops = filtered.dropna(
        subset=["Team Performance Drop Index"]
    ).nlargest(
        10,
        "Team Performance Drop Index",
    ).copy()

    if not record_drops.empty:
        record_drops["Player / Club"] = (
            record_drops["Name"].astype(str)
            + " · "
            + record_drops["Team Name"].astype(str)
        )

        record_drops = record_drops.sort_values(
            "Team Performance Drop Index",
            ascending=True,
        )

        fig_records = px.bar(
            record_drops,
            x="Team Performance Drop Index",
            y="Player / Club",
            orientation="h",
            text="Team Performance Drop Index",
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
            template="plotly_dark",
        )

        fig_records.update_traces(
            texttemplate="%{x:.2f}",
            textposition="outside",
            cliponaxis=False,
        )

        fig_records.update_layout(
            height=430,
            coloraxis_showscale=False,
            xaxis_title="Team Performance Drop Index",
            yaxis_title="",
            margin=dict(l=10, r=45, t=20, b=20),
        )

        st.plotly_chart(
            fig_records,
            use_container_width=True,
        )
    else:
        st.info(
            "No valid individual performance-drop records "
            "are available."
        )


# --------------------------------------------------
# CLUB SUMMARY TABLE
# --------------------------------------------------

st.divider()
st.subheader("Club comparison table")

if not filtered.empty:
    summary_table = (
        filtered.groupby("Team Name", as_index=False)
        .agg(
            Injury_Records=("Name", "size"),
            Unique_Players=("Name", "nunique"),
            Mean_GD_Before=(
                "Average GD Before Injury",
                "mean",
            ),
            Mean_GD_During=(
                "Average GD During Absence",
                "mean",
            ),
            Mean_Performance_Drop=(
                "Team Performance Drop Index",
                "mean",
            ),
        )
        .sort_values(
            "Mean_Performance_Drop",
            ascending=False,
            na_position="last",
        )
    )

    summary_table = summary_table.rename(
        columns={
            "Team Name": "Club",
            "Injury_Records": "Injury Records",
            "Unique_Players": "Unique Players",
            "Mean_GD_Before": "Mean GD Before Injury",
            "Mean_GD_During": "Mean GD During Absence",
            "Mean_Performance_Drop": "Mean Performance-Drop Index",
        }
    )

    st.dataframe(
        summary_table,
        use_container_width=True,
        hide_index=True,
    )
