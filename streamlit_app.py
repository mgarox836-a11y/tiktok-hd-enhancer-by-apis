import streamlit as st
import os
import sys

# Konfigurasi Halaman Web
st.set_page_config(
    page_title="TikTok HD Enhancer — Buatan Apis",
    page_icon="✨",
    layout="centered"
)

# Menyarutkan Seluruh CSS Animasi, Font, dan Styling Kustom
st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">

    <style>
        * {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
            user-select: none;
        }

        /* --- BACKGROUND ANIMATED SHAPES & AMBIENT --- */
        .stApp {
            background: #eef2f7 !important;
            overflow-x: hidden;
        }

        /* Sembunyikan Header & Footer Bawaan Streamlit */
        #MainMenu, header, footer {visibility: hidden;}
        .stDeployButton {display:none;}
        div[data-testid="stDecoration"] {display:none;}

        .ambient-background {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: 0;
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
            width: 550px;
            height: 550px;
            background: radial-gradient(circle, rgba(254, 44, 85, 0.35) 0%, rgba(255, 255, 255, 0) 70%);
            top: -100px;
            right: -80px;
        }

        .light-2 {
            width: 600px;
            height: 600px;
            background: radial-gradient(circle, rgba(37, 244, 238, 0.3) 0%, rgba(255, 255, 255, 0) 70%);
            bottom: -150px;
            left: -120px;
            animation-delay: -4s;
        }

        .light-3 {
            width: 450px;
            height: 450px;
            background: radial-gradient(circle, rgba(147, 51, 234, 0.25) 0%, rgba(255, 255, 255, 0) 70%);
            top: 40%;
            left: 50%;
            transform: translate(-50%, -50%);
            animation-delay: -8s;
        }

        @keyframes pulseLight {
            0% { transform: scale(1) translate(0, 0); opacity: 0.5; }
            50% { transform: scale(1.15) translate(20px, -20px); opacity: 0.75; }
            100% { transform: scale(0.95) translate(-20px, 20px); opacity: 0.5; }
        }

        /* 3D Glass Orbs (Bulatan 3D Melayang) */
        .orb {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.25);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.6);
            box-shadow: 
                inset 8px 8px 20px rgba(255, 255, 255, 0.8),
                inset -8px -8px 20px rgba(0, 0, 0, 0.05),
                0 20px 40px rgba(0, 0, 0, 0.08);
            animation: floatOrb 16s infinite ease-in-out;
        }

        .orb-1 { width: 140px; height: 140px; top: 15%; left: 8%; animation-delay: 0s; }
        .orb-2 { width: 200px; height: 200px; bottom: 10%; right: 8%; animation-delay: -5s; }
        .orb-3 { width: 90px; height: 90px; top: 65%; left: 12%; animation-delay: -10s; }

        @keyframes floatOrb {
            0%, 100% { transform: translateY(0px) rotate(0deg) scale(1); }
            50% { transform: translateY(-35px) rotate(15deg) scale(1.05); }
        }

        /* --- MAIN GLASS CARD CONTAINER --- */
        .block-container {
            max-width: 520px !important;
            padding: 42px 40px !important;
            background: rgba(255, 255, 255, 0.35) !important;
            border-radius: 36px !important;
            position: relative;
            z-index: 10;
            backdrop-filter: blur(30px) !important;
            -webkit-backdrop-filter: blur(30px) !important;
            border: 1px solid rgba(255, 255, 255, 0.7) !important;
            box-shadow: 0 30px 60px rgba(0, 0, 0, 0.08), inset 0 0 0 1px rgba(255, 255, 255, 0.5) !important;
            margin-top: 3rem !important;
            margin-bottom: 3rem !important;
            animation: cardFloat 8s ease-in-out infinite alternate;
        }

        @keyframes cardFloat {
            0% { transform: translateY(0px); }
            100% { transform: translateY(-8px); }
        }

        /* --- AUTHOR BADGE --- */
        .badge-wrapper {
            text-align: center;
            margin-bottom: 22px;
        }

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
            box-shadow: 0 4px 15px rgba(0,0,0,0.03);
            transition: all 0.3s ease;
        }

        .dot-pulse {
            width: 7px;
            height: 7px;
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

        /* --- TITLE & SUBTITLE --- */
        .main-title {
            text-align: center;
            font-size: 36px;
            font-weight: 700;
            letter-spacing: -1px;
            color: #111;
            margin-bottom: 6px;
            line-height: 1.1;
        }

        .subtitle {
            text-align: center;
            font-size: 13px;
            color: rgba(0, 0, 0, 0.55);
            letter-spacing: 0.1px;
            margin-bottom: 30px;
            font-weight: 400;
        }

        /* --- UPLOADER STYLING --- */
        div[data-testid="stFileUploader"] {
            border: 2px dashed rgba(0, 0, 0, 0.12) !important;
            border-radius: 24px !important;
            padding: 10px !important;
            background: rgba(255, 255, 255, 0.25) !important;
            backdrop-filter: blur(10px) !important;
        }
        div[data-testid="stFileUploader"] label {
            color: rgba(0, 0, 0, 0.7) !important;
            font-size: 13px !important;
            font-weight: 600 !important;
        }

        /* --- ANIMATED GLASS BUTTON --- */
        div.stButton > button, div.stDownloadButton > button {
            width: 100% !important;
            margin-top: 15px !important;
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
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        }

        div.stButton > button:hover, div.stDownloadButton > button:hover {
            transform: translateY(-4px) scale(1.02) !important;
            background: #000000 !important;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.25) !important;
        }

        /* --- FOOTER GLASS --- */
        .card-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 30px;
            padding-top: 18px;
            border-top: 1px solid rgba(0, 0, 0, 0.06);
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 1px;
            text-transform: uppercase;
            color: rgba(0, 0, 0, 0.4);
        }
    </style>

    <!-- Latar Belakang Beranimasi HTML -->
    <div class="ambient-background">
        <div class="ambient-light light-1"></div>
        <div class="ambient-light light-2"></div>
        <div class="ambient-light light-3"></div>
        <div class="orb orb-1"></div>
        <div class="orb orb-2"></div>
        <div class="orb orb-3"></div>
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
st.markdown('<h1 class="main-title">TikTok Quality</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Bypass kompresi TikTok ke 1080p 60FPS tanpa re-encoding</p>', unsafe_allow_html=True)

# 3. File Uploader Form
uploaded_file = st.file_uploader("✦ Klik atau seret file .MP4 ke sini", type=["mp4", "mov"])

if uploaded_file is not None:
    if os.path.exists("temp_output.mp4"):
        os.remove("temp_output.mp4")

    with open("temp_input.mp4", "wb") as f:
        f.write(uploaded_file.getbuffer())

    if st.button("PROSES VIDEO"):
        with st.spinner("Processing metadata... Mohon tunggu sebentar."):
            os.system(f'"{sys.executable}" -m tiktok_quality temp_input.mp4 temp_output.mp4')
        
        if os.path.exists("temp_output.mp4") and os.path.getsize("temp_output.mp4") > 0:
            st.success("✨ Selesai! Video HD otomatis siap diunduh.")
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