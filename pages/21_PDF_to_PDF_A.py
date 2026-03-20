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
st.set_page_config(page_title=f"{APP_TITLE} - PDF to PDF/A", layout="wide")
if st.button("← Home"):
    st.switch_page("app.py")

st.title("PDF to PDF/A")

deps = get_dependency_status()

st.info("Uses Ghostscript to convert to PDF/A (best-effort).")
if not deps.ghostscript:
    st.warning("Requires 'gs' (Ghostscript).")
f = st.file_uploader("PDF", type=["pdf"], key="pdf2pdfa")
if f and st.button("Convert", key="pdf2pdfa_btn"):
    if not deps.ghostscript:
        st.stop()
    with tempfile.TemporaryDirectory() as td:
        in_path = Path(td) / "input.pdf"
        out_path = Path(td) / "output_pdfa.pdf"
        in_path.write_bytes(f.read())
        subprocess.check_call(
            [
                deps.gs_cmd or "gs",
                "-dPDFA",
                "-dBATCH",
                "-dNOPAUSE",
                "-sProcessColorModel=DeviceRGB",
                "-sDEVICE=pdfwrite",
                "-sOutputFile=" + str(out_path),
                str(in_path),
            ]
        )
        download_button("Download PDF/A", out_path.read_bytes(), "document-pdfa.pdf")

