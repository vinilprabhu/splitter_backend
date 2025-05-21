from beanie import Document
from typing import List, Optional
from datetime import datetime, timezone
from bson import ObjectId
from pydantic import BaseModel, Field

from .user import PyObjectId


class Group(Document):
    id: Optional[ObjectId] = Field(default_factory=ObjectId, alias="_id")
    name: str
    members: List[ObjectId]  # User IDs
    created_by: ObjectId
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "groups"

    class Config:
        arbitrary_types_allowed = True