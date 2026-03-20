import streamlit as st
from app import *

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

