from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": " Everything Fahad latest from Me FastAPI123344 on Ubuntu!"}
