import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

client = AsyncIOMotorClient(
    settings.mongo_uri,
    tls=True,
    tlsCAFile=certifi.where(),
)


db = client[settings.mongo_db]
