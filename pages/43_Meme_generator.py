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

st.set_page_config(page_title=f"{APP_TITLE} - Meme generator", layout="wide")
if st.button("← Home"):
    st.switch_page("app.py")

st.title("Meme generator")

deps = get_dependency_status()

st.subheader("Meme generator")
st.caption("Add top/bottom text.")
f = st.file_uploader(
    "Image", type=["jpg", "jpeg", "png", "webp", "heic", "heif", "tif", "tiff", "bmp", "gif"], key="img_meme"
)
top = st.text_input("Top text", key="img_meme_top")
bottom = st.text_input("Bottom text", key="img_meme_bottom")
if f and st.button("Generate", key="img_meme_btn"):
    from PIL import ImageDraw, ImageFont

    img = pil_open_image(f).convert("RGB")
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    w, h = img.size

    def outline_text(x, y, t):
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                draw.text((x + dx, y + dy), t, font=font, fill=(0, 0, 0))
        draw.text((x, y), t, font=font, fill=(255, 255, 255))

    if top:
        outline_text(10, 10, top)
    if bottom:
        outline_text(10, h - 25, bottom)
    data = pil_to_bytes(img, "png")
    st.download_button(
        "Download",
        data,
        file_name=f"{Path(f.name).stem}-meme.png",
        mime="image/png",
    )

