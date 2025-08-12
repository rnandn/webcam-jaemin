import streamlit as st
from pathlib import Path
import base64

st.set_page_config(layout="wide", page_title="Webcam + Live Frame (HTML overlay)")

st.title("📸 Webcam dengan Frame")

# --- load frame png ---
FRAME_PATH = Path("Design Frame") / "birthday_frame.png"
if not FRAME_PATH.exists():
    st.error(f"Frame tidak ditemukan di: {FRAME_PATH}. Pastikan path dan nama file benar.")
    st.stop()

with open(FRAME_PATH, "rb") as f:
    frame_bytes = f.read()
frame_b64 = base64.b64encode(frame_bytes).decode("utf-8")
frame_data_url = f"data:image/png;base64,{frame_b64}"

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
        max-width: 1280px;
        width: 100%;
        aspect-ratio: 16/9;
      }}
      video {{
        width:100%;
        height:auto;
        -webkit-transform: scaleX(-1);
        transform: scaleX(-1);
      }}
      #overlayImg {{
        position:absolute;
        left:0;
        top:0;
        width:100%;
        height:100%;
        pointer-events:none;
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

      <div class="hint">Jika diminta, klik <strong>Allow</strong> untuk akses kamera.</div>

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

      function captureImage() {{
        const vw = video.videoWidth;
        const vh = video.videoHeight;
        if (!vw || !vh) {{
          alert('Video belum siap, tunggu sebentar lalu coba lagi.');
          return null;
        }}

        const fw = overlay.naturalWidth;
        const fh = overlay.naturalHeight;

        const canvas = document.createElement('canvas');
        canvas.width = fw;
        canvas.height = fh;
        const ctx = canvas.getContext('2d');

        const scale = Math.max(fw / vw, fh / vh);
        const drawW = vw * scale;
        const drawH = vh * scale;
        const offsetX = (fw - drawW) / 2;
        const offsetY = (fh - drawH) / 2;

        ctx.save();
        ctx.translate(fw, 0);
        ctx.scale(-1, 1);
        ctx.drawImage(video, -offsetX, offsetY, drawW, drawH);
        ctx.restore();

        ctx.drawImage(overlay, 0, 0, fw, fh);

        const dataURL = canvas.toDataURL('image/png');
        return dataURL;
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
        resultImg.src = dataURL;
        resultImg.style.display = 'block';

        downloadArea.innerHTML = '';
        const a = document.createElement('a');
        a.href = dataURL;
        a.download = 'foto_' + Date.now() + '.png';
        a.innerText = '⬇ Download Foto';
        a.style = 'display:inline-block;padding:10px 18px;border-radius:8px;background:#28a745;color:white;text-decoration:none;margin-top:8px;';
        downloadArea.appendChild(a);

        btnRetry.disabled = false;
        btnCapture.disabled = false;
        btnCapture.innerText = '📷 Ambil Foto';
      }});

      btnRetry.addEventListener('click', () => {{
        resultImg.style.display = 'none';
        resultImg.src = '';
        downloadArea.innerHTML = '';
      }});

      startCamera();
    </script>
  </body>
</html>
"""

st.components.v1.html(html_code, height=820, scrolling=True)
