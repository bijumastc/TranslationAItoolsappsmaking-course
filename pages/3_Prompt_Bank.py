import streamlit as st

from utils.content import page_header, prompts
from utils.llm import gemini_generate, key_sidebar

page_header("Prompt Bank", "Copy a prompt, or try it right here in the Prompt Lab.")
key_sidebar()

bank = prompts()
where = st.radio("Show prompts for", ["All", "AI Studio chat", "AI Studio Build mode"], horizontal=True)
wanted = {"All": None, "AI Studio chat": "chat", "AI Studio Build mode": "build"}[where]

for pid, pr in bank.items():
    if wanted and pr["where"] != wanted:
        continue
    with st.expander(f"**{pid}** · {pr['title']}"):
        st.caption(f"Concept: {pr['concept']} · Use in: {'chat' if pr['where'] == 'chat' else 'Build mode'}")
        st.code(pr["text"], language=None)

st.divider()
st.subheader("🧪 Prompt Lab")
st.caption("Edit a chat prompt, fill in the brackets, and run it. Build-mode briefs belong in AI Studio's Build mode.")
chat_ids = [k for k, v in bank.items() if v["where"] == "chat"]
choice = st.selectbox("Start from", chat_ids, format_func=lambda k: f"{k} · {bank[k]['title']}")
text = st.text_area("Your prompt", value=bank[choice]["text"], height=240, key=f"lab_{choice}")
temp = st.slider("Temperature (creativity)", 0.0, 1.5, 0.4, 0.1,
                 help="Low = consistent and literal. High = varied. Try both and compare.")
if st.button("Run with Gemini", type="primary"):
    if "[PASTE" in text:
        st.warning("Replace the [PASTE] placeholder with your text first.")
    else:
        with st.spinner("Translating…"):
            try:
                st.markdown(gemini_generate(text, temperature=temp))
            except Exception as e:
                st.error(str(e))
st.caption("Save prompts that work to your prompt journal with a one-line theory note.")
