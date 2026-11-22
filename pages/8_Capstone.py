import streamlit as st

from utils.content import load_text, page_header

page_header("Capstone", "Weeks 13–15 · a deployed tool for a real user.")
st.markdown(load_text("capstone.md"))
