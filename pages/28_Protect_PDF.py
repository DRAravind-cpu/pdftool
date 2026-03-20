import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
root_str = str(ROOT)
if sys.path[:1] != [root_str]:
    if root_str in sys.path:
        sys.path.remove(root_str)
    sys.path.insert(0, root_str)

import streamlit as st
import importlib
import importlib.util

def _load_local_app():
    app_path = (ROOT / 'app.py').resolve()
    spec = importlib.util.spec_from_file_location('app', app_path)
    if spec is None or spec.loader is None:
        raise ImportError(f'Cannot load app.py from {app_path}')
    module = importlib.util.module_from_spec(spec)
    sys.modules['app'] = module
    spec.loader.exec_module(module)
    return module

try:
    import app as _app
    _app_file = getattr(_app, '__file__', '')
    if not _app_file or Path(_app_file).resolve() != (ROOT / 'app.py').resolve():
        _app = _load_local_app()
except Exception:
    _app = _load_local_app()

APP_TITLE = getattr(_app, 'APP_TITLE', 'PDF & Image Tools')
from app import *

st.set_page_config(page_title=f"{APP_TITLE} - Protect PDF", layout="wide")
if st.button("← Home"):
    st.switch_page("app.py")

st.title("Protect PDF")

deps = get_dependency_status()

st.info("Encrypts the PDF with a password.")
f = st.file_uploader("PDF", type=["pdf"], key="protect")
pwd = st.text_input("New password", type="password", key="protect_pwd")
if f and st.button("Protect", key="protect_btn"):
    if not pwd:
        st.warning("Password is required.")
        st.stop()
    reader = read_uploaded_pdf(f)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.encrypt(pwd)
    download_button("Download protected PDF", writer_to_bytes(writer), "protected.pdf")

