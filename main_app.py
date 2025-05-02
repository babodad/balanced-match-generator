
import streamlit as st

st.title("Magic Turnier Tools")

tool = st.radio(
    "Wähle ein Tool:",
    ["Balanced Match Generator (klassisch)", "Tournament Tool Advanced"]
)

if tool == "Balanced Match Generator (klassisch)":
    import balanced_match_app
elif tool == "Tournament Tool Advanced":
    import tournament_tool_advanced
