from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.doc_parser import extract_course_info
import shutil
import os

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_ext = file.filename.split(".")[-1].lower()
    if file_ext not in ["pdf", "docx"]:
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are allowed.")
    
    file_location = f"temp/{file.filename}"
    os.makedirs("temp", exist_ok=True)
    
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)

    result = extract_course_info(file_location, file_ext)
    return {"status": "success", "data": result}
