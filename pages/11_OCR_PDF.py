import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
root_str = str(ROOT)
if sys.path[:1] != [root_str]:
    if root_str in sys.path:
        sys.path.remove(root_str)
    sys.path.insert(0, root_str)

import streamlit as st
import importlib
import importlib.util

def _load_local_app():
    app_path = (ROOT / 'app.py').resolve()
    spec = importlib.util.spec_from_file_location('app', app_path)
    if spec is None or spec.loader is None:
        raise ImportError(f'Cannot load app.py from {app_path}')
    module = importlib.util.module_from_spec(spec)
    sys.modules['app'] = module
    spec.loader.exec_module(module)
    return module

try:
    import app as _app
    _app_file = getattr(_app, '__file__', '')
    if not _app_file or Path(_app_file).resolve() != (ROOT / 'app.py').resolve():
        _app = _load_local_app()
except Exception:
    _app = _load_local_app()

APP_TITLE = getattr(_app, 'APP_TITLE', 'PDF & Image Tools')
from app import *

st.set_page_config(page_title=f"{APP_TITLE} - OCR PDF", layout="wide")
if st.button("← Home"):
    st.switch_page("app.py")

st.title("OCR PDF")

deps = get_dependency_status()

st.info("Uses Tesseract + Poppler to produce a searchable PDF (best-effort).")
if not deps.tesseract or not deps.poppler:
    st.warning("Requires 'tesseract' and 'pdftoppm' (poppler).")

if deps.tesseract and "tesseract_langs" not in st.session_state:
    st.session_state["tesseract_langs"] = tesseract_list_langs(
        tesseract_cmd=deps.tesseract_cmd or "tesseract"
    )
available_langs = st.session_state.get("tesseract_langs", [])

if available_langs:
    default_langs = [l for l in ["eng", "tam"] if l in available_langs]
    if not default_langs and "eng" in available_langs:
        default_langs = ["eng"]
    langs = st.multiselect(
        "OCR languages",
        options=available_langs,
        default=default_langs,
        help="Tesseract language codes. Install extra language data on the host to add more options.",
    )
    if "tam" not in available_langs:
        st.caption("Tamil (tam) is not installed on this host.")
else:
    langs = st.multiselect(
        "OCR languages",
        options=["eng", "tam"],
        default=["eng"],
        help="Language list unavailable. This host may be missing Tesseract language data.",
    )

lang_arg = "+".join([l for l in langs if l]) if langs else None
ocr_config = "--oem 1 --psm 3 -c preserve_interword_spaces=1"
st.caption(
    "OCR accuracy depends on scan quality; exact extraction cannot be guaranteed for all PDFs. "
    "For best results, use correct language(s) and a clean scan."
)

f = st.file_uploader("PDF", type=["pdf"], key="ocr")

run_col, extract_col = st.columns(2)
run_ocr = run_col.button("Run OCR", key="ocr_btn")
extract_text = extract_col.button("Extract text", key="ocr_extract_btn")

if f and (run_ocr or extract_text):
    if not deps.tesseract or not deps.poppler:
        st.stop()
    import pytesseract

    pdf_bytes = uploaded_file_bytes(f)
    images = pdf2image_convert_from_bytes(
        pdf_bytes, fmt="png", dpi=220, poppler_path=deps.poppler_path
    )

    if run_ocr:
        writer = PdfWriter()
        for img in images:
            pdf_page_bytes = pytesseract.image_to_pdf_or_hocr(
                img,
                extension="pdf",
                lang=lang_arg,
                config=ocr_config,
            )
            if isinstance(pdf_page_bytes, str):
                pdf_page_bytes = pdf_page_bytes.encode("utf-8")
            page_reader = PdfReader(io.BytesIO(pdf_page_bytes))
            writer.add_page(page_reader.pages[0])
        download_button("Download searchable PDF", writer_to_bytes(writer), "ocr.pdf")

    if extract_text:
        chunks: list[str] = []
        for img in images:
            txt = pytesseract.image_to_string(
                img,
                lang=lang_arg,
                config=ocr_config,
            )
            chunks.append(txt or "")
        extracted = "\n\n".join(chunks).strip()
        st.text_area("Extracted text", value=extracted, height=420)
        st.download_button(
            "Download extracted text (txt)",
            extracted.encode("utf-8"),
            file_name="ocr-extracted.txt",
            mime="text/plain",
        )

