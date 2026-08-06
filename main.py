from fastapi import FastAPI
import uvicorn
from mysite.database.mongodb import close_mongodb, connect_mongodb
from contextlib import asynccontextmanager
from mysite.api import bookings

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await connect_mongodb()
        print("Mongodb: successful")
        yield
    finally:
        await close_mongodb()
        print("Mongodb: connect close")

booking_app = FastAPI(title="Booking Service", lifespan=lifespan)

booking_app.include_router(bookings.booking_router)
@booking_app.get("/")
async def test_info():
    return {"message": "all worked"}



if __name__ == "__main__":
    uvicorn.run("main:booking_app", host="127.0.0.1", port=8002, reload=True)