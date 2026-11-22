import json

import pandas as pd
import streamlit as st

from utils.content import page_header
from utils.llm import gemini_generate, key_sidebar
from utils.slop import REVIEW_SYSTEM, run_checks, sentences

page_header("Translation Slop Detector",
            "Find the marks of careless machine translation, with evidence. A support tool, not a judge.")
key_sidebar()

with st.expander("What is translation slop?"):
    st.markdown(
        """
**Translation slop** = fluent-looking output a careful human translator would not sign:
meaning drift, invented content, dropped content, flattened culture, wrong register, or English thinking in Malayalam words.

AI-authorship detectors guess *who* wrote a text and are weak on short texts and on Malayalam.
This tool asks a better question: **is this translation faithful and fit for its reader?**
Rule checks run without any key. The AI review needs a Gemini key.
"""
    )

SAMPLE_SRC = ("The college will remain closed on 15 August 2026 for Independence Day. "
              "Classes will not be held. Students must submit their assignments by 20 August.")
SAMPLE_TGT = ("സ്വാതന്ത്ര്യദിനം പ്രമാണിച്ച് 2026 ഓഗസ്റ്റ് 15-ന് കോളേജ് അടച്ചിരിക്കും. "
              "ക്ലാസുകൾ നടക്കും.")

if st.button("Load a sample with planted errors"):
    st.session_state.src = SAMPLE_SRC
    st.session_state.tgt = SAMPLE_TGT

l, r = st.columns(2)
src = l.text_area("Source text", height=200, key="src")
tgt = r.text_area("Translation", height=200, key="tgt")

if st.button("Check", type="primary") and src.strip() and tgt.strip():
    st.subheader("1 · Rule checks (no AI)")
    st.dataframe(pd.DataFrame(run_checks(src, tgt)), hide_index=True, width="stretch")

    st.subheader("2 · Side by side")
    s, t = sentences(src), sentences(tgt)
    rows = max(len(s), len(t))
    st.dataframe(pd.DataFrame({"#": range(1, rows + 1),
                               "Source": s + [""] * (rows - len(s)),
                               "Translation": t + [""] * (rows - len(t))}),
                 hide_index=True, width="stretch")
    st.session_state.ready_for_ai = True

if st.session_state.get("ready_for_ai"):
    st.subheader("3 · AI review with back-translation (MQM)")
    if st.button("Run AI review"):
        with st.spinner("Back-translating and reviewing…"):
            try:
                raw = gemini_generate(f"SOURCE:\n{src}\n\nTARGET:\n{tgt}", system=REVIEW_SYSTEM,
                                      temperature=0.1, json_mode=True)
                data = json.loads(raw)
                verdict = data.get("verdict", "?")
                icon = {"publish": "🟢", "revise": "🟠", "retranslate": "🔴"}.get(verdict, "⚪")
                st.markdown(f"### {icon} Suggested verdict: **{verdict}**")
                st.write(data.get("reason", ""))
                st.markdown("**Back-translation**")
                st.info(data.get("back_translation", ""))
                issues = pd.DataFrame(data.get("issues", []))
                if issues.empty:
                    st.success("No issues listed. Read it yourself anyway.")
                else:
                    st.dataframe(issues, hide_index=True, width="stretch")
                    st.download_button("Download report (CSV)", issues.to_csv(index=False).encode("utf-8"),
                                       "slop_report.csv", "text/csv")
            except json.JSONDecodeError:
                st.warning("The model did not return clean JSON. Showing raw output:")
                st.code(raw)
            except Exception as e:
                st.error(str(e))
    st.caption("🧑‍⚖️ Human gate: accept or reject each flag and write one line on why. That reflection is what gets graded.")
