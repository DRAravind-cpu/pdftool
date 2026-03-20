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

