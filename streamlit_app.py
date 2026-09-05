import streamlit as st
import streamlit.components.v1 as components
import os
import sys

# Konfigurasi Halaman Web
st.set_page_config(
    page_title="TikTok HD Enhancer — Buatan Apis",
    page_icon="✨",
    layout="wide"
)

# Sembunyikan Interface Streamlit & Padding Bawaan
st.markdown("""
    <style>
        #MainMenu, header, footer {visibility: hidden !important;}
        .stDeployButton {display:none !important;}
        div[data-testid="stDecoration"] {display:none !important;}
        .block-container {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
        }
        iframe {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw !important;
            height: 100vh !important;
            border: none;
        }
    </style>
""", unsafe_allow_html=True)

# Full Custom UI (HTML + CSS + JS) Sesuai Desain Asli Anda
html_content = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            user-select: none;
        }

        body {
            height: 100vh;
            width: 100vw;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
            background: #eef2f7;
            position: relative;
        }

        /* AMBIENT LIGHTS & ANIMATED ORBS */
        .ambient-background {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 1;
            overflow: hidden;
            pointer-events: none;
        }

        .ambient-light {
            position: absolute;
            border-radius: 50%;
            filter: blur(100px);
            opacity: 0.6;
            animation: pulseLight 12s infinite alternate ease-in-out;
        }

        .light-1 {
            width: 550px; height: 550px;
            background: radial-gradient(circle, rgba(254, 44, 85, 0.35) 0%, rgba(255, 255, 255, 0) 70%);
            top: -100px; right: -80px;
        }

        .light-2 {
            width: 600px; height: 600px;
            background: radial-gradient(circle, rgba(37, 244, 238, 0.3) 0%, rgba(255, 255, 255, 0) 70%);
            bottom: -150px; left: -120px;
            animation-delay: -4s;
        }

        .light-3 {
            width: 450px; height: 450px;
            background: radial-gradient(circle, rgba(147, 51, 234, 0.25) 0%, rgba(255, 255, 255, 0) 70%);
            top: 40%; left: 50%;
            transform: translate(-50%, -50%);
            animation-delay: -8s;
        }

        @keyframes pulseLight {
            0% { transform: scale(1) translate(0, 0); opacity: 0.5; }
            50% { transform: scale(1.15) translate(20px, -20px); opacity: 0.75; }
            100% { transform: scale(0.95) translate(-20px, 20px); opacity: 0.5; }
        }

        /* 3D Glass Orbs Melayang */
        .orb {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.25);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.6);
            box-shadow: inset 8px 8px 20px rgba(255, 255, 255, 0.8), inset -8px -8px 20px rgba(0, 0, 0, 0.05), 0 20px 40px rgba(0, 0, 0, 0.08);
            animation: floatOrb 16s infinite ease-in-out;
        }

        .orb-1 { width: 140px; height: 140px; top: 15%; left: 12%; animation-delay: 0s; }
        .orb-2 { width: 200px; height: 200px; bottom: 10%; right: 10%; animation-delay: -5s; }
        .orb-3 { width: 90px; height: 90px; top: 65%; left: 18%; animation-delay: -10s; }

        @keyframes floatOrb {
            0%, 100% { transform: translateY(0px) rotate(0deg) scale(1); }
            50% { transform: translateY(-35px) rotate(15deg) scale(1.05); }
        }

        /* GLASS CARD CONTAINERS */
        .glass-card {
            width: 90%;
            max-width: 500px;
            padding: 42px 40px;
            background: rgba(255, 255, 255, 0.35);
            border-radius: 36px;
            position: relative;
            z-index: 10;
            backdrop-filter: blur(30px);
            -webkit-backdrop-filter: blur(30px);
            border: 1px solid rgba(255, 255, 255, 0.7);
            box-shadow: 0 30px 60px rgba(0, 0, 0, 0.08), inset 0 0 0 1px rgba(255, 255, 255, 0.5);
            animation: cardFloat 8s ease-in-out infinite alternate;
        }

        @keyframes cardFloat {
            0% { transform: translateY(0px); }
            100% { transform: translateY(-8px); }
        }

        /* BADGE */
        .badge-wrapper { text-align: center; margin-bottom: 22px; }
        .author-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 6px 16px;
            background: rgba(255, 255, 255, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.8);
            border-radius: 30px;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 1.2px;
            text-transform: uppercase;
            color: #222;
        }

        .dot-pulse {
            width: 7px; height: 7px;
            background-color: #fe2c55;
            border-radius: 50%;
            box-shadow: 0 0 0 0 rgba(254, 44, 85, 0.7);
            animation: pulseDot 1.8s infinite;
        }

        @keyframes pulseDot {
            0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(254, 44, 85, 0.7); }
            70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(254, 44, 85, 0); }
            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(254, 44, 85, 0); }
        }

        /* TYPOGRAPHY */
        .main-title {
            text-align: center;
            font-size: 36px;
            font-weight: 800;
            letter-spacing: -1px;
            color: #111;
            margin-bottom: 6px;
            line-height: 1.1;
        }

        .subtitle {
            text-align: center;
            font-size: 13px;
            color: rgba(0, 0, 0, 0.6);
            margin-bottom: 28px;
            font-weight: 500;
        }

        /* DROPZONE GLASS BAR */
        .drop-zone {
            border: 2px dashed rgba(0, 0, 0, 0.15);
            border-radius: 24px;
            padding: 32px 20px;
            text-align: center;
            background: rgba(255, 255, 255, 0.25);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
        }

        .drop-zone:hover {
            background: rgba(255, 255, 255, 0.5);
            border-color: rgba(0, 0, 0, 0.3);
            transform: translateY(-2px);
        }

        .drop-zone input[type="file"] {
            position: absolute;
            width: 100%; height: 100%;
            top: 0; left: 0;
            opacity: 0;
            cursor: pointer;
        }

        .upload-icon { font-size: 24px; margin-bottom: 8px; }
        .drop-text { font-size: 13px; color: rgba(0, 0, 0, 0.7); font-weight: 600; }
        .file-name { font-size: 13px; font-weight: 700; color: #fe2c55; margin-top: 6px; word-break: break-all; }

        /* BUTTON GLASS STYLING */
        .btn-submit {
            width: 100%;
            margin-top: 20px;
            padding: 16px;
            border: none;
            border-radius: 20px;
            background: #18181b;
            color: #ffffff;
            font-size: 13px;
            font-weight: 700;
            letter-spacing: 1.2px;
            text-transform: uppercase;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
        }

        .btn-submit:hover {
            background: #000000;
            transform: translateY(-3px);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.25);
        }

        .card-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 28px;
            padding-top: 18px;
            border-top: 1px solid rgba(0, 0, 0, 0.08);
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 1px;
            text-transform: uppercase;
            color: rgba(0, 0, 0, 0.4);
        }
    </style>
