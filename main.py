from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def get_user():
    return {"Hello" : "World"}