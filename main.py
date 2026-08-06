from fastapi import FastAPI
import uvicorn
from mysite.database.mongodb import close_mongodb, connect_mongodb
from contextlib import asynccontextmanager
from mysite.api import favorite

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await connect_mongodb()
        print("Mongodb: successful")
        yield
    finally:
        await close_mongodb()
        print("Mongodb: connect close")

app = FastAPI(title="Favorite", lifespan=lifespan)

app.include_router(favorite.favorite_router)
@app.get("/")
async def test_info():
    return {"message": "all worked"}



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8007, reload=True)