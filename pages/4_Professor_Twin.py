import streamlit as st

from utils.content import LEVELS, load_text, page_header, weeks
from utils.llm import gemini_generate, key_sidebar

page_header("Professor Twin", "Your self-help tutor. It gives hints, not answers, and links every fix to theory.")
key_sidebar()

SYSTEM = load_text("twin_prompt.md")

with st.sidebar:
    st.subheader("About you")
    level = st.radio("Your level this week", list(LEVELS.values()), index=0)
    wk = st.selectbox("Week", [f"Week {w['week']}: {w['title']}" for w in weeks()])
    if st.button("Start a new conversation"):
        st.session_state.twin_history = []

if "twin_history" not in st.session_state:
    st.session_state.twin_history = []

if not st.session_state.twin_history:
    st.info("Try: *“My prompt gives a very formal Malayalam translation for a WhatsApp message. What should I change?”*\n\n"
            "You may write in English or Malayalam.")

for turn in st.session_state.twin_history:
    with st.chat_message("user" if turn["role"] == "user" else "assistant", avatar=None if turn["role"] == "user" else "🎓"):
        st.markdown(turn["text"])

question = st.chat_input("Ask the Twin…")
if question:
    st.session_state.twin_history.append({"role": "user", "text": question})
    with st.chat_message("user"):
        st.markdown(question)
    context = f"Student context: level = {level.split(' ', 1)[1]}; {wk}."
    with st.chat_message("assistant", avatar="🎓"):
        with st.spinner("Thinking…"):
            try:
                answer = gemini_generate(st.session_state.twin_history, system=SYSTEM + "\n\n" + context, temperature=0.5)
            except Exception as e:
                answer = f"⚠️ {e}"
        st.markdown(answer)
    st.session_state.twin_history.append({"role": "model", "text": answer})

if st.session_state.twin_history:
    log = "\n\n".join(f"{'STUDENT' if t['role'] == 'user' else 'TWIN'}: {t['text']}" for t in st.session_state.twin_history)
    st.download_button("Download this conversation for your weekly log", log.encode("utf-8"),
                       "twin_conversation.txt", "text/plain")
st.caption("The Twin can be wrong, especially about Malayalam usage. Check with a dictionary, a classmate or your teacher.")
