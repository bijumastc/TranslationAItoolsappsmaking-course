import streamlit as st

from utils.content import page_header, phases, weeks

page_header(
    "Translation in Praxis",
    "English ↔ Malayalam translation with AI tools · Skill Enhancement Course · University of Calicut",
)

st.markdown(
    """
Welcome. In this course you **translate, build and ship**. You start by writing good translation
prompts, turn them into apps with Google AI Studio, connect India-built engines (Bhashini, Sarvam AI,
AI4Bharat), learn to catch AI translation slop, and finish with a deployed capstone tool for a real user.

> **Promptotyping** = write a brief → let AI build it → test it on real Malayalam → find the failure →
> explain it with translation theory → improve the brief.
"""
)

st.subheader("The ladder you climb")
cols = st.columns(len(phases()))
for col, (pid, p) in zip(cols, phases().items()):
    with col:
        st.markdown(f"**{pid} · {p['name']}**")
        st.caption(f"Weeks {p['weeks']}")
        st.write(p["summary"])
        if p.get("gate"):
            st.markdown(f"🏁 *{p['gate']}*")

st.divider()
left, right = st.columns(2)
with left:
    st.subheader("👩‍🎓 Students: start here")
    st.markdown(
        """
1. Open **Weekly Lessons** and pick this week.
2. Choose your level: 🌱 Starter, 🛠️ Builder or 🚀 Pro. You can move up any week.
3. Copy the prompts from the **Prompt Bank**.
4. Stuck? Ask the **Professor Twin** before you ask the teacher.
5. Check your translations with the **Slop Detector**.
6. Learn to publish in the **Deploy Guide**.
"""
    )
with right:
    st.subheader("👨‍🏫 Teachers: daily 15-minute demo")
    st.markdown(
        """
| Min | Beat | |
|---|---|---|
| 0–2 | Hook | Show one real mistranslation |
| 2–10 | Live build | Type the day's prompt, think aloud |
| 10–13 | Break it | Feed it a hard case |
| 13–15 | Challenge | Put up the three-level task |

Turn on **Projector mode** in Weekly Lessons for large text.
All content lives in the `content/` folder: edit the YAML and Markdown files to change the course.
"""
    )

st.divider()
st.page_link("pages/2_Weekly_Lessons.py", label="Go to this week's lesson →", icon="📅")
st.caption(f"{len(weeks())} weeks · 12 portfolio apps · 1 capstone. AI output in this app is machine-generated; "
           "a human translator always has the final say.")
