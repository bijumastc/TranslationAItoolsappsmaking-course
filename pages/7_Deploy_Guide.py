import streamlit as st

from utils.content import load_text, page_header

page_header("Deploy Guide", "How and where to publish your apps, one small step each week.")
st.markdown(load_text("deploy_guide.md"))
