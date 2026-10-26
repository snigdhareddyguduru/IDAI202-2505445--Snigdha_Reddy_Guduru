
import streamlit as st


def apply_dashboard_styles():
    """Apply a polished, modern football analytics theme."""

    st.markdown(
        """
        <style>
        @import url(
            'https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap'
        );

        .stApp {
            background-color: #0B1220;
            color: #E8EEF8;
            font-family: 'DM Sans', sans-serif;
        }

        [data-testid="stSidebar"] {
            background-color: #111C2E;
            border-right: 1px solid #24334A;
        }

        [data-testid="stSidebar"] * {
            color: #E8EEF8;
        }

        h1, h2, h3 {
            font-family: 'Manrope', sans-serif !important;
            color: #F4F7FC !important;
            font-weight: 800 !important;
        }

        p, label, .stMarkdown {
            color: #C5D0E0;
        }

        [data-testid="stMetric"] {
            background: linear-gradient(
                145deg, #17263B, #111C2E
            );
            border: 1px solid #2B3D56;
            border-radius: 14px;
            padding: 18px 20px;
        }

        [data-testid="stMetricLabel"] {
            color: #A9BAD0 !important;
        }

        [data-testid="stMetricValue"] {
            color: #65E6B4 !important;
            font-family: 'Manrope', sans-serif;
            font-weight: 800;
        }

        div[data-baseweb="select"] > div {
            background-color: #17263B;
            border-color: #344862;
            border-radius: 9px;
        }

        div[data-testid="stDataFrame"] {
            border: 1px solid #2B3D56;
            border-radius: 12px;
            overflow: hidden;
        }

        .section-caption {
            color: #8FA5C0;
            font-size: 0.92rem;
            margin-top: -8px;
            margin-bottom: 18px;
        }

        .dashboard-card {
            background: #142238;
            border: 1px solid #2B3D56;
            border-radius: 14px;
            padding: 20px;
            margin-bottom: 16px;
        }

        .accent-text {
            color: #65E6B4;
            font-weight: 700;
        }

        button[kind="primary"] {
            background-color: #65E6B4;
            color: #0B1220;
            border: none;
            border-radius: 9px;
            font-weight: 700;
        }

        button[kind="primary"]:hover {
            background-color: #8AF0C8;
            color: #0B1220;
        }

        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
