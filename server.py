from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def get_teste():
    return {"Hello": "World"}
