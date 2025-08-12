import streamlit as st
from pathlib import Path
import base64

st.set_page_config(layout="wide", page_title="Webcam + Live Frame (HTML overlay)")

st.title("📸 Webcam dengan Frame")

# --- load frame png dari repo dan ubah jadi data URL (base64) ---
FRAME_PATH = Path("Design Frame") / "birthday_frame.png"  # ubah nama file kalau perlu
if not FRAME_PATH.exists():
    st.error(f"Frame tidak ditemukan di: {FRAME_PATH}. Pastikan path dan nama file benar.")
    st.stop()

with open(FRAME_PATH, "rb") as f:
    frame_bytes = f.read()
frame_b64 = base64.b64encode(frame_bytes).decode("utf-8")
frame_data_url = f"data:image/png;base64,{frame_b64}"

# --- ukuran preview yang kita inginkan (sesuaikan dengan ukuran frame PNG) ---
# gunakan ukuran frame asli agar overlay pas. Jika frame besar, sesuaikan max-width/html css.
# Kita akan membaca ukuran dari image via JS, tapi kita juga bisa menetapkan default styling.
# Untuk performa, kita batasi display max-width agar pas di layar.
html_code = f"""
<!doctype html>
<html>
  <head>
    <meta charset="utf-8"/>
    <style>
      .wrap {{
        display:flex;
        flex-direction:column;
        align-items:center;
        justify-content:center;
        gap:12px;
      }}
      #videoContainer {{
        position: relative;
        display:inline-block;
        /* ubah max-width sesuai kebutuhan; kita tetap menjaga aspect */
        max-width: 1280px;
        width: 100%;
      }}
      video {{
        width:100%;
        height:auto;
        -webkit-transform: scaleX(-1);
        transform: scaleX(-1); /* mirror preview */
      }}
      #overlayImg {{
        position:absolute;
        left:0;
        top:0;
        width:100%;
        height:100%;
        pointer-events:none; /* biar klik jatuh ke tombol & video */
        image-rendering: optimizeQuality;
      }}
      #controls {{
        display:flex;
        gap:10px;
        justify-content:center;
        margin-top:6px;
      }}
      button {{
        padding:10px 18px;
        font-size:16px;
        border-radius:8px;
        border: none;
        background:#ff7ab6;
        color:white;
        cursor:pointer;
      }}
      button:active {{ transform: translateY(1px); }}
      #resultImg {{
        max-width:100%;
        height:auto;
        border: 4px solid #eee;
      }}
      .hint {{ color: #666; font-size: 14px; }}
    </style>
  </head>
  <body>
    <div class="wrap">
      <div id="videoContainer">
        <video id="video" autoplay playsinline></video>
        <img id="overlayImg" src="{frame_data_url}" />
      </div>

      <div id="controls">
        <button id="btnCapture">📷 Ambil Foto</button>
        <button id="btnRetry" style="background:#6c757d">🔄 Foto Ulang</button>
      </div>

      <div class="hint">Jika diminta, klik <strong>Allow</strong> untuk akses kamera. Preview sudah mirror agar hasil sama.</div>

      <div id="output" style="margin-top:14px; text-align:center;">
        <img id="resultImg" style="display:none"/>
        <div id="downloadArea"></div>
      </div>
    </div>

    <script>
      const video = document.getElementById('video');
      const overlay = document.getElementById('overlayImg');
      const btnCapture = document.getElementById('btnCapture');
      const btnRetry = document.getElementById('btnRetry');
      const resultImg = document.getElementById('resultImg');
      const downloadArea = document.getElementById('downloadArea');

      // start webcam
      async function startCamera() {{
        try {{
          const stream = await navigator.mediaDevices.getUserMedia({{ video: true, audio: false }});
          video.srcObject = stream;
          video.play();
          return true;
        }} catch (e) {{
          alert('Gagal mengaktifkan kamera: ' + e.message);
          return false;
        }}
      }}

      // ketika ukuran video berubah (loadedmetadata), sesuaikan overlay element dimensi
      video.addEventListener('loadedmetadata', () => {{
        // overlay element sudah width:100% height:100% jadi dia mengikuti container
        // nothing else required here, but we keep event in case
      }});

      // capture function: draw mirrored video + overlay to canvas
      function captureImage() {{
        // buat canvas sesuai ukuran natural video (w/h)
        const vw = video.videoWidth;
        const vh = video.videoHeight;
        if (!vw || !vh) {{
          alert('Video belum siap, tunggu sebentar lalu coba lagi.');
          return null;
        }}

        // canvas ukuran video
        const canvas = document.createElement('canvas');
        canvas.width = vw;
        canvas.height = vh;
        const ctx = canvas.getContext('2d');

        // mirror horizontally -> translate + scale
        ctx.translate(canvas.width, 0);
        ctx.scale(-1, 1);

        // draw video frame
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        // draw overlay image on top (overlay is data URL)
        const overlayImg = new Image();
        overlayImg.src = overlay.src;
        return new Promise((resolve) => {{
          overlayImg.onload = () => {{
            // overlay image might have same aspect as canvas; draw covering full
            ctx.drawImage(overlayImg, 0, 0, canvas.width, canvas.height);

            // toDataURL
            const dataURL = canvas.toDataURL('image/png');
            resolve(dataURL);
          }};
          overlayImg.onerror = () => {{
            // fallback: resolve video only
            const dataURL = canvas.toDataURL('image/png');
            resolve(dataURL);
          }};
        }});
      }}

      btnCapture.addEventListener('click', async () => {{
        btnCapture.disabled = true;
        btnCapture.innerText = 'Memproses...';
        const dataURL = await captureImage();
        if (!dataURL) {{
          alert('Gagal membuat foto.');
          btnCapture.disabled = false;
          btnCapture.innerText = '📷 Ambil Foto';
          return;
        }}

        // tampilkan hasil di element <img>
        resultImg.src = dataURL;
        resultImg.style.display = 'block';

        // buat tombol download
        downloadArea.innerHTML = '';
        const a = document.createElement('a');
        a.href = dataURL;
        a.download = 'foto_' + Date.now() + '.png';
        a.innerText = '⬇ Download Foto';
        a.style = 'display:inline-block;padding:10px 18px;border-radius:8px;background:#28a745;color:white;text-decoration:none;margin-top:8px;';
        downloadArea.appendChild(a);

        // enable retry
        btnRetry.disabled = false;
        btnCapture.disabled = false;
        btnCapture.innerText = '📷 Ambil Foto';
      }});

      btnRetry.addEventListener('click', () => {{
        // clear result & download
        resultImg.style.display = 'none';
        resultImg.src = '';
        downloadArea.innerHTML = '';
      }});

      // init camera on load
      startCamera();
    </script>
  </body>
</html>
"""

# embed HTML di Streamlit
st.components.v1.html(html_code, height=820, scrolling=True)



