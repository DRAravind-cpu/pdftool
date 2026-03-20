import streamlit as st
from app import *

st.set_page_config(page_title=f"{APP_TITLE} - Edit PDF", layout="wide")
if st.button("← Home"):
    st.switch_page("app.py")

st.title("Edit PDF")

deps = get_dependency_status()

st.info("Full PDF editing is broad. Current app supports rotate, crop, watermark, and page numbers.")

