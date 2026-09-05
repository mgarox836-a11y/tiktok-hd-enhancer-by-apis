import streamlit as st
import os
import sys

# Konfigurasi Halaman Web
st.set_page_config(
    page_title="TikTok HD Enhancer — Buatan Apis",
    page_icon="✨",
    layout="centered"
)

# Injection CSS & Font Custom (Fix Layering & Overlap)
st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">

    <style>
        * {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
            user-select: none;
        }

        /* --- BACKGROUND & CONTAINER RESET --- */
        .stApp {
            background: #eef2f7 !important;
            overflow-x: hidden;
        }

        #MainMenu, header, footer {visibility: hidden;}
        .stDeployButton {display:none;}
        div[data-testid="stDecoration"] {display:none;}

        /* --- ANIMATION LAYER (Dipindah ke Paling Belakang) --- */
        .ambient-background {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: 0 !important; /* Di belakang konten */
            overflow: hidden;
            pointer-events: none;
        }

        .ambient-light {
            position: absolute;
            border-radius: 50%;
            filter: blur(90px);
            opacity: 0.5;
            animation: pulseLight 12s infinite alternate ease-in-out;
        }

        .light-1 {
            width: 500px; height: 500px;
            background: radial-gradient(circle, rgba(254, 44, 85, 0.3) 0%, rgba(255, 255, 255, 0) 70%);
            top: -100px; right: -80px;
        }

        .light-2 {
            width: 550px; height: 550px;
            background: radial-gradient(circle, rgba(37, 244, 238, 0.25) 0%, rgba(255, 255, 255, 0) 70%);
            bottom: -150px; left: -120px;
            animation-delay: -4s;
        }

        @keyframes pulseLight {
            0% { transform: scale(1) translate(0, 0); }
            50% { transform: scale(1.1) translate(15px, -15px); }
            100% { transform: scale(0.95) translate(-15px, 15px); }
        }

        /* 3D Glass Orbs (Di Belakang Card) */
        .orb {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.5);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.05);
            animation: floatOrb 14s infinite ease-in-out;
            z-index: 0 !important;
        }

        .orb-1 { width: 130px; height: 130px; top: 12%; left: 5%; animation-delay: 0s; }
        .orb-2 { width: 180px; height: 180px; bottom: 8%; right: 5%; animation-delay: -5s; }

        @keyframes floatOrb {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-25px) rotate(10deg); }
        }

        /* --- MAIN GLASS CARD --- */
        .block-container {
            max-width: 480px !important;
            padding: 36px 32px !important;
            background: rgba(255, 255, 255, 0.65) !important;
            border-radius: 32px !important;
            position: relative !important;
            z-index: 10 !important; /* Mengunci konten di atas animasi */
            backdrop-filter: blur(25px) !important;
            -webkit-backdrop-filter: blur(25px) !important;
            border: 1px solid rgba(255, 255, 255, 0.9) !important;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.06) !important;
            margin-top: 2rem !important;
            margin-bottom: 2rem !important;
        }

        /* --- AUTHOR BADGE --- */
        .badge-wrapper {
            text-align: center;
            margin-bottom: 16px;
        }

        .author-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 6px 14px;
            background: rgba(255, 255, 255, 0.8);
            border: 1px solid rgba(0, 0, 0, 0.06);
            border-radius: 30px;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 1.2px;
            text-transform: uppercase;
            color: #111;
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

        /* --- TITLE & SUBTITLE FIX --- */
        .main-title {
            text-align: center;
            font-size: 34px !important;
            font-weight: 800 !important;
            letter-spacing: -0.8px;
            color: #111111 !important;
            margin-bottom: 6px !important;
            line-height: 1.1;
        }

        .subtitle {
            text-align: center;
            font-size: 13px;
            color: #555555 !important;
            margin-bottom: 24px;
            font-weight: 500;
            line-height: 1.4;
        }

        /* --- FILE UPLOADER CLEAN FIX --- */
        div[data-testid="stFileUploader"] {
            border: 2px dashed rgba(0, 0, 0, 0.15) !important;
            border-radius: 20px !important;
            padding: 8px !important;
            background: rgba(255, 255, 255, 0.4) !important;
        }
        div[data-testid="stFileUploader"] section {
            background: transparent !important;
        }
        div[data-testid="stFileUploader"] label {
            color: #222222 !important;
            font-size: 13px !important;
            font-weight: 600 !important;
            text-align: center !important;
            display: block !important;
        }

        /* --- BUTTON STYLING --- */
        div.stButton > button, div.stDownloadButton > button {
            width: 100% !important;
            margin-top: 12px !important;
            padding: 14px !important;
            border: none !important;
            border-radius: 16px !important;
            background: #111111 !important;
            color: #ffffff !important;
            font-size: 13px !important;
            font-weight: 700 !important;
            letter-spacing: 1px !important;
            text-transform: uppercase !important;
            cursor: pointer !important;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12) !important;
            transition: all 0.2s ease !important;
        }

        div.stButton > button:hover, div.stDownloadButton > button:hover {
            background: #000000 !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 12px 25px rgba(0, 0, 0, 0.2) !important;
        }

        /* --- FOOTER GLASS --- */
        .card-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 24px;
            padding-top: 16px;
            border-top: 1px solid rgba(0, 0, 0, 0.08);
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 1px;
            text-transform: uppercase;
            color: #888888;
        }
    </style>

    <!-- Layer Animasi Background -->
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

# 2. Title & Subtitle
st.markdown('<div class="main-title">TikTok Quality</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Bypass kompresi TikTok ke 1080p 60FPS<br>tanpa re-encoding</div>', unsafe_allow_html=True)

# 3. File Uploader Form
uploaded_file = st.file_uploader("✦ Klik atau seret file .MP4 ke sini", type=["mp4", "mov"])

if uploaded_file is not None:
    if os.path.exists("temp_output.mp4"):
        os.remove("temp_output.mp4")

    with open("temp_input.mp4", "wb") as f:
        f.write(uploaded_file.getbuffer())

    if st.button("PROSES VIDEO"):
        with st.spinner("Memproses video... Mohon tunggu sebentar."):
            os.system(f'"{sys.executable}" -m tiktok_quality temp_input.mp4 temp_output.mp4')
        
        if os.path.exists("temp_output.mp4") and os.path.getsize("temp_output.mp4") > 0:
            st.success("✨ Selesai! Video HD siap diunduh.")
            st.video("temp_output.mp4")
            
            with open("temp_output.mp4", "rb") as file:
                st.download_button(
                    label="UNDUH VIDEO HD",
                    data=file,
                    file_name="HD_enhanced.mp4",
                    mime="video/mp4"
                )
        else:
            st.error("❌ Gagal memproses video. Coba file MP4 lainnya.")

# 4. Footer Glass
st.markdown("""
    <div class="card-footer">
        <span>By Apis</span>
        <span>•</span>
        <span>60 FPS Unlock</span>
    </div>
""", unsafe_allow_html=True)