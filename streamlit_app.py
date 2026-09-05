import streamlit as st
import os

# Import pustaka tiktok_quality
try:
    from tiktok_quality.transform import transform
except ImportError:
    transform = None

# Konfigurasi Halaman Web
st.set_page_config(
    page_title="TikTok Quality — Neo Brutalism",
    page_icon="⚡",
    layout="centered"
)

# Custom CSS Neo-Brutalism (HANYA untuk background, kartu, & tombol utama)
st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700;800&display=swap" rel="stylesheet">

    <style>
        * {
            font-family: 'Space Grotesk', sans-serif !important;
        }

        /* Latar Belakang Web */
        .stApp {
            background-color: #f4f0ea !important;
        }

        #MainMenu, header, footer {visibility: hidden !important;}
        .stDeployButton {display:none !important;}
        div[data-testid="stDecoration"] {display:none !important;}

        /* Container Kartu Utama Neo-Brutalism */
        .block-container {
            max-width: 480px !important;
            padding: 36px 28px !important;
            background: #ffffff !important;
            border: 3.5px solid #000000 !important;
            border-radius: 18px !important;
            box-shadow: 8px 8px 0px #000000 !important;
            margin-top: 2.5rem !important;
            margin-bottom: 2.5rem !important;
        }

        /* Badge Built By Apis */
        .badge-wrapper {
            margin-bottom: 12px;
        }
        .neo-badge {
            display: inline-block;
            background: #ffde59;
            color: #000000;
            font-weight: 800;
            font-size: 11px;
            padding: 5px 12px;
            border: 2px solid #000000;
            border-radius: 6px;
            box-shadow: 2px 2px 0px #000000;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        /* Judul & Subtitle */
        .main-title {
            font-size: 36px !important;
            font-weight: 800 !important;
            color: #000000 !important;
            line-height: 1;
            margin-bottom: 8px !important;
            text-transform: uppercase;
        }

        .subtitle {
            font-size: 13px;
            font-weight: 700;
            color: #333333;
            margin-bottom: 24px;
        }

        /* Tombol Utama Neo-Brutalism */
        div.stButton > button, div.stDownloadButton > button {
            width: 100% !important;
            margin-top: 14px !important;
            padding: 14px !important;
            border: 3px solid #000000 !important;
            border-radius: 12px !important;
            background: #000000 !important;
            color: #ffffff !important;
            font-size: 14px !important;
            font-weight: 800 !important;
            letter-spacing: 1px !important;
            text-transform: uppercase !important;
            box-shadow: 4px 4px 0px #ff3131 !important;
            transition: all 0.1s ease !important;
            cursor: pointer !important;
        }

        div.stButton > button:hover, div.stDownloadButton > button:hover {
            transform: translate(-2px, -2px) !important;
            box-shadow: 6px 6px 0px #ff3131 !important;
            background: #000000 !important;
            color: #ffffff !important;
        }

        /* Footer */
        .neo-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 24px;
            padding-top: 16px;
            border-top: 3px solid #000000;
            font-size: 12px;
            font-weight: 800;
            text-transform: uppercase;
            color: #000000;
        }
    </style>
""", unsafe_allow_html=True)

# Elemen UI Header
st.markdown("""
    <div class="badge-wrapper">
        <span class="neo-badge">⚡ BUILT BY APIS</span>
    </div>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">TikTok Quality</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Bypass kompresi TikTok ke 1080p 60FPS tanpa re-encoding.</div>', unsafe_allow_html=True)

# File Uploader Murni Tanpa Modifikasi CSS Internal
uploaded_file = st.file_uploader("Pilih file video (MP4 / MOV):", type=["mp4", "mov"])

if uploaded_file is not None:
    input_path = "temp_input.mp4"
    output_path = "temp_output.mp4"

    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    if st.button("PROSES VIDEO SEKARANG"):
        if os.path.exists(output_path):
            os.remove(output_path)

        with st.spinner("Sedang memproses..."):
            success = False
            
            if transform is not None:
                try:
                    transform(input_path, output_path)
                    if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                        success = True
                except Exception as e:
                    st.warning(f"Catatan: {str(e)}")

            if success:
                st.success("✨ Pemrosesan berhasil!")
                st.video(output_path)

                with open(output_path, "rb") as file:
                    st.download_button(
                        label="UNDUH VIDEO HD",
                        data=file,
                        file_name=f"HD_{uploaded_file.name}",
                        mime="video/mp4"
                    )
            else:
                st.error("❌ Gagal memproses video.")

# Footer
st.markdown("""
    <div class="neo-footer">
        <span>BY APIS</span>
        <span>•</span>
        <span>60 FPS UNLOCK</span>
    </div>
""", unsafe_allow_html=True)