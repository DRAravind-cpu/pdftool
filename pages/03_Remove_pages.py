import streamlit as st
from app import *

st.set_page_config(page_title=f"{APP_TITLE} - Remove pages", layout="wide")
if st.button("← Home"):
    st.switch_page("app.py")

st.title("Remove pages")

deps = get_dependency_status()

f = st.file_uploader("PDF", type=["pdf"], key="remove")
pages_text = st.text_input("Pages to remove (e.g., 2, 4-6)", key="remove_pages")
if f and st.button("Remove selected pages", key="remove_btn"):
    reader = read_uploaded_pdf(f)
    ranges = parse_page_ranges(pages_text)
    pages = set()
    for a, b in ranges:
        pages.update(range(min(a, b), max(a, b) + 1))
    out = remove_pages(reader, pages)
    download_button("Download PDF", out, "pages-removed.pdf")

