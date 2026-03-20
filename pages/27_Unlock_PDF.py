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
st.set_page_config(page_title=f"{APP_TITLE} - Unlock PDF", layout="wide")
if st.button("← Home"):
    st.switch_page("app.py")

st.title("Unlock PDF")

deps = get_dependency_status()

st.info("Removes a password if you provide it (no brute forcing).")
f = st.file_uploader("Encrypted PDF", type=["pdf"], key="unlock")
pwd = st.text_input("Password", type="password", key="unlock_pwd")
if f and st.button("Unlock", key="unlock_btn"):
    data = f.read()
    reader = PdfReader(io.BytesIO(data))
    if reader.is_encrypted:
        ok = reader.decrypt(pwd)
        if not ok:
            st.error("Wrong password.")
            st.stop()
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    download_button("Download unlocked PDF", writer_to_bytes(writer), "unlocked.pdf")

