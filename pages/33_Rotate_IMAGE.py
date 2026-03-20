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

st.set_page_config(page_title=f"{APP_TITLE} - Rotate IMAGE", layout="wide")
if st.button("← Home"):
    st.switch_page("app.py")

st.title("Rotate IMAGE")

deps = get_dependency_status()

st.subheader("Rotate IMAGE")
st.caption("Rotate JPG/PNG by 90/180/270.")
f = st.file_uploader(
    "Image", type=["jpg", "jpeg", "png", "webp", "heic", "heif", "tif", "tiff", "bmp", "gif"], key="img_rotate"
)
deg = st.selectbox("Degrees", [90, 180, 270], index=0, key="img_rotate_deg")
if f and st.button("Rotate", key="img_rotate_btn"):
    img = pil_open_image(f)
    out = img.rotate(-deg, expand=True)
    data = pil_to_bytes(out, "png")
    st.download_button("Download", data, file_name=f"{Path(f.name).stem}-rotated.png", mime="image/png")

