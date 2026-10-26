
import pandas as pd
import plotly.express as px
import streamlit as st

from utils.data_loader import load_data
from utils.analytics import get_player_rating_timeline


# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

st.title("Player Explorer")
st.markdown(
    "Explore individual injury records, rating changes, "
    "and recovery patterns across the dataset."
)
st.caption("PITCHSIDE  /  PLAYER INTELLIGENCE")


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

try:
    df = load_data()
except FileNotFoundError as error:
    st.error(str(error))
    st.stop()

if df.empty:
    st.warning("The dataset contains no records.")
    st.stop()

required_columns = [
    "Name",
    "Team Name",
    "Injury",
    "Date of Injury",
    "Date of return",
    "Injury Duration (Days)",
    "Average Rating Before Injury",
    "Average Rating After Injury",
    "Rating Change",
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
# PLAYER SELECTION
# --------------------------------------------------

players = sorted(
    df["Name"].dropna().astype(str).unique().tolist()
)

if not players:
    st.warning("No player names were found.")
    st.stop()

st.subheader("Select a player")

selected_player = st.selectbox(
    "Player",
    options=players,
    index=0,
    help="Choose one player to explore their injury records.",
)

player_data = df[
    df["Name"].astype(str) == selected_player
].copy()

player_data = player_data.sort_values(
    "Date of Injury",
    na_position="last",
)

if player_data.empty:
    st.warning("No records were found for this player.")
    st.stop()


# --------------------------------------------------
# SELECT AN INJURY RECORD
# --------------------------------------------------

def make_record_label(row):
    injury = (
        str(row["Injury"])
        if pd.notna(row["Injury"])
        else "Unknown injury"
    )

    date = (
        row["Date of Injury"].strftime("%d %b %Y")
        if pd.notna(row["Date of Injury"])
        else "Date unavailable"
    )

    club = (
        str(row["Team Name"])
        if pd.notna(row["Team Name"])
        else "Unknown club"
    )

    return f"{date} · {injury} · {club}"


player_data["_record_label"] = player_data.apply(
    make_record_label,
    axis=1,
)

# Add a record number so duplicate labels remain distinguishable.
player_data["_record_label"] = (
    player_data["_record_label"]
    + " · Record "
    + (player_data.groupby("_record_label").cumcount() + 1).astype(str)
)

selected_label = st.selectbox(
    "Injury record",
    options=player_data["_record_label"].tolist(),
    help="Choose which injury to examine in detail.",
)

record = player_data[
    player_data["_record_label"] == selected_label
].iloc[0]


# --------------------------------------------------
# PLAYER SUMMARY
# --------------------------------------------------

st.divider()
st.subheader(selected_player)

club = record["Team Name"]
position = record["Position"] if "Position" in df.columns else None
age = record["Age"] if "Age" in df.columns else None
fifa_rating = (
    record["FIFA rating"]
    if "FIFA rating" in df.columns
    else None
)

profile1, profile2, profile3, profile4 = st.columns(4)

profile1.metric(
    "Club",
    str(club) if pd.notna(club) else "Not recorded",
)

profile2.metric(
    "Position",
    str(position) if pd.notna(position) else "Not recorded",
)

profile3.metric(
    "Age",
    f"{age:.0f}" if pd.notna(age) else "Not recorded",
)

profile4.metric(
    "FIFA rating",
    f"{fifa_rating:.1f}"
    if pd.notna(fifa_rating)
    else "Not recorded",
)


# --------------------------------------------------
# INJURY DETAILS
# --------------------------------------------------

st.subheader("Injury details")

injury1, injury2, injury3 = st.columns(3)

injury1.metric(
    "Injury type",
    str(record["Injury"])
    if pd.notna(record["Injury"])
    else "Not recorded",
)

injury1.caption("Selected record")

injury2.metric(
    "Recovery duration",
    (
        f"{record['Injury Duration (Days)']:.0f} days"
        if pd.notna(record["Injury Duration (Days)"])
        else "Not available"
    ),
)

injury3.metric(
    "Date of return",
    (
        record["Date of return"].strftime("%d %b %Y")
        if pd.notna(record["Date of return"])
        else "Not recorded"
    ),
)


# --------------------------------------------------
# RATING COMPARISON
# --------------------------------------------------

st.divider()
st.subheader("Performance before and after injury")

before = record["Average Rating Before Injury"]
after = record["Average Rating After Injury"]
change = record["Rating Change"]

rating1, rating2, rating3 = st.columns(3)

rating1.metric(
    "Average rating before",
    f"{before:.2f}" if pd.notna(before) else "N/A",
)

rating2.metric(
    "Average rating after",
    f"{after:.2f}" if pd.notna(after) else "N/A",
)

rating3.metric(
    "Rating change",
    f"{change:+.2f}" if pd.notna(change) else "N/A",
    help="After-injury average rating minus before-injury average rating.",
)

rating_periods = [
    ("Before 1", "Match1_before_injury_Player_rating"),
    ("Before 2", "Match2_before_injury_Player_rating"),
    ("Before 3", "Match3_before_injury_Player_rating"),
    ("After 1", "Match1_after_injury_Player_rating"),
    ("After 2", "Match2_after_injury_Player_rating"),
    ("After 3", "Match3_after_injury_Player_rating"),
]

rating_rows = []

for period, column in rating_periods:
    if column in df.columns:
        value = pd.to_numeric(
            pd.Series([record[column]]),
            errors="coerce",
        ).iloc[0]

        if pd.notna(value):
            rating_rows.append({
                "Match Period": period,
                "Player Rating": float(value),
                "Stage": (
                    "Before injury"
                    if period.startswith("Before")
                    else "After injury"
                ),
            })

rating_timeline = pd.DataFrame(rating_rows)

if not rating_timeline.empty:
    fig_ratings = px.line(
        rating_timeline,
        x="Match Period",
        y="Player Rating",
        color="Stage",
        markers=True,
        template="plotly_dark",
        color_discrete_map={
            "Before injury": "#65E6B4",
            "After injury": "#E6B65C",
        },
        category_orders={
            "Match Period": [
                "Before 1",
                "Before 2",
                "Before 3",
                "After 1",
                "After 2",
                "After 3",
            ]
        },
        hover_data={"Stage": False},
    )

    fig_ratings.update_layout(
        height=390,
        xaxis_title="Match period",
        yaxis_title="Player rating",
        legend_title="",
        margin=dict(l=10, r=20, t=25, b=20),
    )

    st.plotly_chart(
        fig_ratings,
        use_container_width=True,
    )
else:
    st.info(
        "No individual match ratings are available for "
        "this injury record."
    )


# --------------------------------------------------
# ALL INJURIES FOR THIS PLAYER
# --------------------------------------------------

st.divider()
st.subheader("Complete injury history")

history_columns = [
    "Date of Injury",
    "Date of return",
    "Team Name",
    "Injury",
    "Injury Duration (Days)",
    "Average Rating Before Injury",
    "Average Rating After Injury",
    "Rating Change",
]

available_history_columns = [
    column for column in history_columns
    if column in player_data.columns
]

history = player_data[available_history_columns].copy()

history = history.rename(
    columns={
        "Date of Injury": "Injury Date",
        "Date of return": "Return Date",
        "Team Name": "Club",
        "Injury": "Injury Type",
        "Injury Duration (Days)": "Recovery Days",
    }
)

st.dataframe(
    history,
    use_container_width=True,
    hide_index=True,
)

st.caption(
    f"Showing all {len(player_data)} injury record(s) "
    f"associated with {selected_player}."
)
