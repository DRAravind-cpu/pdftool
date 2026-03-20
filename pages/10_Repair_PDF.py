import streamlit as st
from app import *

st.set_page_config(page_title=f"{APP_TITLE} - Repair PDF", layout="wide")
if st.button("← Home"):
    st.switch_page("app.py")

st.title("Repair PDF")

deps = get_dependency_status()

st.info(
    "Attempts to open and re-save the PDF to fix minor structure issues. If `qpdf` is installed, it will also attempt a clean rewrite."
)
f = st.file_uploader("PDF", type=["pdf"], key="repair")
if f and st.button("Repair", key="repair_btn"):
    data = _uploaded_file_bytes(f)
    try:
        if deps.qpdf:
            out = qpdf_optimize(data, qpdf_cmd=deps.qpdf_cmd or "qpdf")
        else:
            out = rewrite_pdf_with_pypdf(data)
    except Exception as e:
        st.error(f"Repair failed: {e}")
        st.stop()
    download_button("Download repaired PDF", out, "repaired.pdf")

