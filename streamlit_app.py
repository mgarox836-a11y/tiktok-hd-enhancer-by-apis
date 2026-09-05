import streamlit as st
import os
import time
import uuid
import threading

try:
    from tiktok_quality.transform import transform
except ImportError:
    transform = None

st.set_page_config(
    page_title="TikTok Quality — Y2K Retro",
    page_icon="💾",
    layout="wide"
)

# --- PENGAMAN ANTREAN SERVER (SEMAPHORE) ---
# Batasi maksimal hanya 2 video yang diproses bersamaan di server agar tidak crash
process_lock = threading.Semaphore(2)

def cleanup_old_temp_files(max_age_minutes=15):
    current_time = time.time()
    max_age_seconds = max_age_minutes * 60
    
    try:
        for filename in os.listdir("."):
            if filename.startswith("temp_input_") or filename.startswith("temp_output_"):
                file_path = os.path.join(".", filename)
                file_mod_time = os.path.getmtime(file_path)
                if (current_time - file_mod_time) > max_age_seconds:
                    os.remove(file_path)
    except Exception:
        pass

cleanup_old_temp_files(max_age_minutes=15)

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())[:8]

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

        .block-container {
            width: 92% !important;
            max-width: 900px !important;
            background: #140024 !important;
            border: 4px solid #00ffcc !important;
            box-shadow: 10px 10px 0px #ff007f !important;
            border-radius: 0px !important;
            padding: 40px 6% !important;
            margin: 4vh auto !important;
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
            font-size: clamp(40px, 5vw, 56px) !important;
            color: #00ffcc !important;
            text-shadow: 3px 3px #ff007f;
            line-height: 1;
            margin-bottom: 8px !important;
            text-transform: uppercase;
        }

        .subtitle {
            font-size: clamp(13px, 1.5vw, 15px);
            color: #ff99ff;
            margin-bottom: 28px;
            border-left: 4px solid #00ffcc;
            padding-left: 12px;
            background: rgba(0, 255, 204, 0.05);
            padding-top: 6px;
            padding-bottom: 6px;
        }

        .tips-box {
            background: rgba(255, 0, 127, 0.1);
            border: 2px dashed #ff007f;
            padding: 14px;
            margin-top: 16px;
            font-size: 13px;
            color: #ffccff;
            line-height: 1.5;
        }

        [data-testid="stFileUploader"] {
            width: 100% !important;
            border: 3px dashed #ff007f !important;
            border-radius: 0px !important;
            background-color: #1a002b !important;
            padding: 12px !important;
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

        [data-testid="stUploadedFile"] span,
        [data-testid="stUploadedFile"] div,
        [data-testid="stUploadedFile"] p {
            color: #ffffff !important;
            font-weight: 700 !important;
        }
        
        [data-testid="stUploadedFile"] small {
            color: #ff99ff !important;
        }

        @keyframes pulseGlow {
            0% { box-shadow: 4px 4px 0px #ff007f; }
            50% { box-shadow: 6px 6px 12px #00ffcc, 4px 4px 0px #ff007f; }
            100% { box-shadow: 4px 4px 0px #ff007f; }
        }

        div.stButton > button, div.stLinkButton > a, div.stDownloadButton > button {
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
            text-align: center !important;
            text-decoration: none !important;
            box-shadow: 4px 4px 0px #ff007f !important;
            display: block !important;
            transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1) !important;
            animation: pulseGlow 3s infinite;
        }

        div.stButton > button:hover, div.stLinkButton > a:hover, div.stDownloadButton > button:hover {
            background: #ff007f !important;
            color: #ffffff !important;
            box-shadow: 6px 6px 0px #00ffcc !important;
            transform: translate(-3px, -3px) !important;
        }
        
        div.stButton > button:active, div.stLinkButton > a:active, div.stDownloadButton > button:active {
            transform: translate(2px, 2px) !important;
            box-shadow: 2px 2px 0px #ff007f !important;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div>
        <span class="y2k-tag">💾 SYSTEM_READY // FULL_PROTECTION</span>
    </div>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">TikTok Quality</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Bypass kompresi otomatis ke resolusi 1080p 60FPS tanpa re-encoding.</div>', unsafe_allow_html=True)

MAX_FILE_SIZE_MB = 150

uploaded_file = st.file_uploader("Seret dan letakkan file video (MP4 / MOV) di sini", type=["mp4", "mov"])

st.markdown("""
    <div class="tips-box">
        💡 <b>TIPS SERVER:</b> Gunakan video berdurasi pendek (di bawah 2 menit). Jika ukuran file video Anda terlalu besar/berat, disarankan untuk mengompresnya terlebih dahulu agar pemrosesan berjalan lancar dan cepat!
    </div>
""", unsafe_allow_html=True)

st.link_button("🌐 COMPRESS VIDEO DI SINI (RECOMMENDED)", "https://videocompress.ai/id")

if uploaded_file is not None:
    file_size_mb = uploaded_file.size / (1024 * 1024)
    
    if file_size_mb > MAX_FILE_SIZE_MB:
        st.error(f"❌ Ukuran file terlalu besar ({file_size_mb:.1f}MB). Batas maksimal adalah {MAX_FILE_SIZE_MB}MB.")
    else:
        sid = st.session_state.session_id
        input_path = f"temp_input_{sid}.mp4"
        output_path = f"temp_output_{sid}.mp4"

        with open(input_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        if st.button("PROSES VIDEO SEKARANG"):
            # Cek apakah kapasitas server penuh menangani pengguna lain
            if not process_lock.acquire(blocking=False):
                st.warning("⚠️ Server sedang sibuk memproses video pengguna lain. Harap tunggu sebentar dan coba lagi ya!")
            else:
                try:
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
                            
                            if os.path.exists(input_path):
                                os.remove(input_path)
                        else:
                            st.error("❌ Gagal memproses video.")
                finally:
                    # Wajib lepaskan kunci agar antrean berikutnya bisa masuk
                    process_lock.release()