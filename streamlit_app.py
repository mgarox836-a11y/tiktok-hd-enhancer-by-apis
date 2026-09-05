import streamlit as st
import os

try:
    from tiktok_quality.transform import transform
except ImportError:
    transform = None

st.set_page_config(
    page_title="TikTok Quality — Y2K Retro",
    page_icon="💾",
    layout="centered"
)

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400&family=VT323&display=swap');

        html, body, [class*="css"], p, span, button, label {
            font-family: 'Space Mono', monospace !important;
        }

        .stApp { 
            background: radial-gradient(circle, #2a0845 0%, #11001f 100%) !important; 
        }

        #MainMenu, header, footer {visibility: hidden !important;}

        /* --- Y2K RETRO CONTAINER (CHUNKY BORDERS & NEON SHADOWS) --- */
        .block-container {
            width: 90% !important;
            max-width: 520px !important;
            background: #140024 !important;
            border: 4px solid #00ffcc !important;
            box-shadow: 8px 8px 0px #ff007f !important;
            border-radius: 0px !important;
            padding: 32px !important;
            margin: 5vh auto !important;
        }

        .y2k-tag {
            display: inline-block;
            background: #ff007f;
            color: #ffffff;
            font-family: 'VT323', monospace !important;
            font-size: 18px;
            padding: 2px 10px;
            border: 2px solid #00ffcc;
            margin-bottom: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .main-title {
            font-family: 'VT323', monospace !important;
            font-size: clamp(38px, 6vw, 48px) !important;
            color: #00ffcc !important;
            text-shadow: 3px 3px #ff007f;
            line-height: 1;
            margin-bottom: 8px !important;
            text-transform: uppercase;
        }

        .subtitle {
            font-size: 13px;
            color: #ff99ff;
            margin-bottom: 24px;
            border-left: 4px solid #00ffcc;
            padding-left: 10px;
            background: rgba(0, 255, 204, 0.05);
            padding-top: 4px;
            padding-bottom: 4px;
        }

        /* --- Y2K UPLOADER BOX --- */
        [data-testid="stFileUploader"] {
            width: 100% !important;
            border: 3px dashed #ff007f !important;
            border-radius: 0px !important;
            background-color: #1a002b !important;
            padding: 10px !important;
        }
        
        [data-testid="stFileUploader"] button {
            display: none !important;
        }
        
        [data-testid="stFileUploaderDropzone"] {
            background-color: #0d0017 !important;
            border: 2px solid #00ffcc !important;
            border-radius: 0px !important;
        }

        [data-testid="stFileUploaderDropzone"] span, 
        [data-testid="stFileUploaderDropzone"] small, 
        [data-testid="stFileUploaderDropzone"] p,
        [data-testid="stFileUploader"] div {
            color: #00ffcc !important;
            font-weight: 700 !important;
        }

        /* Nama file yang di-upload */
        [data-testid="stUploadedFile"] span,
        [data-testid="stUploadedFile"] div,
        [data-testid="stUploadedFile"] p {
            color: #ffffff !important;
            font-weight: 700 !important;
        }
        
        [data-testid="stUploadedFile"] small {
            color: #ff99ff !important;
        }

        /* --- Y2K RETRO BUTTONS --- */
        div.stButton > button, div.stDownloadButton > button {
            width: 100% !important;
            margin-top: 16px !important;
            padding: 14px !important;
            border: 3px solid #000000 !important;
            border-radius: 0px !important;
            background: #00ffcc !important;
            color: #000000 !important;
            font-size: 14px !important;
            font-weight: 800 !important;
            text-transform: uppercase !important;
            box-shadow: 4px 4px 0px #ff007f !important;
            transition: none !important;
        }

        div.stButton > button:hover, div.stDownloadButton > button:hover {
            background: #ff007f !important;
            color: #ffffff !important;
            box-shadow: 4px 4px 0px #00ffcc !important;
            transform: translate(-2px, -2px);
        }
        
        div.stButton > button:active, div.stDownloadButton > button:active {
            transform: translate(2px, 2px) !important;
            box-shadow: 2px 2px 0px #ff007f !important;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div>
        <span class="y2k-tag">💾 WEB ENHANCE VID TIKTOK BY APIS</span>
    </div>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">TikTok Quality</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Bypass kompresi otomatis ke resolusi 1080p 60FPS tanpa re-encoding.</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Seret dan letakkan file video (MP4 / MOV) di sini", type=["mp4", "mov"])

if uploaded_file is not None:
    input_path = "temp_input.mp4"
    output_path = "temp_output.mp4"

    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    if st.button("PROSES VIDEO SEKARANG"):
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
                st.success("✨ Video berhasil dioptimasi!")
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