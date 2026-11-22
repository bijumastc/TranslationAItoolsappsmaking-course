"""Calls to Gemini and Sarvam AI.

Keys are read from (1) a key the user typed into the sidebar for this session only,
or (2) Streamlit secrets (.streamlit/secrets.toml locally, the Secrets box on
Streamlit Community Cloud). Keys are never written to disk or shown on screen.
"""
import requests
import streamlit as st

GEMINI_MODELS = ["gemini-flash-latest", "gemini-3.5-flash", "gemini-3.5-flash-lite"]
SARVAM_URL = "https://api.sarvam.ai/translate"
SARVAM_MODES = ["formal", "modern-colloquial", "classic-colloquial", "code-mixed"]
LANG_CODES = {"English": "en-IN", "Malayalam": "ml-IN", "Hindi": "hi-IN", "Tamil": "ta-IN"}


def _secret(name: str) -> str:
    try:
        return st.secrets.get(name, "") or ""
    except Exception:  # no secrets file present
        return ""


def gemini_key() -> str:
    return st.session_state.get("user_gemini_key") or _secret("GEMINI_API_KEY")


def sarvam_key() -> str:
    return st.session_state.get("user_sarvam_key") or _secret("SARVAM_API_KEY")


def gemini_model() -> str:
    return st.session_state.get("gemini_model") or _secret("GEMINI_MODEL") or GEMINI_MODELS[0]


def key_sidebar(need_sarvam: bool = False) -> None:
    """Sidebar box for keys. A typed key lives only in this browser session."""
    with st.sidebar:
        st.subheader("🔑 API keys")
        if _secret("GEMINI_API_KEY"):
            st.success("Gemini key loaded from the app's secrets.")
        st.text_input(
            "Your own Gemini key (optional)",
            type="password",
            key="user_gemini_key",
            help="Get one free at aistudio.google.com → Get API key. Used only for this session.",
        )
        st.selectbox("Gemini model", GEMINI_MODELS, key="gemini_model",
                     help="'gemini-flash-latest' always points to Google's newest Flash model.")
        if need_sarvam:
            if _secret("SARVAM_API_KEY"):
                st.success("Sarvam key loaded from the app's secrets.")
            st.text_input("Your own Sarvam key (optional)", type="password", key="user_sarvam_key",
                          help="Sign up at dashboard.sarvam.ai. Free trial credits are included.")
        st.caption("Never paste a key into a chat, a screenshot or GitHub.")


def gemini_generate(contents, system: str = "", temperature: float = 0.4, json_mode: bool = False) -> str:
    """contents: a string, or a list of {"role": "user"|"model", "text": str} turns."""
    from google import genai
    from google.genai import types

    key = gemini_key()
    if not key:
        raise RuntimeError("No Gemini API key. Add one in the sidebar or in the app's secrets.")
    client = genai.Client(api_key=key)
    if isinstance(contents, list):
        contents = [
            types.Content(role=t["role"], parts=[types.Part.from_text(text=t["text"])]) for t in contents
        ]
    config = types.GenerateContentConfig(
        system_instruction=system or None,
        temperature=temperature,
        response_mime_type="application/json" if json_mode else None,
    )
    resp = client.models.generate_content(model=gemini_model(), contents=contents, config=config)
    return resp.text or ""


def sarvam_translate(text: str, source: str = "en-IN", target: str = "ml-IN", mode: str = "formal",
                     model: str = "mayura:v1") -> str:
    key = sarvam_key()
    if not key:
        raise RuntimeError("No Sarvam API key. Add one in the sidebar or in the app's secrets.")
    if len(text) > 1000 and model == "mayura:v1":
        raise RuntimeError("Mayura accepts up to 1,000 characters per request. Shorten the text.")
    resp = requests.post(
        SARVAM_URL,
        headers={"api-subscription-key": key, "Content-Type": "application/json"},
        json={"input": text, "source_language_code": source, "target_language_code": target,
              "mode": mode, "model": model},
        timeout=60,
    )
    if resp.status_code != 200:
        raise RuntimeError(f"Sarvam error {resp.status_code}: {resp.text[:300]}")
    return resp.json().get("translated_text", "")
