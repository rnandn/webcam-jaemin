import streamlit as st

st.set_page_config(layout="centered")

# CSS custom
#birthday
st.markdown(
    f"""
    <style>
    .pilih-frame {{
        position: relative;
        width: 1280px;
        height: 720px;
        background-image: url('https://i.imgur.com/ZwZ3397.png'); 
        background-size: cover;
        margin: 0 auto;
    }}
    .btn1 {{
        position: absolute;
        left: {113.7}px;
        top: {408.2}px;
        width: {181.9}px;
        height: {58}px;
        background-color: rgba(255,255,255,0); 
        border: none;
        cursor: pointer;
    }}
    .btn2 {{
        position: absolute;
        left: {564.1}px;
        top: {407.2}px;
        width: {182.4}px;
        height: {58.9}px;
        background-color: rgba(255,255,255,0); 
        border: none;
        cursor: pointer;
    }}
    .btn3 {{
        position: absolute;
        left: {996.8}px;
        top: {408.2}px;
        width: {182.4}px;
        height: {58}px;
        background-color: rgba(255,255,255,0); 
        border: none;
        cursor: pointer;
    }}
    .btn4 {{
        position: absolute;
        left: {324.1}px;
        top: {663}px;
        width: {182.4}px;
        height: {58}px;
        background-color: rgba(255,255,255,0); 
        border: none;
        cursor: pointer;
    }}
    .btn5 {{
        position: absolute;
        left: {809.8}px;
        top: {662.1}px;
        width: {182.4}px;
        height: {58.9}px;
        background-color: rgba(255,255,255,0); 
        border: none;
        cursor: pointer;
    }}
    .btn6 {{
        position: absolute;
        left: {6.3}px;
        top: {663}px;
        width: {160.8}px;
        height: {50.8}px;
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
<div class="pilih-frame">
    <form action="/webcam1" method="get">
        <button class="btn1" type="submit"></button>
    </form>
    <form action="/webcam2" method="get">
        <button class="btn2" type="submit"></button>
    </form>
    <form action="/webcam3" method="get">
        <button class="btn3" type="submit"></button>
    </form>
    <form action="/webcam4" method="get">
        <button class="btn4" type="submit"></button>
    </form>
    <form action="/webcam5" method="get">
        <button class="btn5" type="submit"></button>
    </form>
    <form action="/" method="get">
        <button class="btn6" type="submit"></button>
    </form>
</div>
"""

st.markdown(button_html, unsafe_allow_html=True)