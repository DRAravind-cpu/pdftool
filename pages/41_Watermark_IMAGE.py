import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
root_str = str(ROOT)
if sys.path[:1] != [root_str]:
    if root_str in sys.path:
        sys.path.remove(root_str)
    sys.path.insert(0, root_str)

import streamlit as st
import app as _app
APP_TITLE = getattr(_app, 'APP_TITLE', 'PDF & Image Tools')
from app import *

st.set_page_config(page_title=f"{APP_TITLE} - Watermark IMAGE", layout="wide")
if st.button("← Home"):
    st.switch_page("app.py")

st.title("Watermark IMAGE")

deps = get_dependency_status()

st.subheader("Watermark IMAGE")
st.caption("Stamp text watermark with adjustable opacity.")
f = st.file_uploader(
    "Image", type=["jpg", "jpeg", "png", "webp", "heic", "heif", "tif", "tiff", "bmp", "gif"], key="img_wm"
)
text = st.text_input("Watermark text", value="WATERMARK", key="img_wm_text")
opacity = st.slider("Opacity", 5, 100, 25, key="img_wm_op")
if f and st.button("Apply watermark", key="img_wm_btn"):
    from PIL import ImageDraw, ImageFont

    img = pil_open_image(f).convert("RGBA")
    overlay = img.copy()
    draw = ImageDraw.Draw(overlay)
    font = ImageFont.load_default()
    w, h = img.size
    draw.text((w * 0.05, h * 0.9), text, fill=(255, 255, 255, int(255 * opacity / 100)), font=font)
    out = overlay
    data = pil_to_bytes(out, "png")
    st.download_button("Download", data, file_name=f"{Path(f.name).stem}-watermarked.png", mime="image/png")

