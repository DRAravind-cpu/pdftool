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
st.set_page_config(page_title=f"{APP_TITLE} - Compare PDF", layout="wide")
if st.button("← Home"):
    st.switch_page("app.py")

st.title("Compare PDF")

deps = get_dependency_status()

st.info("Compares extracted text per page (quick diff). For pixel-perfect compare, we can add image-based compare.")
a = st.file_uploader("PDF A", type=["pdf"], key="cmp_a")
b = st.file_uploader("PDF B", type=["pdf"], key="cmp_b")
if a and b and st.button("Compare", key="cmp_btn"):
    from rapidfuzz import fuzz

    ra = read_uploaded_pdf(a)
    rb = read_uploaded_pdf(b)
    pages = max(len(ra.pages), len(rb.pages))
    results = []
    for i in range(pages):
        ta = ra.pages[i].extract_text() if i < len(ra.pages) else ""
        tb = rb.pages[i].extract_text() if i < len(rb.pages) else ""
        score = fuzz.ratio(ta or "", tb or "")
        results.append({"page": i + 1, "similarity": score})
    st.dataframe(results, use_container_width=True)

