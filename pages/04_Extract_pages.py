import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
from app import *

st.set_page_config(page_title=f"{APP_TITLE} - Extract pages", layout="wide")
if st.button("← Home"):
    st.switch_page("app.py")

st.title("Extract pages")

deps = get_dependency_status()

f = st.file_uploader("PDF", type=["pdf"], key="extract")
ranges_text = st.text_input("Pages to extract (e.g., 1-2, 5)", key="extract_ranges")
if f and st.button("Extract", key="extract_btn"):
    reader = read_uploaded_pdf(f)
    ranges = parse_page_ranges(ranges_text)
    parts = split_pdf_by_ranges(reader, ranges)
    if not parts:
        st.warning("No valid page selection provided.")
    for name, data in parts:
        download_button(f"Download {name}", data, name)

