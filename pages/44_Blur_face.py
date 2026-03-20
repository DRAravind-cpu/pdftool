import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
root_str = str(ROOT)
if sys.path[:1] != [root_str]:
    if root_str in sys.path:
        sys.path.remove(root_str)
    sys.path.insert(0, root_str)

import streamlit as st
import importlib
import importlib.util

def _load_local_app():
    app_path = (ROOT / 'app.py').resolve()
    spec = importlib.util.spec_from_file_location('app', app_path)
    if spec is None or spec.loader is None:
        raise ImportError(f'Cannot load app.py from {app_path}')
    module = importlib.util.module_from_spec(spec)
    sys.modules['app'] = module
    spec.loader.exec_module(module)
    return module

try:
    import app as _app
    _app_file = getattr(_app, '__file__', '')
    if not _app_file or Path(_app_file).resolve() != (ROOT / 'app.py').resolve():
        _app = _load_local_app()
except Exception:
    _app = _load_local_app()

for _name in dir(_app):
    if not _name.startswith('__'):
        globals()[_name] = getattr(_app, _name)

APP_TITLE = getattr(_app, 'APP_TITLE', 'PDF & Image Tools')
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



