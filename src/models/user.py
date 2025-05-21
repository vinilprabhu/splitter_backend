from typing import Annotated, Optional
from beanie import Document
from bson import ObjectId
from pydantic import BeforeValidator, EmailStr, Field
from datetime import datetime, timezone

PyObjectId = Annotated[str, BeforeValidator(str)]

class User(Document):
    id: Optional[ObjectId] = Field(default_factory=ObjectId, alias="_id")
    name: str
    email: EmailStr
    password_hash: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "users"

    class Config:
        arbitrary_types_allowed = True