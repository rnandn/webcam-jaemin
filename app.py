import streamlit as st

# Set halaman jadi lebar penuh
st.set_page_config(layout="wide")

# CSS custom
st.markdown(
    f"""
    <style>
    .start-container {{
        position: relative;
        width: 1280px;
        height: 720px;
        background-image: url('https://i.imgur.com/BAuBj1c.png'); 
        background-size: cover;
        margin: 0 auto;
    }}
    .start-btn {{
        position: absolute;
        left: {842.2}px;
        top: {417.7}px;
        width: {365.8}px;
        height: {115.4}px;
        background-color: rgba(255,255,255,0); 
        border: none;
        cursor: pointer;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# HTML tombol
button_html = f"""
<div class="start-container">
    <form action="/pilih_frame" method="get">
        <button class="start-btn" type="submit"></button>
    </form>
</div>
"""

st.markdown(button_html, unsafe_allow_html=True)
