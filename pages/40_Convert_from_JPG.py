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

st.set_page_config(page_title=f"{APP_TITLE} - Convert from JPG", layout="wide")
if st.button("← Home"):
    st.switch_page("app.py")

st.title("Convert from JPG")

deps = get_dependency_status()

st.subheader("Convert from JPG")
st.caption("Convert JPG to PNG/WebP/PDF.")
files = st.file_uploader("JPG images", type=["jpg", "jpeg"], accept_multiple_files=True, key="img_from_jpg")
ordered_files = show_sorted_names(files)
target = st.selectbox("Target", ["png", "webp", "pdf"], index=0, key="img_from_jpg_target")
quality = st.slider("Quality (WebP)", 10, 95, 85, key="img_from_jpg_q")
if files and st.button("Convert", key="img_from_jpg_btn"):
    if target == "pdf":
        from PIL import Image

        pil_imgs = [pil_open_image(f).convert("RGB") for f in ordered_files]
        buf = io.BytesIO()
        pil_imgs[0].save(buf, format="PDF", save_all=True, append_images=pil_imgs[1:])
        st.download_button("Download PDF", buf.getvalue(), file_name="images.pdf", mime="application/pdf")
    else:
        outs = []
        for f in ordered_files:
            img = pil_open_image(f)
            data = pil_to_bytes(img, target, quality=quality)
            outs.append((Path(f.name).stem + f".{target}", data))
        z = zip_files(outs) if len(outs) > 1 else outs[0][1]
        if len(outs) > 1:
            st.download_button("Download ZIP", z, file_name=f"converted-{target}.zip", mime="application/zip")
        else:
            st.download_button("Download", z, file_name=outs[0][0], mime=f"image/{target}")

