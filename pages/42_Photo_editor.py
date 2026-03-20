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

st.set_page_config(page_title=f"{APP_TITLE} - Photo editor", layout="wide")
if st.button("← Home"):
    st.switch_page("app.py")

st.title("Photo editor")

deps = get_dependency_status()

st.subheader("Photo editor")
st.caption("Adjust brightness/contrast/saturation/sharpness.")
f = st.file_uploader(
    "Image", type=["jpg", "jpeg", "png", "webp", "heic", "heif", "tif", "tiff", "bmp", "gif"], key="img_edit"
)
if f:
    from PIL import ImageEnhance

    img = pil_open_image(f)
    st.image(img, use_container_width=True)
    bright = st.slider("Brightness", 0.2, 2.0, 1.0, 0.05, key="img_edit_b")
    contrast = st.slider("Contrast", 0.2, 2.0, 1.0, 0.05, key="img_edit_c")
    color = st.slider("Saturation", 0.0, 2.0, 1.0, 0.05, key="img_edit_s")
    sharp = st.slider("Sharpness", 0.0, 3.0, 1.0, 0.05, key="img_edit_sh")
    if st.button("Apply edits", key="img_edit_btn"):
        out = ImageEnhance.Brightness(img).enhance(bright)
        out = ImageEnhance.Contrast(out).enhance(contrast)
        out = ImageEnhance.Color(out).enhance(color)
        out = ImageEnhance.Sharpness(out).enhance(sharp)
        data = pil_to_bytes(out, "png")
        st.download_button(
            "Download",
            data,
            file_name=f"{Path(f.name).stem}-edited.png",
            mime="image/png",
        )

