## The one rule

An API key must live on a server or in a secrets setting, **never in code a browser can see**, never in a screenshot, and never in GitHub.

## Where to deploy

| Host | Best for | Level | Watch out for |
| --- | --- | --- | --- |
| AI Studio share link | Showing an app to the class quickly | Starter | Check how shared apps use quota; fine for demos |
| Google Cloud Run (from AI Studio) | Public AI Studio apps with server-side keys | Builder | May ask for a billing account; set a budget alert |
| GitHub (sync from AI Studio) | Versions, teamwork, portfolio record | Builder | Never commit `.env` or `secrets.toml` |
| Streamlit Community Cloud | Python apps like this course app | Builder–Pro | Keys go in the app's Secrets box |
| Hugging Face Spaces | Gradio/Streamlit apps, open models like IndicTrans2 | Pro | Free CPU is slow for big models |
| GitHub Pages / Netlify / Vercel | Static pages: portfolio site, front ends | Builder–Pro | A static page cannot hide a key |
| Google Sites | Department portfolio page | Starter | Link to apps, don't rebuild them |

## Deploying an AI Studio app

1. **Test before you ship.** Run five hard cases: Manglish, a proverb, a kinship term, a long sentence, empty input.
2. **Move keys to secrets.** Ask the Build agent: *"Make sure all API calls run on the server and read keys from secrets."*
3. **Add the honesty layer.** An About box: who built it, which engine, output is machine-generated, no user text stored.
4. **Sync to GitHub.** Connect a new repository; ask the agent to write a README.
5. **Deploy** to Cloud Run. Copy the public URL.
6. **Smoke test on a phone** using mobile data and a Malayalam keyboard.
7. **Record it** in the portfolio sheet: URL, repo, screenshot.

## Deploying a Streamlit app (like this one)

1. Push the repository to GitHub (public or private).
2. Go to share.streamlit.io, sign in with GitHub, choose **Create app**.
3. Pick the repository, branch `main`, and main file `Home.py`.
4. Open **Advanced settings → Secrets** and paste your keys in TOML form, e.g. `GEMINI_API_KEY = "..."`.
5. Click **Deploy**. Every `git push` redeploys automatically.

## Deploying a Hugging Face Space (Pro)

1. Create a new Space and pick Gradio (or Streamlit).
2. Ask an AI assistant for `app.py` and `requirements.txt` that translate English to Malayalam with a distilled IndicTrans2 model.
3. Upload both files; put keys under **Settings → Secrets**.
4. When the build fails, read the log, paste the error to the Professor Twin, fix and retry.

## Teaching sequence

| Week | Skill | Proof of learning |
| --- | --- | --- |
| 1–3 | Share a link | A classmate uses it |
| 4 | Deploy to Cloud Run | Public URL works on a phone |
| 5–6 | GitHub sync, commit, roll back | Repo with 5+ commits |
| 8–9 | Secrets and environment variables | Key not visible anywhere |
| 10 | Hugging Face Space | Running Space with an Indic model |
| 13–15 | Launch | Capstone live with real users |
