from beanie import Document
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timezone
from bson import ObjectId

from .user import PyObjectId

class ExpenseSplit(BaseModel):
    user_id: PyObjectId
    owed_amount: float

    model_config = {
        "arbitrary_types_allowed": True,
    }


class Expense(Document):
    id: Optional[PyObjectId] = Field(default_factory=ObjectId, alias="_id")
    group_id: PyObjectId
    paid_by: PyObjectId
    amount: float
    description: str
    splits: List[ExpenseSplit]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_by: PyObjectId

    class Settings:
        name = "expenses"

    class Config:
        arbitrary_types_allowed = True
