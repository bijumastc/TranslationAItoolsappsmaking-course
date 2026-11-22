import streamlit as st

from utils.content import LEVELS, page_header, phases, prompts, weeks

page_header("Weekly Lessons", "Theory, the 15-minute demo, and your task at three levels.")

all_weeks = weeks()
ph = phases()
bank = prompts()

with st.sidebar:
    n = st.select_slider("Week", options=[w["week"] for w in all_weeks], value=1)
    projector = st.toggle("Projector mode (large text)", help="For the teacher's 15-minute demo.")

w = next(x for x in all_weeks if x["week"] == n)
p = ph[w["phase"]]

if projector:
    st.markdown("<style>.stMarkdown p, .stMarkdown li {font-size: 1.45rem !important;}</style>",
                unsafe_allow_html=True)

st.header(f"Week {w['week']} · {w['title']}")
st.caption(f"Phase {p['id']}: {p['name']} · Portfolio app: {w['app']}")

st.subheader("📖 Theory")
st.write(w["theory"])

st.subheader("⏱️ 15-minute demo")
d = w["demo"]
c1, c2, c3, c4 = st.columns(4)
c1.markdown(f"**0–2 · Hook**\n\n{d['hook']}")
c2.markdown(f"**2–10 · Live build**\n\n{d['live_build']}")
c3.markdown(f"**10–13 · Break it**\n\n{d['break_it']}")
c4.markdown("**13–15 · Challenge**\n\nPick your level below and start.")

st.subheader("🎯 Your task this week")
tabs = st.tabs(list(LEVELS.values()))
for tab, key in zip(tabs, LEVELS):
    with tab:
        st.markdown(f"### {w['levels'][key]}")
        if key == "starter":
            st.caption("Support: template, worked example, the Twin. Evidence: screenshot + prompt + 3-line reflection.")
        elif key == "builder":
            st.caption("Support: brief template, the Twin. Evidence: app link + brief + test log of 5 hard cases.")
        else:
            st.caption("Support: problem statement only. Evidence: repo or deployed link + test log + short write-up.")

if w["prompts"]:
    st.subheader("🧾 Prompts for this week")
    for pid in w["prompts"]:
        pr = bank.get(pid)
        if pr:
            with st.expander(f"{pid} · {pr['title']}  ({'AI Studio chat' if pr['where'] == 'chat' else 'AI Studio Build mode'})"):
                st.caption(f"Concept: {pr['concept']}")
                st.code(pr["text"], language=None)

a, b, c = st.columns(3)
a.markdown(f"**🚀 Deploy skill**\n\n{w['deploy']}")
b.markdown(f"**🤖 Ask the Twin**\n\n{w['twin_tip']}")
c.markdown(f"**🏛️ Digital Humanities link**\n\n{w['dh_link']}")

st.divider()
nav_l, nav_r = st.columns(2)
if n > 1:
    nav_l.caption(f"← Week {n - 1}: {all_weeks[n - 2]['title']}")
if n < len(all_weeks):
    nav_r.caption(f"Week {n + 1}: {all_weeks[n]['title']} →")
