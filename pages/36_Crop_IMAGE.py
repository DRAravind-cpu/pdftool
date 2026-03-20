import streamlit as st
from app import *

st.set_page_config(page_title=f"{APP_TITLE} - Crop IMAGE", layout="wide")
if st.button("← Home"):
    st.switch_page("app.py")

st.title("Crop IMAGE")

deps = get_dependency_status()

st.subheader("Crop IMAGE")
st.caption("Crop by pixel coordinates.")
f = st.file_uploader(
    "Image", type=["jpg", "jpeg", "png", "webp", "heic", "heif", "tif", "tiff", "bmp", "gif"], key="img_crop"
)
if f:
    img = pil_open_image(f)
    w0, h0 = img.size
    st.image(img, use_container_width=True)
    x1 = st.number_input("Left", min_value=0, value=0, key="img_crop_x1")
    y1 = st.number_input("Top", min_value=0, value=0, key="img_crop_y1")
    x2 = st.number_input("Right", min_value=1, value=w0, key="img_crop_x2")
    y2 = st.number_input("Bottom", min_value=1, value=h0, key="img_crop_y2")
    if st.button("Crop", key="img_crop_btn"):
        out = img.crop((int(x1), int(y1), int(x2), int(y2)))
        data = pil_to_bytes(out, "png")
        st.download_button("Download", data, file_name=f"{Path(f.name).stem}-cropped.png", mime="image/png")

