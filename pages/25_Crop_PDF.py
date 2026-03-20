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

st.set_page_config(page_title=f"{APP_TITLE} - Crop PDF", layout="wide")
if st.button("← Home"):
    st.switch_page("app.py")

st.title("Crop PDF")

deps = get_dependency_status()

st.info("Sets a crop box for all pages.")
f = st.file_uploader("PDF", type=["pdf"], key="crop")
left = st.number_input("Left", min_value=0.0, value=0.0)
bottom = st.number_input("Bottom", min_value=0.0, value=0.0)
right = st.number_input("Right (from left)", min_value=1.0, value=500.0)
top = st.number_input("Top (from bottom)", min_value=1.0, value=700.0)
if f and st.button("Apply crop", key="crop_btn"):
    reader = read_uploaded_pdf(f)
    writer = PdfWriter()
    for page in reader.pages:
        page.cropbox.lower_left = (left, bottom)
        page.cropbox.upper_right = (left + right, bottom + top)
        writer.add_page(page)
    download_button("Download cropped PDF", writer_to_bytes(writer), "cropped.pdf")

