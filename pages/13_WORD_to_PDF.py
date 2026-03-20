import streamlit as st
from app import *

st.set_page_config(page_title=f"{APP_TITLE} - WORD to PDF", layout="wide")
if st.button("← Home"):
    st.switch_page("app.py")

st.title("WORD to PDF")

deps = get_dependency_status()

st.info("Uses LibreOffice (soffice) if installed.")
if not deps.libreoffice:
    st.warning("Requires 'soffice' (LibreOffice).")
f = st.file_uploader("DOC/DOCX", type=["doc", "docx"], key="doc2pdf")
if f and st.button("Convert", key="doc2pdf_btn"):
    if not deps.libreoffice:
        st.stop()
    with tempfile.TemporaryDirectory() as td:
        in_path = Path(td) / f.name
        in_path.write_bytes(f.read())
        subprocess.check_call([
            deps.soffice_cmd or "soffice",
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            td,
            str(in_path),
        ])
        out_path = in_path.with_suffix(".pdf")
        download_button("Download PDF", out_path.read_bytes(), out_path.name)

