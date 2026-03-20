import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
from app import *

st.set_page_config(page_title=f"{APP_TITLE} - Add page numbers", layout="wide")
if st.button("← Home"):
    st.switch_page("app.py")

st.title("Add page numbers")

deps = get_dependency_status()

st.info("Adds simple bottom-center page numbers.")
f = st.file_uploader("PDF", type=["pdf"], key="pagenum")
if f and st.button("Add numbers", key="pagenum_btn"):
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import inch

    reader = read_uploaded_pdf(f)
    writer = PdfWriter()
    total = len(reader.pages)
    for i, page in enumerate(reader.pages, start=1):
        packet = io.BytesIO()
        c = canvas.Canvas(packet, pagesize=(page.mediabox.width, page.mediabox.height))
        c.setFont("Helvetica", 10)
        c.drawCentredString(float(page.mediabox.width) / 2, 0.5 * inch, f"{i} / {total}")
        c.save()
        packet.seek(0)
        overlay = PdfReader(packet)
        page.merge_page(overlay.pages[0])
        writer.add_page(page)
    download_button("Download PDF", writer_to_bytes(writer), "page-numbered.pdf")

