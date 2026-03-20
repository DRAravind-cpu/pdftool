import streamlit as st
from app import *

st.set_page_config(page_title=f"{APP_TITLE} - OCR PDF", layout="wide")
if st.button("← Home"):
    st.switch_page("app.py")

st.title("OCR PDF")

deps = get_dependency_status()

st.info("Uses Tesseract + Poppler to produce a searchable PDF (best-effort).")
if not deps.tesseract or not deps.poppler:
    st.warning("Requires 'tesseract' and 'pdftoppm' (poppler).")
f = st.file_uploader("PDF", type=["pdf"], key="ocr")
if f and st.button("Run OCR", key="ocr_btn"):
    if not deps.tesseract or not deps.poppler:
        st.stop()
    import pytesseract

    images = pdf2image_convert_from_bytes(f.read(), fmt="png", dpi=200, poppler_path=deps.poppler_path)
    writer = PdfWriter()
    for img in images:
        pdf_page_bytes = pytesseract.image_to_pdf_or_hocr(img, extension="pdf")
        if isinstance(pdf_page_bytes, str):
            pdf_page_bytes = pdf_page_bytes.encode("utf-8")
        page_reader = PdfReader(io.BytesIO(pdf_page_bytes))
        writer.add_page(page_reader.pages[0])
    download_button("Download searchable PDF", writer_to_bytes(writer), "ocr.pdf")

