import streamlit as st
import cv2
from PIL import Image
import numpy as np
import os
from datetime import datetime
import io

st.title("📸 Webcam dengan Frame")

# Pilih frame PNG
frame_path = "Design Frame/autumn_frame.png"  
frame_image = Image.open(frame_path).convert("RGBA")

# Placeholder kamera
camera_placeholder = st.empty()

# State untuk simpan foto sementara
if "photo" not in st.session_state:
    st.session_state.photo = None

# Tombol ambil foto
take_photo = st.button("📷 Ambil Foto")

# Kalau belum ada foto, nyalakan kamera
if st.session_state.photo is None:
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            st.error("Tidak bisa mengakses kamera.")
            break

        # Mirror kamera
        frame = cv2.flip(frame, 1)

        # Convert ke RGBA dan resize
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_pil = Image.fromarray(frame_rgb).convert("RGBA")
        frame_pil = frame_pil.resize(frame_image.size)

        # Gabungkan frame kamera dan PNG
        combined = Image.alpha_composite(frame_pil, frame_image)

        camera_placeholder.image(combined, use_container_width=True)

        # Kalau tombol ambil foto ditekan
        if take_photo:
            st.session_state.photo = combined
            break

    cap.release()

# Kalau foto sudah diambil
if st.session_state.photo is not None:
    camera_placeholder.image(st.session_state.photo, use_container_width=True)

    # Simpan ke bytes untuk download
    img_bytes = io.BytesIO()
    st.session_state.photo.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    # Tombol download
    st.download_button(
        label="⬇ Download Foto",
        data=img_bytes,
        file_name=f"foto_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
        mime="image/png"
    )

    # Tombol foto ulang
    if st.button("🔄 Foto Ulang"):
        st.session_state.photo = None
        st.rerun()
