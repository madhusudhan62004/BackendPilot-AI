# from motor.motor_asyncio import AsyncIOMotorClient

# from app.core.config import settings

# client = AsyncIOMotorClient(settings.MONGODB_URI)

# database = client[settings.DATABASE_NAME]

from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

client = AsyncIOMotorClient(
    settings.MONGODB_URI,
    connect=False,
)

database = client[settings.DATABASE_NAME]