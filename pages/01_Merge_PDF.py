import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
from app import *

st.set_page_config(page_title=f"{APP_TITLE} - Merge PDF", layout="wide")
if st.button("← Home"):
    st.switch_page("app.py")

st.title("Merge PDF")

deps = get_dependency_status()

files = st.file_uploader(
    "Select PDFs", type=["pdf"], accept_multiple_files=True, key="merge"
)
ordered_files = show_sorted_names(files)
if files and st.button("Merge", key="merge_btn"):
    out = merge_pdfs(ordered_files)
    download_button("Download merged PDF", out, "merged.pdf")

