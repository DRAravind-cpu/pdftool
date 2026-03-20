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

