import streamlit as st
import os

# Pustaka internal pemrosesan video (Python Murni)
try:
    from tiktok_quality.transform import transform
except ImportError:
    transform = None

# Konfigurasi Halaman Web Standard
st.set_page_config(
    page_title="TikTok HD Enhancer — Buatan Apis",
    page_icon="✨",
    layout="centered"
)

# Custom CSS Minimalis (Aman & Tidak Merusak Elemen Uploader Asli)
st.markdown("""
    <style>
        /* Sembunyikan Header Streamlit Bawaan */
        #MainMenu, header, footer {visibility: hidden !important;}
        .stDeployButton {display:none !important;}

        /* Styling Kartu Utama */
        .main-card {
            background-color: #ffffff;
            padding: 24px;
            border-radius: 16px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            border: 1px solid #e2e8f0;
            margin-bottom: 20px;
        }

        /* Header Subtitle */
        .sub-text {
            color: #64748b;
            font-size: 14px;
            margin-top: -10px;
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# UI Layout Utama
st.caption("BUILT BY APIS")
st.title("TikTok Quality")
st.markdown('<p class="sub-text">Bypass kompresi TikTok ke 1080p 60FPS tanpa re-encoding</p>', unsafe_allow_html=True)

# Elemen File Uploader Standar Streamlit
uploaded_file = st.file_uploader("Pilih file video MP4 / MOV", type=["mp4", "mov"])

if uploaded_file is not None:
    input_path = "temp_input.mp4"
    output_path = "temp_output.mp4"

    # Simpan file yang diunggah
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    if st.button("PROSES VIDEO", type="primary", use_container_width=True):
        if os.path.exists(output_path):
            os.remove(output_path)

        with st.spinner("Sedang memproses file video..."):
            success = False
            
            # Eksekusi Pemrosesan Python Murni
            if transform is not None:
                try:
                    transform(input_path, output_path)
                    if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                        success = True
                except Exception as e:
                    st.warning(f"Metadata standar tidak dapat diubah: {str(e)}")

            # Jika berhasil diproses
            if success:
                st.success("✨ Pemrosesan selesai! Video siap diunduh.")
                st.video(output_path)

                with open(output_path, "rb") as file:
                    st.download_button(
                        label="UNDUH VIDEO HD",
                        data=file,
                        file_name=f"HD_{uploaded_file.name}",
                        mime="video/mp4",
                        use_container_width=True
                    )
            else:
                st.error("❌ Video ini tidak kompatibel untuk diubah metadanya. Gunakan video mentah langsung dari HP/Kamera.")

# Footer Sederhana
st.divider()
st.caption("By Apis • 60 FPS Unlock")