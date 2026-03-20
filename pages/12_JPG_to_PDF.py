import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
root_str = str(ROOT)
if sys.path[:1] != [root_str]:
    if root_str in sys.path:
        sys.path.remove(root_str)
    sys.path.insert(0, root_str)

import streamlit as st
import runpy

_app_ns = runpy.run_path(str((ROOT / 'app.py').resolve()))
for _name, _value in _app_ns.items():
    if not _name.startswith('__'):
        globals()[_name] = _value

APP_TITLE = _app_ns.get('APP_TITLE', 'PDF & Image Tools')
st.set_page_config(page_title=f"{APP_TITLE} - JPG to PDF", layout="wide")
if st.button("← Home"):
    st.switch_page("app.py")

st.title("JPG to PDF")

deps = get_dependency_status()

imgs = st.file_uploader(
    "Select images",
    type=["jpg", "jpeg", "png", "webp", "heic", "heif", "tif", "tiff", "bmp", "gif"],
    accept_multiple_files=True,
    key="img2pdf",
)
ordered_imgs = show_sorted_names(imgs)
if imgs and st.button("Convert to PDF", key="img2pdf_btn"):
    from PIL import Image

    pil_imgs = []
    for f in ordered_imgs:
        img = pil_open_image(f).convert("RGB")
        pil_imgs.append(img)
    out = io.BytesIO()
    pil_imgs[0].save(out, format="PDF", save_all=True, append_images=pil_imgs[1:])
    download_button("Download PDF", out.getvalue(), "images.pdf")

