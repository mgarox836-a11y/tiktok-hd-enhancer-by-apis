import streamlit as st
import os
import sys

st.title("TikTok HD Video Enhancer")

uploaded_file = st.file_uploader("Pilih video TikTok Anda", type=["mp4", "mov"])

if uploaded_file is not None:
    # Hapus file lama jika ada
    if os.path.exists("temp_output.mp4"):
        os.remove("temp_output.mp4")

    # Simpan file input sementara
    with open("temp_input.mp4", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.info("Memproses video... Mohon tunggu sebentar.")
    
    # Jalankan modul tiktok-quality secara aman lewat executable Python
    return_code = os.system(f'"{sys.executable}" -m tiktok_quality temp_input.mp4 -o temp_output.mp4')
    
    # Pastikan proses sukses dan file hasil benar-benar ada
    if os.path.exists("temp_output.mp4") and os.path.getsize("temp_output.mp4") > 0:
        st.success("Selesai!")
        st.video("temp_output.mp4")
        
        with open("temp_output.mp4", "rb") as file:
            st.download_button(
                label="Download Video HD",
                data=file,
                file_name="enhanced_tiktok.mp4",
                mime="video/mp4"
            )
    else:
        st.error("Gagal memproses video. Pastikan format video sesuai.")