from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": " Hello World from my Fast api app run on EC2!"}
