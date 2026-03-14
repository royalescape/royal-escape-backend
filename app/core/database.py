import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

# Initialize client in global scope for connection reuse
# maxPoolSize=10 is usually plenty for a hobby project 
# and stays well under the Atlas Free Tier limit.
client = AsyncIOMotorClient(
    settings.mongo_uri,
    tls=True,
    tlsCAFile=certifi.where(),
    maxPoolSize=10,
    minPoolSize=1,
    serverSelectionTimeoutMS=5000
)


db = client[settings.mongo_db]
