  
import pandas as pd
import streamlit as st

from utils.data_loader import load_data


# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

st.title("Data Lab")

st.markdown(
    """
    Search, filter, sort, and inspect the football injury dataset.
    Explore the records behind the dashboard's analysis.
    """
)

st.caption("PITCHSIDE  /  DATA EXPLORATION")


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

# Preserve the complete dataset and its original row order.
data = df.copy()

st.subheader("Dataset overview")

metric1, metric2, metric3 = st.columns(3)

metric1.metric("Total records", f"{len(data):,}")
metric2.metric("Total columns", f"{len(data.columns):,}")

missing_cells = int(data.isna().sum().sum())

metric3.metric("Missing cells", f"{missing_cells:,}")

st.divider()


# --------------------------------------------------
# SEARCH
# --------------------------------------------------

st.subheader("Find records")

search_term = st.text_input(
    "Search across player, club, and injury information",
    placeholder="For example: Arsenal, hamstring, or a player's name",
)

filtered = data.copy()

if search_term.strip():
    searchable_columns = [
        column
        for column in ["Name", "Team Name", "Injury", "Position"]
        if column in filtered.columns
    ]

    if searchable_columns:
        search_mask = pd.Series(
            False,
            index=filtered.index,
        )

        for column in searchable_columns:
            search_mask |= (
                filtered[column]
                .astype("string")
                .str.contains(
                    search_term.strip(),
                    case=False,
                    na=False,
                    regex=False,
                )
            )

        filtered = filtered[search_mask]


# --------------------------------------------------
# FILTERS
# --------------------------------------------------

st.subheader("Refine the dataset")

filter_col1, filter_col2 = st.columns(2)

with filter_col1:
    if "Team Name" in filtered.columns:
        available_clubs = sorted(
            filtered["Team Name"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_clubs = st.multiselect(
            "Filter by club",
            options=available_clubs,
            default=[],
            help=(
                "Leave empty to include every club "
                "matching your search."
            ),
        )

        if selected_clubs:
            filtered = filtered[
                filtered["Team Name"].astype(str).isin(
                    selected_clubs
                )
            ]

with filter_col2:
    if "Injury" in filtered.columns:
        available_injuries = sorted(
            filtered["Injury"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_injuries = st.multiselect(
            "Filter by injury type",
            options=available_injuries,
            default=[],
            help=(
                "Leave empty to include every injury type "
                "matching the other filters."
            ),
        )

        if selected_injuries:
            filtered = filtered[
                filtered["Injury"].astype(str).isin(
                    selected_injuries
                )
            ]


# --------------------------------------------------
# NUMERIC FILTER
# --------------------------------------------------

numeric_filter_columns = [
    column
    for column in [
        "Age",
        "FIFA rating",
        "Injury Duration (Days)",
        "Rating Change",
        "Team Performance Drop Index",
    ]
    if column in filtered.columns
    and pd.to_numeric(
        filtered[column],
        errors="coerce",
    ).notna().any()
]

if numeric_filter_columns:
    numeric_column = st.selectbox(
        "Optional numeric filter",
        options=["None"] + numeric_filter_columns,
    )

    if numeric_column != "None":
        numeric_values = pd.to_numeric(
            filtered[numeric_column],
            errors="coerce",
        )

        valid_values = numeric_values.dropna()

        if not valid_values.empty:
            minimum = float(valid_values.min())
            maximum = float(valid_values.max())

            if minimum < maximum:
                selected_range = st.slider(
                    f"Range for {numeric_column}",
                    min_value=minimum,
                    max_value=maximum,
                    value=(minimum, maximum),
                )

                filtered = filtered[
                    numeric_values.between(
                        selected_range[0],
                        selected_range[1],
                    )
                ]
            else:
                st.caption(
                    f"All valid values of {numeric_column} "
                    f"equal {minimum:g}."
                )


# --------------------------------------------------
# SORTING
# --------------------------------------------------

st.divider()
st.subheader("Explore matching records")

sort_col1, sort_col2 = st.columns(2)

with sort_col1:
    sort_column = st.selectbox(
        "Sort records by",
        options=data.columns.tolist(),
        index=(
            data.columns.get_loc("Date of Injury")
            if "Date of Injury" in data.columns
            else 0
        ),
    )

with sort_col2:
    sort_order = st.radio(
        "Sort direction",
        options=["Descending", "Ascending"],
        horizontal=True,
    )

if sort_column in filtered.columns:
    filtered = filtered.sort_values(
        by=sort_column,
        ascending=(sort_order == "Ascending"),
        na_position="last",
    )


# --------------------------------------------------
# RESULT COUNTS
# --------------------------------------------------

result1, result2, result3 = st.columns(3)

result1.metric(
    "Matching records",
    f"{len(filtered):,}",
)

result2.metric(
    "Unique players",
    f"{filtered['Name'].nunique():,}"
    if "Name" in filtered.columns
    else "N/A",
)

result3.metric(
    "Clubs represented",
    f"{filtered['Team Name'].nunique():,}"
    if "Team Name" in filtered.columns
    else "N/A",
)


# --------------------------------------------------
# DISPLAY FULL MATCHING TABLE
# --------------------------------------------------

st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True,
    height=560,
)

st.caption(
    f"Displaying all {len(filtered):,} matching records "
    f"across {len(filtered.columns):,} columns."
)


# --------------------------------------------------
# MISSING-VALUE ANALYSIS
# --------------------------------------------------

st.divider()
st.subheader("Data quality explorer")

st.markdown(
    "Inspect missing values by column in the complete dataset."
)

missing_summary = pd.DataFrame({
    "Column": data.columns,
    "Missing Values": [
        int(data[column].isna().sum())
        for column in data.columns
    ],
})

missing_summary["Missing Percentage"] = (
    missing_summary["Missing Values"]
    / len(data)
    * 100
).round(2)

missing_summary = missing_summary.sort_values(
    "Missing Values",
    ascending=False,
)

missing_summary = missing_summary[
    missing_summary["Missing Values"] > 0
]

if not missing_summary.empty:
    st.dataframe(
        missing_summary,
        use_container_width=True,
        hide_index=True,
    )
else:
    st.success("No missing values were detected.")

st.caption(
    "Missing values are reported rather than automatically "
    "replaced with zero, because an unavailable measurement "
    "is not necessarily a zero measurement."
)
