from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Fahad latest from Me FastAPI123344 on Ubuntu!"}
