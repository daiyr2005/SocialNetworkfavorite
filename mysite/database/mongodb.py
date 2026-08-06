from motor.motor_asyncio import AsyncIOMotorClient

from mysite.config import settings


client = None
database = None


async def connect_mongodb():

    global client, database

    client = AsyncIOMotorClient(
        settings.mongodb_url
    )

    database = client[
        settings.mongodb_db_name
    ]

    await client.admin.command("ping")

    print("MongoDB connected")



async def close_mongodb():

    global client

    if client:
        client.close()

        print("MongoDB closed")



async def get_favorite_connection():

    return database["favorites"]