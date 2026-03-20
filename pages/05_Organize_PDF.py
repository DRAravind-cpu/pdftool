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
st.set_page_config(page_title=f"{APP_TITLE} - Organize PDF", layout="wide")
if st.button("← Home"):
    st.switch_page("app.py")

st.title("Organize PDF")

deps = get_dependency_status()

st.info("Reorder pages by providing a new page order list.")
f = st.file_uploader("PDF", type=["pdf"], key="organize")
order_text = st.text_input("New order (e.g., 3,1,2,4)", key="organize_order")
if f and st.button("Reorder", key="organize_btn"):
    reader = read_uploaded_pdf(f)
    try:
        new_order = parse_page_list(order_text)
        out = reorder_pages(reader, new_order)
    except Exception as e:
        st.error(f"Reorder failed: {e}")
        st.stop()
    download_button("Download reordered PDF", out, "reordered.pdf")

