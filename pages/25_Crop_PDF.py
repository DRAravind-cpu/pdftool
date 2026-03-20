import streamlit as st
from app import *

st.set_page_config(page_title=f"{APP_TITLE} - Crop PDF", layout="wide")
if st.button("← Home"):
    st.switch_page("app.py")

st.title("Crop PDF")

deps = get_dependency_status()

st.info("Sets a crop box for all pages.")
f = st.file_uploader("PDF", type=["pdf"], key="crop")
left = st.number_input("Left", min_value=0.0, value=0.0)
bottom = st.number_input("Bottom", min_value=0.0, value=0.0)
right = st.number_input("Right (from left)", min_value=1.0, value=500.0)
top = st.number_input("Top (from bottom)", min_value=1.0, value=700.0)
if f and st.button("Apply crop", key="crop_btn"):
    reader = read_uploaded_pdf(f)
    writer = PdfWriter()
    for page in reader.pages:
        page.cropbox.lower_left = (left, bottom)
        page.cropbox.upper_right = (left + right, bottom + top)
        writer.add_page(page)
    download_button("Download cropped PDF", writer_to_bytes(writer), "cropped.pdf")

