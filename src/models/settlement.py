from typing import Optional
from beanie import Document
from datetime import datetime, timezone
from bson import ObjectId
from pydantic import Field

from .user import PyObjectId


class Settlement(Document):
    id: Optional[ObjectId] = Field(default_factory=ObjectId, alias="_id")
    group_id: PyObjectId
    from_user: PyObjectId
    to_user: PyObjectId
    amount: float
    paid_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "settlements"

    class Config:
        arbitrary_types_allowed = True  # ✅ This allows ObjectId in schema
