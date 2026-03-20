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

for _name in dir(_app):
    if not _name.startswith('__'):
        globals()[_name] = getattr(_app, _name)

APP_TITLE = getattr(_app, 'APP_TITLE', 'PDF & Image Tools')
st.set_page_config(page_title=f"{APP_TITLE} - Sign PDF", layout="wide")
if st.button("← Home"):
    st.switch_page("app.py")

st.title("Sign PDF")

deps = get_dependency_status()

st.info("Adds a visible signature stamp image (not a cryptographic certificate signature).")
f = st.file_uploader("PDF", type=["pdf"], key="sign_pdf")
sig = st.file_uploader("Signature image (PNG)", type=["png"], key="sign_img")
pages_text = st.text_input("Pages to sign (e.g., 1, 3-4)", key="sign_pages")
x = st.number_input("X (points)", value=50.0)
y = st.number_input("Y (points)", value=50.0)
w = st.number_input("Width (points)", value=200.0, min_value=10.0)
if f and sig and st.button("Apply signature", key="sign_btn"):
    reader = read_uploaded_pdf(f)
    ranges = parse_page_ranges(pages_text)
    pages = set()
    for a, b in ranges:
        pages.update(range(min(a, b), max(a, b) + 1))
    try:
        out = stamp_signature(reader, sig.read(), pages, x, y, w)
    except Exception as e:
        st.error(f"Signing failed: {e}")
        st.stop()
    download_button("Download signed PDF", out, "signed.pdf")

