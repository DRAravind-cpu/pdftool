import streamlit as st
from app import *

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

