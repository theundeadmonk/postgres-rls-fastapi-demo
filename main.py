from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/toys/")
async def toys(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]