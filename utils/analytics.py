
import pandas as pd


def get_injury_counts(data):
    """Count injury records by injury type."""
    return (
        data.groupby("Injury")["Name"]
        .count()
        .sort_values(ascending=False)
    )


def get_player_injury_counts(data):
    """Count injury records for every player."""
    return (
        data.groupby("Name")
        .size()
        .sort_values(ascending=False)
    )


def get_club_injury_counts(data):
    """Count injury records for every club."""
    return (
        data.groupby("Team Name")
        .size()
        .sort_values(ascending=False)
    )


def get_average_rating_change(data):
    """Calculate the average rating change for each player."""
    valid_data = data.dropna(subset=["Rating Change"])

    return (
        valid_data.groupby("Name")["Rating Change"]
        .mean()
        .sort_values(ascending=False)
    )


def get_top_performance_drops(data, n=10):
    """Find injury records associated with the largest performance drops."""
    valid_data = data.dropna(
        subset=["Team Performance Drop Index"]
    )

    return valid_data.nlargest(
        n, "Team Performance Drop Index"
    )


def get_monthly_injury_counts(data):
    """Count injury records by club and month."""
    valid_data = data.dropna(subset=["Date of Injury"]).copy()

    valid_data["Injury Month"] = (
        valid_data["Date of Injury"].dt.month
    )

    return pd.pivot_table(
        valid_data,
        index="Team Name",
        columns="Injury Month",
        values="Name",
        aggfunc="count",
        fill_value=0,
    )


def get_player_rating_timeline(record):
    """Return a selected injury record's ratings before and after injury."""
    periods = [
        ("Before 1", "Match1_before_injury_Player_rating"),
        ("Before 2", "Match2_before_injury_Player_rating"),
        ("Before 3", "Match3_before_injury_Player_rating"),
        ("After 1", "Match1_after_injury_Player_rating"),
        ("After 2", "Match2_after_injury_Player_rating"),
        ("After 3", "Match3_after_injury_Player_rating"),
    ]

    timeline = []

    for label, column in periods:
        if column in record.index:
            value = pd.to_numeric(
                record[column], errors="coerce"
            )

            if pd.notna(value):
                timeline.append({
                    "Match Period": label,
                    "Player Rating": float(value),
                })

    return pd.DataFrame(timeline)


def get_injury_duration_rating_correlation(data):
    """Calculate correlation between injury duration and rating change."""
    valid_data = data[
        ["Injury Duration (Days)", "Rating Change"]
    ].dropna()

    if len(valid_data) < 2:
        return None, len(valid_data)

    correlation = valid_data[
        "Injury Duration (Days)"
    ].corr(valid_data["Rating Change"])

    return correlation, len(valid_data)
