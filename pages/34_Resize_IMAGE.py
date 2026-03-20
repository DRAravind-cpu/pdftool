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
st.set_page_config(page_title=f"{APP_TITLE} - Resize IMAGE", layout="wide")
if st.button("← Home"):
    st.switch_page("app.py")

st.title("Resize IMAGE")

deps = get_dependency_status()

st.subheader("Resize IMAGE")
st.caption("Resize by percent or exact width/height.")
f = st.file_uploader(
    "Image", type=["jpg", "jpeg", "png", "webp", "heic", "heif", "tif", "tiff", "bmp", "gif"], key="img_resize"
)
mode = st.radio("Mode", ["Percent", "Exact"], horizontal=True, key="img_resize_mode")
keep = st.checkbox("Keep aspect ratio", value=True, key="img_resize_keep")
if f:
    img = pil_open_image(f)
    w0, h0 = img.size
    st.image(img, caption=f"{w0}×{h0}", use_container_width=True)
    if mode == "Percent":
        pct = st.slider("Scale %", 10, 400, 100, key="img_resize_pct")
        w = max(1, int(w0 * pct / 100))
        h = max(1, int(h0 * pct / 100))
    else:
        w = st.number_input("Width", min_value=1, value=w0, key="img_resize_w")
        h = st.number_input("Height", min_value=1, value=h0, key="img_resize_h")
        if keep:
            # adjust height when width changes (simple)
            h = max(1, int(h0 * (int(w) / w0)))

    if st.button("Resize", key="img_resize_btn"):
        out = img.resize((int(w), int(h)))
        data = pil_to_bytes(out, "png")
        st.download_button("Download", data, file_name=f"{Path(f.name).stem}-resized.png", mime="image/png")

