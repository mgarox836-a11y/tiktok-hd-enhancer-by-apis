import streamlit as st
import os

st.title("TikTok HD Video Enhancer")

uploaded_file = st.file_uploader("Pilih video TikTok Anda", type=["mp4", "mov"])

if uploaded_file is not None:
    # Simpan file sementara
    with open("temp_input.mp4", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.info("Memproses video...")
    
    # Jalankan perintah tiktok-quality via command line
    os.system("tiktok-quality temp_input.mp4 -o temp_output.mp4")
    
    st.success("Selesai!")
    st.video("temp_output.mp4")
    
    with open("temp_output.mp4", "rb") as file:
        st.download_button(
            label="Download Video HD",
            data=file,
            file_name="enhanced_tiktok.mp4",
            mime="video/mp4"
        )