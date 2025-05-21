from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from .user import User
from .group import Group
from .expense import Expense
from .settlement import Settlement
from src.config import settings


async def init_db():
    client = AsyncIOMotorClient(settings.mongo_uri)
    await init_beanie(
        database=client.splitter,
        document_models=[User, Group, Expense, Settlement],
    )
