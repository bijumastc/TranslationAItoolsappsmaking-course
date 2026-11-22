# Translation in Praxis 🔤

An interactive course app for **English ↔ Malayalam translation with AI tools**, built for a
Skill Enhancement Course (SEC) at a college under the University of Calicut.

Students climb from prompting in a chat window → building apps with Google AI Studio →
India-built language engines (Bhashini, Sarvam AI, AIKosh, AI4Bharat IndicTrans2) →
evaluation and AI-slop detection → a deployed capstone.

## What's inside

| Page | What it does | Needs a key? |
| --- | --- | --- |
| Home | Course overview, the ladder, how students and teachers use the app | No |
| Roadmap | Six phases, gates, all 15 weeks; CSV download | No |
| Weekly Lessons | Theory, the 15-minute demo plan, Starter/Builder/Pro tasks, prompts, deploy skill; projector mode | No |
| Prompt Bank | Every course prompt to copy, plus a Prompt Lab to run chat prompts | Gemini (for the lab) |
| Professor Twin | A self-help AI tutor that gives hints, not answers | Gemini |
| Slop Detector | Rule checks (no key) + AI review with back-translation and MQM | Gemini (for the AI review) |
| Engine Comparator | Gemini vs Sarvam on the same text; vote and export CSV | Gemini + Sarvam |
| Deploy Guide | Where and how to publish apps, step by step | No |
| Capstone | Brief, roles, deliverables, Kerala-rooted ideas, marking | No |
| Resources | Indic AI stack, alternative tools, DH bridge, ethics | No |

## Edit the course without touching code

All course text lives in `content/`:

- `weeks.yaml` — phases and the 15 weeks (theory, demo, tasks at three levels, deploy skill, Twin tip, DH link)
- `prompts.yaml` — the prompt bank
- `twin_prompt.md` — the Professor Twin's instructions (make it sound like you)
- `deploy_guide.md`, `capstone.md`, `resources.md` — the reference pages

Edit a file on GitHub, commit, and the deployed app updates itself.

## Run it on your laptop

```bash
git clone https://github.com/<your-username>/translation-in-praxis.git
cd translation-in-praxis
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml   # then paste your keys
streamlit run Home.py
```

Without keys, every page opens. The AI features ask for a key in the sidebar.

## Put it on GitHub

1. Create a new repository on github.com called `translation-in-praxis` (no README, since this folder has one).
2. In this folder:
   ```bash
   git init
   git add .
   git commit -m "Translation in Praxis course app"
   git branch -M main
   git remote add origin https://github.com/<your-username>/translation-in-praxis.git
   git push -u origin main
   ```
   Or use GitHub Desktop, or drag the files into the repository page with **Add file → Upload files**.
3. Check that `.streamlit/secrets.toml` is **not** in the repository. The `.gitignore` keeps it out.

## Deploy on Streamlit Community Cloud (free)

1. Go to **share.streamlit.io** and sign in with GitHub.
2. Click **Create app → Deploy a public app from GitHub**.
3. Repository: `<your-username>/translation-in-praxis`, branch `main`, main file `Home.py`.
4. Open **Advanced settings → Secrets** and paste:
   ```toml
   GEMINI_API_KEY = "your-gemini-key"
   SARVAM_API_KEY = "your-sarvam-key"
   GEMINI_MODEL = "gemini-flash-latest"
   ```
5. Click **Deploy**. Share the URL with your class. Every `git push` redeploys.

### Keys and cost

- Get a Gemini key at **aistudio.google.com → Get API key**. Get a Sarvam key at **dashboard.sarvam.ai** (free trial credits).
- A key in the app's Secrets is used by **every visitor**. For a whole class, either keep the app link within the class
  or leave Secrets empty and ask each student to paste their own key in the sidebar (it lasts only for their session).
- Never put a key in code, a slide, a screenshot or a chat. If one leaks, delete it and create a new one.

## Teaching notes

- Each class opens with a 15-minute demo: hook (0–2), live build (2–10), break it (10–13), challenge card (13–15).
- Students pick a level each week: 🌱 Starter, 🛠️ Builder, 🚀 Pro. Support fades from *I do* to *you do alone*.
- AI output is machine-generated. A human translator always has the final say, especially for health, legal and
  government texts.

## Licence

Code: MIT. Course content in `content/`: CC BY 4.0 — reuse and adapt with credit. Change these if your
institution prefers otherwise.
