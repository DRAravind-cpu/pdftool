import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
from app import *

st.set_page_config(page_title=f"{APP_TITLE} - AI Summarizer", layout="wide")
if st.button("← Home"):
    st.switch_page("app.py")

st.title("AI Summarizer")

deps = get_dependency_status()

f = st.file_uploader("PDF", type=["pdf"], key="summarize")
n = st.slider("Sentences", min_value=3, max_value=15, value=6)
if f and st.button("Summarize", key="summarize_btn"):
    reader = read_uploaded_pdf(f)
    text = extract_pdf_text(reader)
    summary = simple_summarize(text, sentence_count=n)
    st.text_area("Summary", value=summary, height=200)
    st.download_button("Download summary (txt)", summary.encode("utf-8"), "summary.txt", "text/plain")
    st.download_button("Download summary (pdf)", text_to_pdf_bytes(summary, title="Summary"), "summary.pdf")

