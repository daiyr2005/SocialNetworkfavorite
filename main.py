from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn

from mysite.api import check_file, favorite
from mysite.database.mongodb import close_mongodb, connect_mongodb


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

# Подключаем роутеры
app.include_router(favorite.favorite_router)
app.include_router(check_file.router)


# Переименовано с test_info на root_info, чтобы pytest не считал это тестом
@app.get("/")
async def root_info():
    return {"message": "all worked"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8002, reload=True)