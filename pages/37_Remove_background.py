import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
from app import *

st.set_page_config(page_title=f"{APP_TITLE} - Remove background", layout="wide")
if st.button("← Home"):
    st.switch_page("app.py")

st.title("Remove background")

deps = get_dependency_status()

st.subheader("Remove background")
st.caption("Best for near-white backgrounds (offline).")
f = st.file_uploader(
    "Image", type=["png", "jpg", "jpeg", "webp", "heic", "heif", "tif", "tiff", "bmp", "gif"], key="img_rmbg"
)
thresh = st.slider("White threshold", 200, 255, 245, key="img_rmbg_t")
if f and st.button("Remove BG", key="img_rmbg_btn"):
    img = pil_open_image(f)
    out = None
    try:
        from rembg import remove  # type: ignore

        out_bytes = remove(f.getvalue())
        st.download_button("Download", out_bytes, file_name=f"{Path(f.name).stem}-nobg.png", mime="image/png")
    except Exception:
        out = simple_remove_background(img, threshold=int(thresh))
        data = pil_to_bytes(out, "png")
        st.download_button("Download", data, file_name=f"{Path(f.name).stem}-nobg.png", mime="image/png")

