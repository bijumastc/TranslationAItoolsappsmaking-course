import pandas as pd
import streamlit as st

from utils.content import page_header, phases, weeks

page_header("Roadmap", "Six phases from prompting in a chat window to a deployed capstone.")

ph = phases()
for pid, p in ph.items():
    with st.container(border=True):
        a, b, c = st.columns([2, 5, 2])
        a.markdown(f"### {pid} · {p['name']}")
        a.caption(f"Weeks {p['weeks']}")
        b.write(p["summary"])
        phase_weeks = [w for w in weeks() if w["phase"] == pid]
        b.caption(" · ".join(f"W{w['week']}: {w['app']}" for w in phase_weeks))
        if p.get("gate"):
            c.markdown(f"🏁 **{p['gate']}**")

st.info("Support fades over the semester: **I do** (Weeks 1–4) → **we do** (5–7) → "
        "**you do with the Twin** (8–12) → **you do alone** (13–15).")

st.subheader("All weeks at a glance")
df = pd.DataFrame(
    [
        {
            "Week": w["week"],
            "Phase": ph[w["phase"]]["name"],
            "Title": w["title"],
            "Portfolio app": w["app"],
            "Deploy skill": w["deploy"],
        }
        for w in weeks()
    ]
)
st.dataframe(df, hide_index=True, width="stretch")
st.download_button("Download roadmap as CSV", df.to_csv(index=False).encode("utf-8"),
                   "translation_in_praxis_roadmap.csv", "text/csv")
