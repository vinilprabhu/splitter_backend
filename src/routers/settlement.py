from fastapi import APIRouter, Depends
from src.models.settlement import Settlement
from datetime import datetime
from pydantic import BaseModel
from bson import ObjectId

from src.models.user import User
from src.auth import get_current_user

router = APIRouter(prefix="/settlements", tags=["Settlements"])

class SettlementCreate(BaseModel):
    group_id: str
    from_user: str
    to_user: str
    amount: float

@router.post("/")
async def settle_up(data: SettlementCreate, user: User = Depends(get_current_user)):
    settlement = Settlement(
        group_id=ObjectId(data.group_id),
        from_user=ObjectId(data.from_user),
        to_user=ObjectId(data.to_user),
        amount=data.amount,
        paid_at=datetime.utcnow()
    )
    await settlement.insert()
    return {"message": "Settlement recorded"}