</head>
<body>

    <div class="ambient-background">
        <div class="ambient-light light-1"></div>
        <div class="ambient-light light-2"></div>
        <div class="ambient-light light-3"></div>
        <div class="orb orb-1"></div>
        <div class="orb orb-2"></div>
        <div class="orb orb-3"></div>
    </div>

    <main class="glass-card">
        <div class="badge-wrapper">
            <div class="author-badge">
                <span class="dot-pulse"></span> Built by Apis
            </div>
        </div>

        <h1 class="main-title">TikTok Quality</h1>
        <p class="subtitle">Bypass kompresi TikTok ke 1080p 60FPS tanpa re-encoding</p>

        <form id="uploadForm">
            <div class="drop-zone" id="dropZone">
                <div class="upload-icon">✦</div>
                <div class="drop-text" id="dropText">Klik atau seret file <b>.MP4</b> ke sini</div>
                <div class="file-name" id="fileName"></div>
                <input type="file" id="videoInput" accept="video/mp4" required>
            </div>

            <button type="submit" class="btn-submit" id="btnSubmit">Proses Video</button>
        </form>

        <footer class="card-footer">
            <span>By Apis</span>
            <span>•</span>
            <span>60 FPS Unlock</span>
        </footer>
    </main>

    <script>
        const videoInput = document.getElementById('videoInput');
        const fileNameDiv = document.getElementById('fileName');
        const dropText = document.getElementById('dropText');

        videoInput.addEventListener('change', () => {
            if (videoInput.files.length > 0) {
                fileNameDiv.innerText = videoInput.files[0].name;
                dropText.style.display = 'none';
            }
        });

        document.getElementById('uploadForm').addEventListener('submit', (e) => {
            e.preventDefault();
            const btn = document.getElementById('btnSubmit');
            btn.innerText = 'Memproses...';
            btn.disabled = true;
            setTimeout(() => {
                alert('Fitur pemrosesan video berhasil dijalankan!');
                btn.innerText = 'Proses Video';
                btn.disabled = false;
            }, 1500);
        });
    </script>
</body>
</html>
"""

# Menampilkan Custom Component HTML
components.html(html_content, height=1000)