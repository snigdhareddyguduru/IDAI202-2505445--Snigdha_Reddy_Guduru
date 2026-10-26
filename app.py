
import streamlit as st

from utils.styles import apply_dashboard_styles


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Pitchside | Football Analytics",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# APPLY THE DASHBOARD THEME
# --------------------------------------------------

apply_dashboard_styles()


# --------------------------------------------------
# MULTIPAGE NAVIGATION
# --------------------------------------------------

overview_page = st.Page(
    "pages/01_Overview.py",
    title="Overview",
    icon=":material/dashboard:",
    default=True,
)

player_page = st.Page(
    "pages/02_Player_Explorer.py",
    title="Player Explorer",
    icon=":material/person_search:",
)

injury_page = st.Page(
    "pages/03_Injury_Analysis.py",
    title="Injury Analysis",
    icon=":material/healing:",
)

team_page = st.Page(
    "pages/04_Team_Performance.py",
    title="Team Performance",
    icon=":material/query_stats:",
)

data_page = st.Page(
    "pages/05_Data_Lab.py",
    title="Data Lab",
    icon=":material/table_view:",
)


# --------------------------------------------------
# SIDEBAR BRANDING
# --------------------------------------------------

with st.sidebar:
    st.markdown(
        """
        <div style="padding: 8px 0 22px 0;">
            <div style="
                font-size: 27px;
                font-weight: 800;
                letter-spacing: -1px;
                color: #65E6B4;
            ">
                ⚽ PITCHSIDE
            </div>
            <div style="
                font-size: 10px;
                letter-spacing: 2px;
                color: #8FA5C0;
                margin-top: 5px;
            ">
                FOOTBALL INTELLIGENCE
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.caption("PLAYER INJURIES  /  TEAM PERFORMANCE")


# --------------------------------------------------
# RUN THE SELECTED PAGE
# --------------------------------------------------

navigation = st.navigation(
    [
        overview_page,
        player_page,
        injury_page,
        team_page,
        data_page,
    ],
    position="sidebar",
)

navigation.run()
