"""Load course content from the content/ folder.

Teachers edit the YAML and Markdown files; the pages only display them.
"""
from pathlib import Path

import streamlit as st
import yaml

CONTENT_DIR = Path(__file__).resolve().parent.parent / "content"
LEVELS = {"starter": "🌱 Starter", "builder": "🛠️ Builder", "pro": "🚀 Pro"}


@st.cache_data
def load_yaml(name: str) -> dict:
    with open(CONTENT_DIR / name, encoding="utf-8") as f:
        return yaml.safe_load(f)


@st.cache_data
def load_text(name: str) -> str:
    return (CONTENT_DIR / name).read_text(encoding="utf-8")


def course() -> dict:
    return load_yaml("weeks.yaml")


def phases() -> dict:
    return {p["id"]: p for p in course()["phases"]}


def weeks() -> list:
    return course()["weeks"]


def prompts() -> dict:
    return {p["id"]: p for p in load_yaml("prompts.yaml")["prompts"]}


def page_header(title: str, caption: str = "") -> None:
    st.set_page_config(page_title=f"{title} · Translation in Praxis", page_icon="🔤", layout="wide")
    st.title(title)
    if caption:
        st.caption(caption)
