from fastapi import APIRouter, Depends
from src.auth import get_current_user
from src.models.expense import Expense, ExpenseSplit
from bson import ObjectId
from pydantic import BaseModel
from typing import List
from datetime import datetime

from src.models.user import User

router = APIRouter(prefix="/expenses", tags=["Expenses"])


class ExpenseSplitCreate(BaseModel):
    user_id: str
    owed_amount: float


class ExpenseCreate(BaseModel):
    group_id: str
    paid_by: str
    amount: float
    description: str
    splits: List[ExpenseSplitCreate]


@router.post("/")
async def add_expense(
    data: ExpenseCreate,
    user: User = Depends(get_current_user)
):
    splits = [
        ExpenseSplit(
            user_id=ObjectId(split.user_id),
            owed_amount=split.owed_amount
        )
        for split in data.splits
    ]
    expense = Expense(
        group_id=ObjectId(data.group_id),
        paid_by=ObjectId(data.paid_by),
        amount=data.amount,
        description=data.description,
        splits=splits,
        created_by=ObjectId(user['id']),
    )

    print('expense', expense)

    await expense.insert()
    return {"message": "Expense added"}


@router.get("/group/{group_id}", response_model=List[Expense])
async def get_expenses_for_group(
    group_id: str,
    user: User = Depends(get_current_user)
):
    expenses = await Expense.find(Expense.group_id == ObjectId(group_id)).to_list()
    return expenses

@router.get("/user", response_model=List[Expense])
async def get_expenses_for_user(
    user: User = Depends(get_current_user)
):
    expenses = await Expense.find(Expense.paid_by == ObjectId(user['id'])).to_list()
    return expenses