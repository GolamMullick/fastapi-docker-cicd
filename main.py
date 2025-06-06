import os
import time
import json
from threading import Thread
from typing import List

from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from botocore.exceptions import BotoCoreError, ClientError

import boto3

# Your existing SQLAlchemy/database setup
from database import engine, SessionLocal
from models import Base, Flat

# --------- AWS SETTINGS FROM ENVIRONMENT ---------
S3_BUCKET = "golam1991-bucket"
QUEUE_URL = "https://sqs.ap-southeast-2.amazonaws.com/137435348544/ekyc-job-queue"
TABLE_NAME = "ekyc-jobs"
AWS_REGION = "ap-southeast-2"

# --------- AWS CLIENTS ---------
s3 = boto3.client("s3", region_name=AWS_REGION)
sqs = boto3.client("sqs", region_name=AWS_REGION)
dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)

# --------- DATABASE INIT ---------
Base.metadata.create_all(bind=engine)

# --------- FASTAPI APP ---------
app = FastAPI()

# --------- Pydantic Schemas ---------
class FlatCreate(BaseModel):
    address: str
    suburb: str
    price: float
    description: str

class FlatRead(FlatCreate):
    id: int
    class Config:
        orm_mode = True

# --------- DB Dependency ---------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --------- Endpoints ---------
@app.get("/")
def root():
    return {"message": "Hello World from my FastAPI app run on EC2!"}

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
    try:
        file.file.seek(0)
        upload_file_to_s3(file.file, S3_BUCKET, file.filename)
        return {"filename": file.filename}
    except (BotoCoreError, ClientError) as e:
        raise HTTPException(status_code=500, detail=f"S3 error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"File upload failed: {str(e)}")

@app.get("/download/{filename}")
def download_file(filename: str):
    data = download_file_from_s3(S3_BUCKET, filename)
    return StreamingResponse(iter([data]), media_type="application/octet-stream")

# --------- S3 Utility Functions ---------
def upload_file_to_s3(file, bucket, filename):
    file.seek(0)
    s3.upload_fileobj(file, bucket, filename)

def download_file_from_s3(bucket, filename):
    from io import BytesIO
    stream = BytesIO()
    s3.download_fileobj(bucket, filename, stream)
    stream.seek(0)
    return stream.read()

# --------- SQS/DynamoDB WORKER ---------
processing = True

def process_file(bucket, key):
    local_path = f"/tmp/{key.split('/')[-1]}"
    s3.download_file(bucket, key, local_path)
    # Simulate processing
    time.sleep(2)
    return "pass"

def worker_loop():
    global processing
    while processing:
        msgs = sqs.receive_message(QueueUrl=QUEUE_URL, MaxNumberOfMessages=1, WaitTimeSeconds=10)
        if "Messages" in msgs:
            for msg in msgs["Messages"]:
                body = json.loads(msg["Body"])
                job_id = body["job_id"]
                bucket = body["bucket"]
                key = body["key"]
                result = process_file(bucket, key)
                table = dynamodb.Table(TABLE_NAME)
                table.update_item(
                    Key={"job_id": job_id},
                    UpdateExpression="set #s=:s, #r=:r",
                    ExpressionAttributeNames={"#s": "status", "#r": "result"},
                    ExpressionAttributeValues={":s": "done", ":r": result},
                )
                sqs.delete_message(QueueUrl=QUEUE_URL, ReceiptHandle=msg["ReceiptHandle"])
        else:
            time.sleep(5)

@app.on_event("startup")
def startup_event():
    Thread(target=worker_loop, daemon=True).start()

@app.get("/worker-health")
def worker_health():
    return {"status": "ok", "worker_running": processing}

@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    table = dynamodb.Table(TABLE_NAME)
    resp = table.get_item(Key={"job_id": job_id})
    return resp.get("Item", {"error": "Job not found"})

@app.post("/stop-worker")
def stop_worker():
    global processing
    processing = False
    return {"status": "worker stopping"}
