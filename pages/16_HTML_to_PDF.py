import streamlit as st
from app import *

st.set_page_config(page_title=f"{APP_TITLE} - HTML to PDF", layout="wide")
if st.button("← Home"):
    st.switch_page("app.py")

st.title("HTML to PDF")

deps = get_dependency_status()

st.info("Uses WeasyPrint (pure Python + system libs).")
html = st.text_area("HTML", height=200, key="html_input")
if html and st.button("Convert", key="html2pdf_btn"):
    from weasyprint import HTML

    pdf_bytes = HTML(string=html).write_pdf()
    if not pdf_bytes:
        st.error("HTML→PDF failed to produce output.")
        st.stop()
    download_button("Download PDF", pdf_bytes, "document.pdf")

