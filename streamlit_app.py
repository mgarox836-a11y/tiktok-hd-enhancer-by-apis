import streamlit as st
import os

try:
    from tiktok_quality.transform import transform
except ImportError:
    transform = None

st.set_page_config(
    page_title="TikTok Quality — Bento UI",
    page_icon="⚡",
    layout="centered"
)

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap');

        html, body, [class*="css"], p, span, button, label {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }

        .stApp { background-color: #f8fafc !important; }
        #MainMenu, header, footer {visibility: hidden !important;}

        /* --- BENTO GRID CONTAINER (ELASTIS & RESPONSIF) --- */
        .block-container {
            width: 90% !important;
            max-width: 600px !important;
            min-width: 320px !important;
            padding: 40px !important;
            background: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 24px !important;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.05) !important;
            margin: 5vh auto !important;
        }

        /* Bento Badge */
        .bento-badge {
            display: inline-flex;
            align-items: center;
            background: #eff6ff;
            color: #2563eb;
            font-weight: 700;
            font-size: 11px;
            padding: 6px 12px;
            border-radius: 9999px;
            margin-bottom: 14px;
            letter-spacing: -0.01em;
            text-transform: uppercase;
        }

        .main-title {
            font-size: clamp(26px, 4vw, 34px) !important;
            font-weight: 800 !important;
            color: #0f172a !important;
            letter-spacing: -0.03em;
            line-height: 1.15;
            margin-bottom: 8px !important;
        }

        .subtitle {
            font-size: clamp(13px, 1.5vw, 15px);
            font-weight: 500;
            color: #64748b;
            margin-bottom: 28px;
            letter-spacing: -0.01em;
        }

        /* --- BENTO UPLOADER CARD --- */
        [data-testid="stFileUploader"] {
            width: 100% !important;
            border: 2px dashed #cbd5e1 !important;
            border-radius: 16px !important;
            background-color: #f8fafc !important;
            padding: 12px !important;
            transition: all 0.2s ease;
        }

        [data-testid="stFileUploader"]:hover {
            border-color: #2563eb !important;
        }
        
        [data-testid="stFileUploader"] button {
            display: none !important;
        }
        
        [data-testid="stFileUploaderDropzone"] {
            background-color: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 12px !important;
            padding: 12px !important;
        }

        /* Teks Instruksi Drag & Drop */
        [data-testid="stFileUploaderDropzone"] span, 
        [data-testid="stFileUploaderDropzone"] small, 
        [data-testid="stFileUploaderDropzone"] p,
        [data-testid="stFileUploader"] div {
            color: #475569 !important;
            font-weight: 600 !important;
        }

        /* Nama File yang Di-upload */
        [data-testid="stUploadedFile"] span,
        [data-testid="stUploadedFile"] div,
        [data-testid="stUploadedFile"] p {
            color: #0f172a !important;
            font-weight: 600 !important;
        }
        
        [data-testid="stUploadedFile"] small {
            color: #64748b !important;
        }

        /* --- BENTO BUTTONS (PRIMARY ACCENT) --- */
        div.stButton > button, div.stDownloadButton > button {
            width: 100% !important;
            margin-top: 18px !important;
            padding: 14px 20px !important;
            border: none !important;
            border-radius: 14px !important;
            background: #2563eb !important;
            color: #ffffff !important;
            font-size: 14px !important;
            font-weight: 700 !important;
            letter-spacing: -0.01em !important;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25) !important;
            transition: all 0.2s ease !important;
        }

        div.stButton > button:hover, div.stDownloadButton > button:hover {
            background: #1d4ed8 !important;
            box-shadow: 0 6px 16px rgba(37, 99, 235, 0.35) !important;
            transform: translateY(-1px);
        }
        
        div.stButton > button:active, div.stDownloadButton > button:active {
            transform: translateY(0px);
        }
    </style>
""", unsafe_allow_html=True)

# Bento UI Header Section
st.markdown("""
    <div>
        <span class="bento-badge">⚡ Bento Engine</span>
    </div>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">TikTok Quality</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Bypass kompresi otomatis ke resolusi 1080p 60FPS tanpa re-encoding.</div>', unsafe_allow_html=True)

# File Uploader
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