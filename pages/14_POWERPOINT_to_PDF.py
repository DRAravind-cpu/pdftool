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
st.set_page_config(page_title=f"{APP_TITLE} - POWERPOINT to PDF", layout="wide")
if st.button("← Home"):
    st.switch_page("app.py")

st.title("POWERPOINT to PDF")

deps = get_dependency_status()

st.info("Uses LibreOffice (soffice) if installed.")
if not deps.libreoffice:
    st.warning("Requires 'soffice' (LibreOffice).")
f = st.file_uploader("PPT/PPTX", type=["ppt", "pptx"], key="ppt2pdf")
if f and st.button("Convert", key="ppt2pdf_btn"):
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

