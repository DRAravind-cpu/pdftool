import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
root_str = str(ROOT)
if sys.path[:1] != [root_str]:
    if root_str in sys.path:
        sys.path.remove(root_str)
    sys.path.insert(0, root_str)

import streamlit as st
import app as _app
APP_TITLE = getattr(_app, 'APP_TITLE', 'PDF & Image Tools')
from app import *

st.set_page_config(page_title=f"{APP_TITLE} - Rotate PDF", layout="wide")
if st.button("← Home"):
    st.switch_page("app.py")

st.title("Rotate PDF")

deps = get_dependency_status()

f = st.file_uploader("PDF", type=["pdf"], key="rotate")
pages_text = st.text_input("Pages to rotate (e.g., 1-3, 5)", key="rotate_pages")
degrees = st.selectbox("Degrees", options=[90, 180, 270], index=0)
if f and st.button("Rotate", key="rotate_btn"):
    reader = read_uploaded_pdf(f)
    ranges = parse_page_ranges(pages_text)
    pages = set()
    for a, b in ranges:
        pages.update(range(min(a, b), max(a, b) + 1))
    out = rotate_pages(reader, pages, degrees)
    download_button("Download rotated PDF", out, "rotated.pdf")

