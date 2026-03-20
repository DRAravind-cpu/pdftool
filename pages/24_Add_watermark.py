import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
from app import *

st.set_page_config(page_title=f"{APP_TITLE} - Add watermark", layout="wide")
if st.button("← Home"):
    st.switch_page("app.py")

st.title("Add watermark")

deps = get_dependency_status()

st.info("Adds a diagonal text watermark on all pages.")
f = st.file_uploader("PDF", type=["pdf"], key="watermark")
text = st.text_input("Watermark text", value="CONFIDENTIAL", key="watermark_text")
if f and st.button("Apply watermark", key="watermark_btn"):
    from reportlab.pdfgen import canvas

    reader = read_uploaded_pdf(f)
    writer = PdfWriter()
    for page in reader.pages:
        packet = io.BytesIO()
        c = canvas.Canvas(packet, pagesize=(page.mediabox.width, page.mediabox.height))
        c.saveState()
        c.setFont("Helvetica-Bold", 48)
        c.translate(float(page.mediabox.width) / 2, float(page.mediabox.height) / 2)
        c.rotate(45)
        c.drawCentredString(0, 0, text)
        c.restoreState()
        c.save()
        packet.seek(0)
        overlay = PdfReader(packet)
        page.merge_page(overlay.pages[0])
        writer.add_page(page)
    download_button("Download PDF", writer_to_bytes(writer), "watermarked.pdf")

