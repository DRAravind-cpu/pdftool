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
st.set_page_config(page_title=f"{APP_TITLE} - PDF to EXCEL", layout="wide")
if st.button("← Home"):
    st.switch_page("app.py")

st.title("PDF to EXCEL")

deps = get_dependency_status()

st.info("Extracts tables is non-trivial; this tool exports page text into a spreadsheet (one sheet per page).")
f = st.file_uploader("PDF", type=["pdf"], key="pdf2xls")
if f and st.button("Convert", key="pdf2xls_btn"):
    import openpyxl

    reader = read_uploaded_pdf(f)
    wb = openpyxl.Workbook()
    for i, page in enumerate(reader.pages, start=1):
        if i == 1 and wb.active is not None:
            ws = wb.active
            ws.title = "Page 1"
        else:
            ws = wb.create_sheet(title=f"Page {i}")
        text = (page.extract_text() or "").splitlines()
        for r, line in enumerate(text, start=1):
            ws.cell(row=r, column=1, value=line)
    out = io.BytesIO()
    wb.save(out)
    st.download_button(
        "Download XLSX",
        out.getvalue(),
        file_name="document.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

