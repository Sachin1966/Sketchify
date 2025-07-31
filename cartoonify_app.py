import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

st.set_page_config(
    page_title="Sketch Generator",
    page_icon="✏️",
    layout="centered"
)

st.markdown("""
    <h1 style='text-align: center;'>🖌️ Sketch Generator</h1>
    <p style='text-align: center;'>Turn your photo into a pencil sketch </p>
    <hr>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("Settings")
    uploaded_file = st.file_uploader("📄 Upload an image", type=["jpg", "jpeg", "png"])
    blur_value = st.slider("🎚️ Sketch Blur Intensity", 3, 101, step=2, value=21)
    name_text = st.text_input(" Enter name to print on sketch", "")

def convert_to_sketch(image, blur_ksize=21):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    inv_gray = 255 - gray
    blur = cv2.GaussianBlur(inv_gray, (blur_ksize, blur_ksize), 0)
    sketch = cv2.divide(gray, 255 - blur, scale=256)
    return sketch

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    image_np = np.array(image)
    image_cv2 = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    sketch = convert_to_sketch(image_cv2, blur_ksize=blur_value)

    if name_text.strip():
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        font_thickness = 2
        color = (0,)  # Black in grayscale
        text_size = cv2.getTextSize(name_text, font, font_scale, font_thickness)[0]
        text_x = (sketch.shape[1] - text_size[0]) // 2
        text_y = sketch.shape[0] - 20  # 20 px from bottom
        cv2.putText(sketch, name_text, (text_x, text_y), font, font_scale, color, font_thickness, cv2.LINE_AA)

    sketch_rgb = cv2.cvtColor(sketch, cv2.COLOR_GRAY2RGB)  # for display

    col1, col2 = st.columns(2)
    with col1:
        st.image(image, caption="Original Image", use_container_width=True)
    with col2:
        st.image(sketch_rgb, caption="Pencil Sketch", use_container_width=True)

    buf = io.BytesIO()
    sketch_pil = Image.fromarray(sketch)
    sketch_pil.save(buf, format="PNG")
    st.download_button("⬇️ Download Sketch", buf.getvalue(), file_name="sketch.png", mime="image/png")

st.markdown("""
    <hr>
    <p style='text-align:center; font-size:14px;'>Made with ❤️ by Sachin..</p>
""", unsafe_allow_html=True)

