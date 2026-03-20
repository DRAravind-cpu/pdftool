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
st.set_page_config(page_title=f"{APP_TITLE} - Convert to JPG", layout="wide")
if st.button("← Home"):
    st.switch_page("app.py")

st.title("Convert to JPG")

deps = get_dependency_status()

st.subheader("Convert to JPG")
st.caption("Turn PNG/WebP/TIFF/etc into JPG.")
files = st.file_uploader(
    "Images",
    type=["png", "webp", "heic", "heif", "tif", "tiff", "bmp", "gif", "jpg", "jpeg"],
    accept_multiple_files=True,
    key="img_to_jpg",
)
ordered_files = show_sorted_names(files)
quality = st.slider("JPG quality", 10, 95, 85, key="img_to_jpg_q")
if files and st.button("Convert", key="img_to_jpg_btn"):
    outs = []
    for f in ordered_files:
        img = pil_open_image(f)
        data = pil_to_bytes(img, "jpeg", quality=quality)
        outs.append((Path(f.name).stem + ".jpg", data))
    z = zip_files(outs) if len(outs) > 1 else outs[0][1]
    if len(outs) > 1:
        st.download_button("Download ZIP", z, file_name="converted-jpg.zip", mime="application/zip")
    else:
        st.download_button("Download JPG", z, file_name=outs[0][0], mime="image/jpeg")

