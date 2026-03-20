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

st.set_page_config(page_title=f"{APP_TITLE} - Compress IMAGE", layout="wide")
if st.button("← Home"):
    st.switch_page("app.py")

st.title("Compress IMAGE")

deps = get_dependency_status()

st.subheader("Compress IMAGE")
st.caption("Compress JPG/PNG/WebP by re-encoding.")
files = st.file_uploader(
    "Images",
    type=["jpg", "jpeg", "png", "webp", "heic", "heif", "tif", "tiff", "bmp", "gif"],
    accept_multiple_files=True,
    key="img_compress",
)
ordered_files = show_sorted_names(files)
quality = st.slider("Quality", 10, 95, 80, key="img_compress_q")
out_fmt = st.selectbox("Output", ["jpeg", "webp", "png"], index=0, key="img_compress_fmt")
if files and st.button("Compress", key="img_compress_btn"):
    outs: list[tuple[str, bytes]] = []
    for f in ordered_files:
        img = pil_open_image(f)
        data = pil_to_bytes(img, out_fmt, quality=quality)
        name = Path(f.name).stem + "." + ("jpg" if out_fmt == "jpeg" else out_fmt)
        outs.append((name, data))
    z = zip_files(outs) if len(outs) > 1 else outs[0][1]
    if len(outs) > 1:
        st.download_button("Download ZIP", z, file_name="compressed-images.zip", mime="application/zip")
    else:
        st.download_button(
            "Download image",
            z,
            file_name=outs[0][0],
            mime="image/jpeg" if out_fmt == "jpeg" else f"image/{out_fmt}",
        )

