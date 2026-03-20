import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
root_str = str(ROOT)
if sys.path[:1] != [root_str]:
    if root_str in sys.path:
        sys.path.remove(root_str)
    sys.path.insert(0, root_str)

import streamlit as st
import app as _app
APP_TITLE = getattr(_app, 'APP_TITLE', 'PDF & Image Tools')
from app import *

st.set_page_config(page_title=f"{APP_TITLE} - Translate PDF", layout="wide")
if st.button("← Home"):
    st.switch_page("app.py")

st.title("Translate PDF")

deps = get_dependency_status()

st.info("Offline-first translation using Argos Translate if installed (no quotas).")
f = st.file_uploader("PDF", type=["pdf"], key="translate")
src = st.text_input("Source language code", value="en", key="tr_src")
dst = st.text_input("Target language code", value="fr", key="tr_dst")
has_argos = False
argos_translate = None
try:
    import argostranslate.package  # type: ignore
    import argostranslate.translate as _argos_translate  # type: ignore

    has_argos = True
    argos_translate = _argos_translate
except Exception:
    has_argos = False

if not has_argos:
    st.warning("Argos Translate not installed. Install with: pip install argostranslate")
if f and st.button("Translate", key="translate_btn"):
    if not has_argos:
        st.stop()
    reader = read_uploaded_pdf(f)
    text = extract_pdf_text(reader)
    translated = argos_translate.translate(text, from_code=src, to_code=dst)  # type: ignore[union-attr]
    st.text_area("Translated text", value=translated, height=200)
    st.download_button(
        "Download translated (txt)",
        translated.encode("utf-8"),
        file_name=f"translated-{src}-to-{dst}.txt",
        mime="text/plain",
    )
    st.download_button(
        "Download translated (pdf)",
        text_to_pdf_bytes(translated, title=f"Translated ({src}→{dst})"),
        file_name=f"translated-{src}-to-{dst}.pdf",
    )

