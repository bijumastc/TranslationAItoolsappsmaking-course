import pandas as pd
import streamlit as st

from utils.content import page_header
from utils.llm import LANG_CODES, SARVAM_MODES, gemini_generate, key_sidebar, sarvam_translate

page_header("Engine Comparator", "Engine choice is a translation decision. Same text, two engines, your vote.")
key_sidebar(need_sarvam=True)

c1, c2 = st.columns(2)
src_lang = c1.selectbox("From", list(LANG_CODES), index=0)
tgt_lang = c2.selectbox("To", list(LANG_CODES), index=1)
text = st.text_area("Text (max 1,000 characters for Sarvam Mayura)", max_chars=1000, height=140)

g, s = st.columns(2)
register = g.selectbox("Gemini register", ["formal", "everyday spoken", "literary", "code-mixed (Manglish)"])
mode = s.selectbox("Sarvam mode", SARVAM_MODES)

if st.button("Translate with both", type="primary") and text.strip():
    prompt = (f"Translate from {src_lang} to {tgt_lang}. Register: {register}. "
              f"Return only the translation.\n\nText:\n{text}")
    out = {}
    with st.spinner("Asking Gemini…"):
        try:
            out["Gemini"] = gemini_generate(prompt, temperature=0.2).strip()
        except Exception as e:
            out["Gemini"] = f"⚠️ {e}"
    with st.spinner("Asking Sarvam…"):
        try:
            out["Sarvam"] = sarvam_translate(text, LANG_CODES[src_lang], LANG_CODES[tgt_lang], mode)
        except Exception as e:
            out["Sarvam"] = f"⚠️ {e}"
    st.session_state.last = {"source": text, "register": register, "mode": mode, **out}

if "last" in st.session_state:
    last = st.session_state.last
    a, b = st.columns(2)
    with a.container(border=True):
        st.markdown(f"**Gemini** · {last['register']}")
        st.write(last["Gemini"])
    with b.container(border=True):
        st.markdown(f"**Sarvam Mayura** · {last['mode']}")
        st.write(last["Sarvam"])

    st.subheader("Your vote")
    v1, v2 = st.columns(2)
    winner = v1.radio("Better translation", ["Gemini", "Sarvam", "Tie"], horizontal=True)
    errors = v2.multiselect("Errors you saw in the losing one", ["meaning", "grammar", "word choice", "style", "register", "name/number"])
    note = st.text_input("One-line reason (link it to theory)")
    if st.button("Save vote"):
        st.session_state.setdefault("votes", []).append(
            {**last, "winner": winner, "errors": ", ".join(errors), "reason": note})
        st.success("Saved for this session.")

if st.session_state.get("votes"):
    df = pd.DataFrame(st.session_state.votes)
    st.dataframe(df, hide_index=True, width="stretch")
    st.download_button("Download votes (CSV)", df.to_csv(index=False).encode("utf-8"), "engine_votes.csv", "text/csv")
    st.caption("Votes live only in this browser session. Download before you close the tab.")
