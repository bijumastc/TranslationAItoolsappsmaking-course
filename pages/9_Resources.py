import streamlit as st

from utils.content import load_text, page_header

page_header("Resources", "The Indian language AI stack, builder tools, the DH bridge and ethics rules.")
st.markdown(load_text("resources.md"))
