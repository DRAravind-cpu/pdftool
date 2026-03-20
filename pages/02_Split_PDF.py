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

st.set_page_config(page_title=f"{APP_TITLE} - Split PDF", layout="wide")
if st.button("← Home"):
    st.switch_page("app.py")

st.title("Split PDF")

deps = get_dependency_status()

f = st.file_uploader("PDF", type=["pdf"], key="split")
ranges_text = st.text_input(
    "Page ranges (e.g., 1-3, 5, 7-9)", key="split_ranges"
)
if f and st.button("Split", key="split_btn"):
    reader = read_uploaded_pdf(f)
    ranges = parse_page_ranges(ranges_text)
    parts = split_pdf_by_ranges(reader, ranges)
    if not parts:
        st.warning("No valid ranges provided.")
    for name, data in parts:
        download_button(f"Download {name}", data, name)

