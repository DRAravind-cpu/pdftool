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
    data = uploaded_file_bytes(f)
    try:
        if deps.qpdf:
            out = qpdf_optimize(data, qpdf_cmd=deps.qpdf_cmd or "qpdf")
        else:
            out = rewrite_pdf_with_pypdf(data)
    except Exception as e:
        st.error(f"Repair failed: {e}")
        st.stop()
    download_button("Download repaired PDF", out, "repaired.pdf")

