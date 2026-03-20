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

