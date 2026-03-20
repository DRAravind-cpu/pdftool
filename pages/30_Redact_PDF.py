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
st.set_page_config(page_title=f"{APP_TITLE} - Redact PDF", layout="wide")
if st.button("← Home"):
    st.switch_page("app.py")

st.title("Redact PDF")

deps = get_dependency_status()

st.info(
    "Safe redaction by rasterizing pages and burning black boxes into the pixels. Requires Poppler (`pdftoppm`)."
)
if not deps.poppler:
    st.warning("Requires 'pdftoppm' (poppler).")
f = st.file_uploader("PDF", type=["pdf"], key="redact_pdf")
st.caption("Boxes format (normalized coords, origin top-left): page,x1,y1,x2,y2 per line. Example: 1,0.1,0.2,0.9,0.3")
boxes_text = st.text_area("Redaction boxes", height=120, key="redact_boxes")
if f and st.button("Redact", key="redact_btn"):
    if not deps.poppler:
        st.stop()
    redact_boxes: list[tuple[int, float, float, float, float]] = []
    for line in (boxes_text or "").splitlines():
        line = line.strip()
        if not line:
            continue
        parts = [p.strip() for p in line.split(",")]
        if len(parts) != 5:
            st.error(f"Invalid line: {line}")
            st.stop()
        page = int(parts[0])
        x1, y1, x2, y2 = map(float, parts[1:])
        redact_boxes.append((page, x1, y1, x2, y2))
    try:
        out = redact_via_rasterize(f.read(), redact_boxes, poppler_path=deps.poppler_path)
    except Exception as e:
        st.error(f"Redaction failed: {e}")
        st.stop()
    download_button("Download redacted PDF", out, "redacted.pdf")

