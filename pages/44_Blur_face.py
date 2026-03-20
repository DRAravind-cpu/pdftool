import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
from app import *

st.set_page_config(page_title=f"{APP_TITLE} - Blur face", layout="wide")
if st.button("← Home"):
    st.switch_page("app.py")

st.title("Blur face")

deps = get_dependency_status()

st.subheader("Blur face")
st.caption("Auto face blur uses OpenCV if installed; otherwise use manual boxes.")
f = st.file_uploader(
    "Image", type=["jpg", "jpeg", "png", "webp", "heic", "heif", "tif", "tiff", "bmp", "gif"], key="img_blur"
)
radius = st.slider("Blur radius", 3, 40, 12, key="img_blur_r")
auto = st.checkbox("Auto-detect faces (requires opencv-python)", value=False, key="img_blur_auto")
st.caption("Manual boxes format: x1,y1,x2,y2 per line in pixels")
boxes_text = st.text_area("Manual boxes", height=90, key="img_blur_boxes")
if f and st.button("Blur", key="img_blur_btn"):
    img = pil_open_image(f)
    boxes: list[tuple[int, int, int, int]] = []
    if auto:
        try:
            import cv2  # type: ignore
            import numpy as np  # type: ignore

            rgb = img.convert("RGB")
            arr = np.array(rgb)
            gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
            cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
            faces = cascade.detectMultiScale(gray, 1.1, 5)
            for (x, y, w, h) in faces:
                boxes.append((int(x), int(y), int(x + w), int(y + h)))
        except Exception as e:
            st.warning(f"Auto-detect unavailable: {e}")

    for line in (boxes_text or "").splitlines():
        line = line.strip()
        if not line:
            continue
        parts = [p.strip() for p in line.split(",")]
        if len(parts) != 4:
            st.error(f"Invalid box line: {line}")
            st.stop()
        boxes.append((int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3])))

    if not boxes:
        st.warning("No boxes found (auto or manual).")
        st.stop()
    out = blur_boxes(img, boxes, radius=int(radius))
    data = pil_to_bytes(out, "png")
    st.download_button(
        "Download",
        data,
        file_name=f"{Path(f.name).stem}-blurred.png",
        mime="image/png",
    )



