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

