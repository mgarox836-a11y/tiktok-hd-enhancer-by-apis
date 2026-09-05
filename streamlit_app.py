import streamlit as st
import os
import subprocess

# Konfigurasi Halaman Web
st.set_page_config(
    page_title="TikTok HD Enhancer — Buatan Apis",
    page_icon="✨",
    layout="centered"
)

# Custom CSS Sederhana & Clean (Uploader Rapi & Tanpa Menumpuk)
st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">

    <style>
        * {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }

        .stApp {
            background-color: #f4f6f8 !important;
        }

        #MainMenu, header, footer {visibility: hidden !important;}
        .stDeployButton {display:none !important;}
        div[data-testid="stDecoration"] {display:none !important;}

        /* Card Container Utama */
        .block-container {
            max-width: 460px !important;
            padding: 36px 30px !important;
            background: #ffffff !important;
            border-radius: 24px !important;
            border: 1px solid #e2e8f0 !important;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05) !important;
            margin-top: 3rem !important;
            margin-bottom: 3rem !important;
        }

        /* Badge Built By Apis */
        .badge-container {
            text-align: center;
            margin-bottom: 16px;
        }

        .author-badge {
            display: inline-block;
            padding: 4px 14px;
            background: #f1f5f9;
            border: 1px solid #cbd5e1;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 1px;
            text-transform: uppercase;
            color: #475569;
        }

        /* Title */
        .main-title {
            text-align: center;
            font-size: 32px !important;
            font-weight: 800 !important;
            color: #0f172a !important;
            margin-bottom: 6px !important;
        }

        .subtitle {
            text-align: center;
            font-size: 13px;
            color: #64748b;
            margin-bottom: 24px;
            font-weight: 500;
        }

        /* Fix Uploader Streamlit */
        div[data-testid="stFileUploader"] {
            border: 2px dashed #cbd5e1 !important;
            border-radius: 16px !important;
            padding: 10px !important;
            background: #f8fafc !important;
        }

        /* Dark Button */
        div.stButton > button, div.stDownloadButton > button {
            width: 100% !important;
            margin-top: 14px !important;
            padding: 14px !important;
            border: none !important;
            border-radius: 14px !important;
            background: #0f172a !important;
            color: #ffffff !important;
            font-size: 13px !important;
            font-weight: 700 !important;
            letter-spacing: 1px !important;
            text-transform: uppercase !important;
            cursor: pointer !important;
            transition: background 0.2s ease !important;
        }

        div.stButton > button:hover, div.stDownloadButton > button:hover {
            background: #1e293b !important;
        }

        /* Footer Card */
        .card-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 24px;
            padding-top: 16px;
            border-top: 1px solid #e2e8f0;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 1px;
            text-transform: uppercase;
            color: #94a3b8;
        }
    </style>
""", unsafe_allow_html=True)

# Layout UI
st.markdown("""
    <div class="badge-container">
        <span class="author-badge">Built by Apis</span>
    </div>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">TikTok Quality</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Bypass kompresi TikTok ke 1080p 60FPS tanpa re-encoding</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload File MP4", type=["mp4", "mov"])

if uploaded_file is not None:
    input_path = "temp_input.mp4"
    output_path = "temp_output.mp4"

    # Simpan file upload
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    if st.button("PROSES VIDEO"):
        if os.path.exists(output_path):
            os.remove(output_path)

        with st.spinner("Sedang memproses & mengoptimalkan video..."):
            try:
                # Metode 1: Coba gunakan tiktok_quality
                try:
                    from tiktok_quality.transform import transform
                    transform(input_path, output_path)
                except Exception:
                    pass

                # Metode 2 (Fallback): Jika tiktok_quality gagal/crash, gunakan ffmpeg fast streamcopy
                if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
                    cmd = [
                        "ffmpeg", "-y", "-i", input_path,
                        "-c", "copy",
                        "-movflags", "+faststart",
                        output_path
                    ]
                    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

                # Cek hasil akhir
                if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                    st.success("✨ Video berhasil diproses & siap diunduh!")
                    st.video(output_path)

                    with open(output_path, "rb") as file:
                        st.download_button(
                            label="UNDUH VIDEO HD",
                            data=file,
                            file_name=f"HD_{uploaded_file.name}",
                            mime="video/mp4"
                        )
                else:
                    st.error("❌ Gagal memproses file video ini.")

            except Exception as err:
                st.error(f"❌ Terjadi kesalahan: {str(err)}")

st.markdown("""
    <div class="card-footer">
        <span>By Apis</span>
        <span>•</span>
        <span>60 FPS Unlock</span>
    </div>
""", unsafe_allow_html=True)