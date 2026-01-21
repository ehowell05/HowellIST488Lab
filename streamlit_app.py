import streamlit as st

st.set_page_config(
    page_title="Eddie Howell IST488 Labs",
    page_icon="🥼",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.page(
    'labs/lab1',
    title = "Lab 1",
    icon = "📄",
    url_path = None,
    default = False
)

st.page(
    'labs/lab2',
    title = "Lab 2",
    icon = "🥼",
    url_path = None,
    default = False
)