from fastapi import APIRouter
from app.database.requests import get_user_balance, update_user_balance


router = APIRouter()


@router.get("/balance/{user_id}")
async def get_balance(user_id: int):
    balance = await get_user_balance(user_id)
    return {"user_id": user_id, "balance": balance}

@router.post("/balance/update")
async def update_balance(user_id: int, amount: int):
    new_balance = await update_user_balance(user_id, amount)
    return {"user_id": user_id, "new_balance": new_balance}