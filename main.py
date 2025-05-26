from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from s3_utils import upload_file_to_s3, download_file_from_s3
from database import engine
from models import Base
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Flat
from database import SessionLocal
from pydantic import BaseModel
from typing import List

Base.metadata.create_all(bind=engine)

app = FastAPI()
S3_BUCKET = "EC2"

class FlatCreate(BaseModel):
    address: str
    suburb: str
    price: float
    description: str

class FlatRead(FlatCreate):
    id: int
    class Config:
        orm_mode = True

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": " Hello Hello World from my Fast api app run on EC2!"}


@app.post("/flats/", response_model=FlatRead)
def create_flat(flat: FlatCreate, db: Session = Depends(get_db)):
    db_flat = Flat(**flat.dict())
    db.add(db_flat)
    db.commit()
    db.refresh(db_flat)
    return db_flat

@app.get("/flats/", response_model=List[FlatRead])
def list_flats(db: Session = Depends(get_db)):
    return db.query(Flat).all()


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file.file.seek(0)
    upload_file_to_s3(file.file, S3_BUCKET, file.filename)
    return {"filename": file.filename}

@app.get("/download/{filename}")
def download_file(filename: str):
    data = download_file_from_s3(S3_BUCKET, filename)
    return StreamingResponse(iter([data]), media_type="application/octet-stream")