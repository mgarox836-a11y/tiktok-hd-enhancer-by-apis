import streamlit as st
import os

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

# Custom CSS Neo-Brutalism (Fix Total Overlap & Dark Mode Clash)
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700;800&display=swap');

        /* Gunakan class spesifik, BUKAN wildcard (*) agar komponen internal Streamlit tidak rusak */
        html, body, [class*="css"], [class*="st-"], p, span, button, label {
            font-family: 'Space Grotesk', sans-serif !important;
        }

        /* Latar Belakang & Hide Elemen Bawaan */
        .stApp { background-color: #f4f0ea !important; }
        #MainMenu, header, footer {visibility: hidden !important;}

        /* Container Kartu Utama Neo-Brutalism */
        .block-container {
            max-width: 480px !important;
            padding: 36px 28px !important;
            background: #ffffff !important;
            border: 4px solid #000000 !important;
            border-radius: 16px !important;
            box-shadow: 8px 8px 0px #000000 !important;
            margin-top: 2rem !important;
            margin-bottom: 2rem !important;
        }

        .main-title {
            font-size: 36px !important;
            font-weight: 800 !important;
            color: #000000 !important;
            line-height: 1.1;
            margin-bottom: 8px !important;
            text-transform: uppercase;
        }

        .subtitle {
            font-size: 14px;
            font-weight: 700;
            color: #444444;
            margin-bottom: 24px;
        }

        /* --- FIX AREA UPLOADER (ANTI-OVERLAP & PAKSA LIGHT MODE) --- */
        /* Hapus warna gelap bawaan sistem di area uploader */
        [data-testid="stFileUploader"] section {
            background-color: transparent !important;
        }
        
        /* Desain area dropzone */
        [data-testid="stFileUploaderDropzone"] {
            background-color: #ffffff !important;
            border: 3px dashed #000000 !important;
            border-radius: 12px !important;
            padding: 16px !important;
        }
        
        /* Paksa semua teks di dalam uploader menjadi hitam (menimpa dark mode sistem) */
        [data-testid="stFileUploaderDropzone"] *, [data-testid="stFileUploader"] label p {
            color: #000000 !important;
        }

        [data-testid="stFileUploader"] label p {
            font-weight: 800 !important;
            font-size: 14px !important;
            text-transform: uppercase;
        }

        /* --- FIX TEKS BERTUMPUK (SEMBUNYIKAN TEKS SCREEN READER) --- */
        .st-visually-hidden {
            display: none !important;
            opacity: 0 !important;
        }

        /* --- TOMBOL UTAMA NEO-BRUTALISM --- */
        div.stButton > button, div.stDownloadButton > button {
            width: 100% !important;
            margin-top: 16px !important;
            padding: 14px !important;
            border: 3px solid #000000 !important;
            border-radius: 12px !important;
            background: #ffde59 !important;
            color: #000000 !important;
            font-size: 14px !important;
            font-weight: 800 !important;
            text-transform: uppercase !important;
            box-shadow: 4px 4px 0px #000000 !important;
            transition: all 0.1s ease !important;
        }

        div.stButton > button:hover, div.stDownloadButton > button:hover {
            transform: translate(-2px, -2px) !important;
            box-shadow: 6px 6px 0px #000000 !important;
        }
        
        div.stButton > button:active, div.stDownloadButton > button:active {
            transform: translate(2px, 2px) !important;
            box-shadow: 2px 2px 0px #000000 !important;
        }
    </style>
""", unsafe_allow_html=True)

# UI Header
st.markdown('<div class="main-title">TikTok Quality</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">⚡ BUILT BY APIS • Bypass kompresi ke 1080p 60FPS.</div>', unsafe_allow_html=True)

# Uploader
uploaded_file = st.file_uploader("Upload video (MP4 / MOV):", type=["mp4", "mov"])

if uploaded_file is not None:
    input_path = "temp_input.mp4"
    output_path = "temp_output.mp4"

    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    if st.button("PROSES VIDEO"):
        if os.path.exists(output_path):
            os.remove(output_path)

        with st.spinner("Memproses video..."):
            success = False
            if transform is not None:
                try:
                    transform(input_path, output_path)
                    if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                        success = True
                except Exception as e:
                    st.warning(f"Error: {str(e)}")

            if success:
                st.success("✨ Selesai diproses!")
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