import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
from app import *

st.set_page_config(page_title=f"{APP_TITLE} - Upscale Image", layout="wide")
if st.button("← Home"):
    st.switch_page("app.py")

st.title("Upscale Image")

deps = get_dependency_status()

st.subheader("Upscale Image")
st.caption("Upscale with high-quality resampling (offline).")
f = st.file_uploader(
    "Image", type=["jpg", "jpeg", "png", "webp", "heic", "heif", "tif", "tiff", "bmp", "gif"], key="img_upscale"
)
factor = st.selectbox("Scale", [2, 3, 4], index=0, key="img_upscale_factor")
if f and st.button("Upscale", key="img_upscale_btn"):
    from PIL import Image

    img = pil_open_image(f)
    w0, h0 = img.size
    out = img.resize((w0 * factor, h0 * factor), resample=Image.Resampling.LANCZOS)
    data = pil_to_bytes(out, "png")
    st.download_button("Download", data, file_name=f"{Path(f.name).stem}-upscaled.png", mime="image/png")

