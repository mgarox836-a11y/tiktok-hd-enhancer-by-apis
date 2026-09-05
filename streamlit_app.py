import streamlit as st
import os

# Import fungsi langsung dari library tiktok_quality
try:
    from tiktok_quality.transform import transform
except ImportError:
    transform = None

# Konfigurasi Halaman Web
st.set_page_config(
    page_title="TikTok HD Enhancer — Buatan Apis",
    page_icon="✨",
    layout="centered"
)

# Custom Styling & Glassmorphism Animation
st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">

    <style>
        * {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
            user-select: none;
        }

        .stApp {
            background: #eef2f7 !important;
            overflow-x: hidden;
        }

        #MainMenu, header, footer {visibility: hidden !important;}
        .stDeployButton {display:none !important;}
        div[data-testid="stDecoration"] {display:none !important;}

        /* Background Lights & Orbs */
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
            width: 500px; height: 500px;
            background: radial-gradient(circle, rgba(254, 44, 85, 0.35) 0%, rgba(255, 255, 255, 0) 70%);
            top: -100px; right: -80px;
        }

        .light-2 {
            width: 550px; height: 550px;
            background: radial-gradient(circle, rgba(37, 244, 238, 0.3) 0%, rgba(255, 255, 255, 0) 70%);
            bottom: -150px; left: -120px;
            animation-delay: -4s;
        }

        @keyframes pulseLight {
            0% { transform: scale(1) translate(0, 0); }
            50% { transform: scale(1.1) translate(20px, -20px); }
            100% { transform: scale(0.95) translate(-20px, 20px); }
        }

        .orb {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.25);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.6);
            box-shadow: inset 8px 8px 20px rgba(255, 255, 255, 0.8), 0 20px 40px rgba(0, 0, 0, 0.08);
            animation: floatOrb 16s infinite ease-in-out;
            z-index: 0 !important;
        }

        .orb-1 { width: 140px; height: 140px; top: 15%; left: 8%; }
        .orb-2 { width: 200px; height: 200px; bottom: 10%; right: 8%; animation-delay: -5s; }

        @keyframes floatOrb {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-30px) rotate(15deg); }
        }

        /* Glass Container Card */
        .block-container {
            max-width: 480px !important;
            padding: 40px 36px !important;
            background: rgba(255, 255, 255, 0.45) !important;
            border-radius: 36px !important;
            position: relative !important;
            z-index: 10 !important;
            backdrop-filter: blur(25px) !important;
            -webkit-backdrop-filter: blur(25px) !important;
            border: 1px solid rgba(255, 255, 255, 0.8) !important;
            box-shadow: 0 30px 60px rgba(0, 0, 0, 0.06) !important;
            margin-top: 2rem !important;
            margin-bottom: 2rem !important;
        }

        /* Badge Styling */
        .badge-wrapper { text-align: center; margin-bottom: 20px; }
        .author-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 6px 16px;
            background: rgba(255, 255, 255, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.9);
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

        /* Text Headings */
        .main-title {
            text-align: center;
            font-size: 34px !important;
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
            margin-bottom: 26px;
            font-weight: 500;
        }

        /* Streamlit File Uploader Clean Fix */
        div[data-testid="stFileUploader"] {
            border: 2px dashed rgba(0, 0, 0, 0.15) !important;
            border-radius: 20px !important;
            padding: 12px !important;
            background: rgba(255, 255, 255, 0.3) !important;
        }

        /* Custom Dark Buttons */
        div.stButton > button, div.stDownloadButton > button {
            width: 100% !important;
            margin-top: 16px !important;
            padding: 16px !important;
            border: none !important;
            border-radius: 18px !important;
            background: #18181b !important;
            color: #ffffff !important;
            font-size: 13px !important;
            font-weight: 700 !important;
            letter-spacing: 1px !important;
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

        .card-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 26px;
            padding-top: 16px;
            border-top: 1px solid rgba(0, 0, 0, 0.08);
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 1px;
            text-transform: uppercase;
            color: rgba(0, 0, 0, 0.4);
        }
    </style>

    <div class="ambient-background">
        <div class="ambient-light light-1"></div>
        <div class="ambient-light light-2"></div>
        <div class="orb orb-1"></div>
        <div class="orb orb-2"></div>
    </div>
""", unsafe_allow_html=True)

# Main Web Structure
st.markdown("""
    <div class="badge-wrapper">
        <div class="author-badge">
            <span class="dot-pulse"></span> Built by Apis
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">TikTok Quality</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Bypass kompresi TikTok ke 1080p 60FPS tanpa re-encoding</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("✦ Klik atau seret file .MP4 ke sini", type=["mp4", "mov"])

if uploaded_file is not None:
    input_path = "temp_input.mp4"
    output_path = "temp_output.mp4"

    if os.path.exists(output_path):
        os.remove(output_path)

    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    if st.button("PROSES VIDEO"):
        with st.spinner("Sedang memproses metadata video..."):
            try:
                if transform is not None:
                    transform(
                        input_path=input_path,
                        output_path=output_path,
                        force=True,
                        quiet=True
                    )
                else:
                    os.system(f'tiktok-quality "{input_path}" "{output_path}"')

                if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                    st.success("✨ Selesai! Video HD berhasil diproses.")
                    st.video(output_path)

                    with open(output_path, "rb") as file:
                        st.download_button(
                            label="UNDUH VIDEO HD",
                            data=file,
                            file_name=f"HD_{uploaded_file.name}",
                            mime="video/mp4"
                        )
                else:
                    st.error("❌ File video ini tidak mendukung pengubahan struktur metadata TikTok.")
            except Exception as err:
                st.error(f"❌ Terjadi kesalahan: {str(err)}")

st.markdown("""
    <div class="card-footer">
        <span>By Apis</span>
        <span>•</span>
        <span>60 FPS Unlock</span>
    </div>
""", unsafe_allow_html=True)