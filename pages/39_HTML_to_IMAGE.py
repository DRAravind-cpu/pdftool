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
st.set_page_config(page_title=f"{APP_TITLE} - HTML to IMAGE", layout="wide")
if st.button("← Home"):
    st.switch_page("app.py")

st.title("HTML to IMAGE")

deps = get_dependency_status()

st.subheader("HTML to IMAGE")
st.caption("Renders HTML to PDF then converts pages to PNG (needs Poppler).")
html = st.text_area("HTML", height=120, key="html_to_img")
if not deps.poppler:
    st.warning("Requires 'pdftoppm' (poppler).")
if html and st.button("Render", key="html_to_img_btn"):
    if not deps.poppler:
        st.stop()
    from weasyprint import HTML

    pdf_bytes = HTML(string=html).write_pdf()
    if not pdf_bytes:
        st.error("HTML→PDF failed to produce output.")
        st.stop()
    images = pdf2image_convert_from_bytes(pdf_bytes, fmt="png", dpi=200, poppler_path=deps.poppler_path)
    outs = []
    for i, img in enumerate(images, start=1):
        outs.append((f"page-{i}.png", pil_to_bytes(img, "png")))
    z = zip_files(outs) if len(outs) > 1 else outs[0][1]
    if len(outs) > 1:
        st.download_button("Download ZIP", z, file_name="html-images.zip", mime="application/zip")
    else:
        st.download_button("Download PNG", z, file_name=outs[0][0], mime="image/png")

