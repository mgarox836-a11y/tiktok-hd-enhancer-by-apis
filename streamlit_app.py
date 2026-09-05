import streamlit as st
import os
import sys

# Konfigurasi Halaman Web
st.set_page_config(
    page_title="TikTok HD Enhancer — Buatan Apis",
    page_icon="✨",
    layout="centered"
)

# Injection CSS Kustom (Latar Belakang Animasi, Glassmorphism & Font)
st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">

    <style>
        * {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
            user-select: none;
        }

        /* Ambient Background & Body Reset */
        .stApp {
            background: #eef2f7 !important;
            overflow-x: hidden;
        }

        #MainMenu, header, footer {visibility: hidden !important;}
        .stDeployButton {display:none !important;}
        div[data-testid="stDecoration"] {display:none !important;}

        /* Latar Belakang Cahaya Melayang */
        .ambient-background {
            position: fixed;
            top: 0; left: 0;
            width: 100vw; height: 100vh;
            z-index: 0 !important;
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

        @keyframes pulseLight {
            0% { transform: scale(1) translate(0, 0); }
            50% { transform: scale(1.15) translate(20px, -20px); }
            100% { transform: scale(0.95) translate(-20px, 20px); }
        }

        /* 3D Glass Orbs */
        .orb {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.25);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.6);
            box-shadow: inset 8px 8px 20px rgba(255, 255, 255, 0.8), inset -8px -8px 20px rgba(0, 0, 0, 0.05), 0 20px 40px rgba(0, 0, 0, 0.08);
            animation: floatOrb 16s infinite ease-in-out;
            z-index: 0 !important;
        }

        .orb-1 { width: 140px; height: 140px; top: 15%; left: 8%; animation-delay: 0s; }
        .orb-2 { width: 200px; height: 200px; bottom: 10%; right: 8%; animation-delay: -5s; }

        @keyframes floatOrb {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-35px) rotate(15deg); }
        }

        /* Main Glass Card Container */
        .block-container {
            max-width: 500px !important;
            padding: 42px 40px !important;
            background: rgba(255, 255, 255, 0.35) !important;
            border-radius: 36px !important;
            position: relative !important;
            z-index: 10 !important;
            backdrop-filter: blur(30px) !important;
            -webkit-backdrop-filter: blur(30px) !important;
            border: 1px solid rgba(255, 255, 255, 0.7) !important;
            box-shadow: 0 30px 60px rgba(0, 0, 0, 0.08), inset 0 0 0 1px rgba(255, 255, 255, 0.5) !important;
            margin-top: 3rem !important;
            margin-bottom: 3rem !important;
        }

        /* Badge Built By Apis */
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

        /* Headings */
        .main-title {
            text-align: center;
            font-size: 36px !important;
            font-weight: 800 !important;
            letter-spacing: -1px;
            color: #111 !important;
            margin-bottom: 6px !important;
            line-height: 1.1;
        }

        .subtitle {
            text-align: center;
            font-size: 13px;
            color: rgba(0, 0, 0, 0.6);
            margin-bottom: 28px;
            font-weight: 500;
        }

        /* Custom Styling Uploader Bawaan agar Bersih */
        div[data-testid="stFileUploader"] {
            border: 2px dashed rgba(0, 0, 0, 0.15) !important;
            border-radius: 24px !important;
            padding: 16px !important;
            background: rgba(255, 255, 255, 0.25) !important;
            backdrop-filter: blur(10px) !important;
        }
        div[data-testid="stFileUploader"] section {
            background: transparent !important;
        }
        div[data-testid="stFileUploader"] label {
            color: rgba(0, 0, 0, 0.7) !important;
            font-size: 13px !important;
            font-weight: 600 !important;
        }

        /* Buttons Styling */
        div.stButton > button, div.stDownloadButton > button {
            width: 100% !important;
            margin-top: 18px !important;
            padding: 16px !important;
            border: none !important;
            border-radius: 20px !important;
            background: #18181b !important;
            color: #ffffff !important;
            font-size: 13px !important;
            font-weight: 700 !important;
            letter-spacing: 1.2px !important;
            text-transform: uppercase !important;
            cursor: pointer !important;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15) !important;
            transition: all 0.3s ease !important;
        }

        div.stButton > button:hover, div.stDownloadButton > button:hover {
            background: #000000 !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.25) !important;
        }

        /* Card Footer */
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

    <!-- Layer Background Animasi -->
    <div class="ambient-background">
        <div class="ambient-light light-1"></div>
        <div class="ambient-light light-2"></div>
        <div class="orb orb-1"></div>
        <div class="orb orb-2"></div>
    </div>
""", unsafe_allow_html=True)

# 1. Author Badge
st.markdown("""
    <div class="badge-wrapper">
        <div class="author-badge">
            <span class="dot-pulse"></span> Built by Apis
        </div>
    </div>
""", unsafe_allow_html=True)

# 2. Judul & Subtitle
st.markdown('<div class="main-title">TikTok Quality</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Bypass kompresi TikTok ke 1080p 60FPS tanpa re-encoding</div>', unsafe_allow_html=True)

# 3. Form File Uploader
uploaded_file = st.file_uploader("✦ Klik atau seret file .MP4 ke sini", type=["mp4", "mov"])

if uploaded_file is not None:
    if os.path.exists("temp_output.mp4"):
        os.remove("temp_output.mp4")

    with open("temp_input.mp4", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Tombol Jalankan Pemrosesan Real
    if st.button("PROSES VIDEO"):
        with st.spinner("Sedang memproses metadata video..."):
            # Jalankan skrip tiktok_quality bawaan Python
            res = os.system(f'"{sys.executable}" -m tiktok_quality temp_input.mp4 temp_output.mp4')

        if os.path.exists("temp_output.mp4") and os.path.getsize("temp_output.mp4") > 0:
            st.success("✨ Selesai! Video HD berhasil diproses.")
            st.video("temp_output.mp4")

            with open("temp_output.mp4", "rb") as file:
                st.download_button(
                    label="UNDUH VIDEO HD",
                    data=file,
                    file_name=f"HD_{uploaded_file.name}",
                    mime="video/mp4"
                )
        else:
            st.error("❌ Terjadi kesalahan saat memproses video. Pastikan format .MP4 valid.")

# 4. Footer Card
st.markdown("""
    <div class="card-footer">
        <span>By Apis</span>
        <span>•</span>
        <span>60 FPS Unlock</span>
    </div>
""", unsafe_allow_html=True)