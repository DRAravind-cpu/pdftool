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

st.set_page_config(page_title=f"{APP_TITLE} - PDF to WORD", layout="wide")
if st.button("← Home"):
    st.switch_page("app.py")

st.title("PDF to WORD")

deps = get_dependency_status()

st.info("Basic text extraction to DOCX (layout not preserved).")
f = st.file_uploader("PDF", type=["pdf"], key="pdf2word")
if f and st.button("Convert", key="pdf2word_btn"):
    from docx import Document

    reader = read_uploaded_pdf(f)
    doc = Document()
    for page in reader.pages:
        text = page.extract_text() or ""
        doc.add_paragraph(text)
    out = io.BytesIO()
    doc.save(out)
    st.download_button(
        "Download DOCX",
        out.getvalue(),
        file_name="document.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )

