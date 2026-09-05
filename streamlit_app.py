import streamlit as st
import os
import sys

st.set_page_config(page_title="TikTok HD Enhancer", layout="centered")

st.title("TikTok HD Video Enhancer")
st.write("Tingkatkan kualitas video TikTok Anda secara otomatis.")

uploaded_file = st.file_uploader("Pilih video TikTok Anda", type=["mp4", "mov"])

if uploaded_file is not None:
    if os.path.exists("temp_output.mp4"):
        os.remove("temp_output.mp4")

    with open("temp_input.mp4", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.info("Memproses video... Mohon tunggu sebentar.")
    
    # Argumen CLI tiktok-quality yang benar: tiktok-quality [input] [output]
    code = os.system(f'"{sys.executable}" -m tiktok_quality temp_input.mp4 temp_output.mp4')
    
    if os.path.exists("temp_output.mp4") and os.path.getsize("temp_output.mp4") > 0:
        st.success("Selesai! Berikut hasil video HD Anda:")
        st.video("temp_output.mp4")
        
        with open("temp_output.mp4", "rb") as file:
            st.download_button(
                label="Download Video HD",
                data=file,
                file_name="enhanced_tiktok.mp4",
                mime="video/mp4"
            )
    else:
        st.error("Gagal memproses video. Pastikan file video valid.")