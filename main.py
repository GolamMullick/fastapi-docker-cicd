from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello latest from Me FastAPI123344 on Ubuntu!"}
