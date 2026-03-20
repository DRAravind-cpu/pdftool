import streamlit as st
from app import *

st.set_page_config(page_title=f"{APP_TITLE} - Meme generator", layout="wide")
if st.button("← Home"):
    st.switch_page("app.py")

st.title("Meme generator")

deps = get_dependency_status()

st.subheader("Meme generator")
st.caption("Add top/bottom text.")
f = st.file_uploader(
    "Image", type=["jpg", "jpeg", "png", "webp", "heic", "heif", "tif", "tiff", "bmp", "gif"], key="img_meme"
)
top = st.text_input("Top text", key="img_meme_top")
bottom = st.text_input("Bottom text", key="img_meme_bottom")
if f and st.button("Generate", key="img_meme_btn"):
    from PIL import ImageDraw, ImageFont

    img = pil_open_image(f).convert("RGB")
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    w, h = img.size

    def outline_text(x, y, t):
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                draw.text((x + dx, y + dy), t, font=font, fill=(0, 0, 0))
        draw.text((x, y), t, font=font, fill=(255, 255, 255))

    if top:
        outline_text(10, 10, top)
    if bottom:
        outline_text(10, h - 25, bottom)
    data = pil_to_bytes(img, "png")
    st.download_button(
        "Download",
        data,
        file_name=f"{Path(f.name).stem}-meme.png",
        mime="image/png",
    )

