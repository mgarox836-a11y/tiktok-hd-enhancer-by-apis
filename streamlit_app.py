import streamlit as st
import os
import sys

# Konfigurasi Halaman
st.set_page_config(
    page_title="TikTok HD Enhancer — Buatan Apis",
    page_icon="✨",
    layout="centered"
)

# Kustomisasi CSS Meniru Desain HTML Anda
st.markdown("""
    <style>
    /* Reset Latar Belakang ke Putih / Soft Gray Gradien */
    .stApp {
        background: linear-gradient(180deg, #F9FAFB 0%, #E5E7EB 100%);
        color: #111827;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Sembunyikan Element Bawaan Streamlit yang Mengganggu */
    #MainMenu, header, footer {visibility: hidden;}
    .stDeployButton {display:none;}
    div[data-testid="stDecoration"] {display:none;}

    /* Container Kartu Utama */
    .block-container {
        max-width: 500px !important;
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        background: #ffffff;
        border-radius: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.08), 0 8px 10px -6px rgba(0, 0, 0, 0.01);
        margin-top: 2rem;
        border: 1px solid #E5E7EB;
    }

    /* Badge BUILT BY APIS */
    .badge-container {
        text-align: center;
        margin-bottom: 1rem;
    }
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #F3F4F6;
        border: 1px solid #E5E7EB;
        padding: 6px 16px;
        border-radius: 9999px;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 0.05em;
        color: #374151;
    }
    .badge-dot {
        width: 8px;
        height: 8px;
        background-color: #EF4444;
        border-radius: 50%;
    }

    /* Typography Judul & Sub-judul */
    .title-text {
        font-size: 38px;
        font-weight: 800;
        text-align: center;
        color: #111827;
        line-height: 1.1;
        margin-bottom: 8px;
        letter-spacing: -0.02em;
    }
    .subtitle-text {
        font-size: 15px;
        text-align: center;
        color: #6B7280;
        margin-bottom: 24px;
        line-height: 1.4;
    }

    /* Area File Uploader */
    div[data-testid="stFileUploader"] {
        background: #F9FAFB !important;
        border: 2px dashed #E5E7EB !important;
        border-radius: 20px !important;
        padding: 10px !important;
        text-align: center;
    }
    div[data-testid="stFileUploader"] section {
        background: transparent !important;
    }
    div[data-testid="stFileUploader"] label {
        color: #374151 !important;
        font-weight: 600 !important;
    }

    /* Tombol Hitam 'PROSES VIDEO' / 'DOWNLOAD VIDEO' */
    div.stButton > button, div.stDownloadButton > button {
        width: 100% !important;
        background-color: #111827 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 16px 24px !important;
        font-size: 15px !important;
        font-weight: 700 !important;
        letter-spacing: 0.05em !important;
        cursor: pointer !important;
        margin-top: 10px !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button:hover, div.stDownloadButton > button:hover {
        background-color: #1F2937 !important;
        transform: translateY(-1px);
    }

    /* Custom Footer */
    .custom-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 32px;
        padding-top: 16px;
        border-top: 1px solid #F3F4F6;
        font-size: 12px;
        font-weight: 700;
        color: #9CA3AF;
        letter-spacing: 0.05em;
    }
    </style>
""", unsafe_allow_html=True)

# 1. Badge Top
st.markdown("""
    <div class="badge-container">
        <span class="badge">
            <span class="badge-dot"></span> BUILT BY APIS
        </span>
    </div>
""", unsafe_allow_html=True)

# 2. Judul Utama & Subtitle
st.markdown('<div class="title-text">TikTok Quality</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">Bypass kompresi TikTok ke 1080p 60FPS<br>tanpa re-encoding</div>', unsafe_allow_html=True)

# 3. Form Upload Video
uploaded_file = st.file_uploader("Klik atau seret file .MP4 ke sini", type=["mp4", "mov"], label_visibility="visible")

if uploaded_file is not None:
    # Hapus cache lama jika ada
    if os.path.exists("temp_output.mp4"):
        os.remove("temp_output.mp4")

    with open("temp_input.mp4", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Tombol Proses Video
    if st.button("PROSES VIDEO"):
        with st.spinner("Memproses video... Mohon tunggu sebentar."):
            os.system(f'"{sys.executable}" -m tiktok_quality temp_input.mp4 temp_output.mp4')
        
        if os.path.exists("temp_output.mp4") and os.path.getsize("temp_output.mp4") > 0:
            st.success("✨ Selesai! Video berhasil diproses.")
            st.video("temp_output.mp4")
            
            with open("temp_output.mp4", "rb") as file:
                st.download_button(
                    label="UNDUH VIDEO HD",
                    data=file,
                    file_name="enhanced_tiktok.mp4",
                    mime="video/mp4"
                )
        else:
            st.error("Gagal memproses video. Pastikan format file valid.")

# 4. Footer Bawah (BY APIS & 60 FPS UNLOCK)
st.markdown("""
    <div class="custom-footer">
        <span>BY APIS</span>
        <span>•</span>
        <span>60 FPS UNLOCK</span>
    </div>
""", unsafe_allow_html=True)