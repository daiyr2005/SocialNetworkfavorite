from pymongo import AsyncMongoClient
from mysite.config import settings

mongo_client: AsyncMongoClient | None = None
mongo_database = None


async def connect_mongodb():
    global mongo_client, mongo_database

    mongo_client = AsyncMongoClient(
        settings.mongodb_url,
        serverSelectionTimeoutMS=5000,
        tz_aware=True
    )

    await mongo_client.admin.command("ping")

    mongo_database = mongo_client[
        settings.mongodb_db_name
    ]

    print("MongoDB connected")


async def close_mongodb():
    global mongo_client, mongo_database

    if mongo_client is not None:
        mongo_client.close()

    mongo_client = None
    mongo_database = None

    print("MongoDB closed")


def get_database():
    if mongo_database is None:
        raise RuntimeError("Подключение к MongoDB отсутствует")

    return mongo_database


def get_favorite_connection():
    database = get_database()
    return database["favorites"]


def get_favorite_item_connection():
    database = get_database()
    return database["favorites_item"]