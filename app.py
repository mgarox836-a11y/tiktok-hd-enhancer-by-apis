import os
import shutil
import traceback
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import tiktok_quality

app = FastAPI()

UPLOAD_DIR = "uploads"
PROCESSED_DIR = "processed"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

@app.get("/")
def read_root():
    # Membaca file index.html langsung dari folder proyek
    if os.path.exists("index.html"):
        return FileResponse("index.html")
    # Jika index.html ada di dalam folder tiktok-enhancer-web
    elif os.path.exists("tiktok-enhancer-web/index.html"):
        return FileResponse("tiktok-enhancer-web/index.html")
    return {"message": "index.html tidak ditemukan"}

@app.post("/api/enhance")
async def enhance_video(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".mp4"):
        raise HTTPException(status_code=400, detail="Hanya file .mp4 yang didukung.")

    safe_filename = file.filename.replace(" ", "_")
    input_path = os.path.join(UPLOAD_DIR, safe_filename)
    output_filename = f"enhanced_{safe_filename}"
    output_path = os.path.join(PROCESSED_DIR, output_filename)

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        tiktok_quality.transform(input_path, output_path, multiplier=10)

        return FileResponse(
            path=output_path, 
            filename=output_filename, 
            media_type="video/mp4"
        )
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Gagal memproses: {str(e)}")