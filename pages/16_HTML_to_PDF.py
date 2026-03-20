import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
root_str = str(ROOT)
if sys.path[:1] != [root_str]:
    if root_str in sys.path:
        sys.path.remove(root_str)
    sys.path.insert(0, root_str)

import streamlit as st
import runpy

_app_ns = runpy.run_path(str((ROOT / 'app.py').resolve()))
for _name, _value in _app_ns.items():
    if not _name.startswith('__'):
        globals()[_name] = _value

APP_TITLE = _app_ns.get('APP_TITLE', 'PDF & Image Tools')
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

