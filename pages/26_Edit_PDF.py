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

st.set_page_config(page_title=f"{APP_TITLE} - Edit PDF", layout="wide")
if st.button("← Home"):
    st.switch_page("app.py")

st.title("Edit PDF")

deps = get_dependency_status()

st.info("Full PDF editing is broad. Current app supports rotate, crop, watermark, and page numbers.")

