
from pathlib import Path

import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "football_injury_cleaned.csv"


@st.cache_data
def load_data():
    """Load the complete cleaned football injury dataset."""

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}"
        )

    data = pd.read_csv(DATA_PATH)
    data.columns = data.columns.str.strip()

    # Convert date fields
    for column in ["Date of Injury", "Date of return"]:
        if column in data.columns:
            data[column] = pd.to_datetime(
                data[column], errors="coerce"
            )

    # Convert analysis fields to numeric values
    numeric_columns = [
        "Age",
        "FIFA rating",
        "Injury Duration (Days)",
        "Average Rating Before Injury",
        "Average Rating After Injury",
        "Rating Change",
        "Average GD Before Injury",
        "Average GD During Absence",
        "Team Performance Drop Index",
    ]

    for column in numeric_columns:
        if column in data.columns:
            data[column] = pd.to_numeric(
                data[column], errors="coerce"
            )

    # Add a consistent injury category for grouping
    if "Injury" in data.columns:
        data["Injury Type Clean"] = (
            data["Injury"]
            .astype("string")
            .str.strip()
            .str.lower()
        )

    return data


def get_dataset_summary(data):
    """Return the main dataset statistics."""

    return {
        "records": len(data),
        "players": data["Name"].nunique(),
        "clubs": data["Team Name"].nunique(),
        "injury_types": data["Injury"].nunique(),
    }
