import streamlit as st
from app import *

st.set_page_config(page_title=f"{APP_TITLE} - PDF to JPG", layout="wide")
if st.button("← Home"):
    st.switch_page("app.py")

st.title("PDF to JPG")

deps = get_dependency_status()

st.info("Uses Poppler via pdf2image.")
if not deps.poppler:
    st.warning("Requires 'pdftoppm' (poppler).")
f = st.file_uploader("PDF", type=["pdf"], key="pdf2jpg")
if f and st.button("Convert", key="pdf2jpg_btn"):
    if not deps.poppler:
        st.stop()

    images = pdf2image_convert_from_bytes(f.read(), fmt="jpeg", poppler_path=deps.poppler_path)
    for i, img in enumerate(images, start=1):
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=95)
        st.download_button(
            f"Download page {i}",
            buf.getvalue(),
            file_name=f"page-{i}.jpg",
            mime="image/jpeg",
        )

