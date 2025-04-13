from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.database import requests as rq

router = APIRouter()

class UserCreateRequest(BaseModel):
    tg_id: int


@router.get("/users/{tg_id}")
async def get_user(tg_id: int):
    user_id = await rq.get_user_id(tg_id)
    response = await rq.get_user(user_id)
    return response

@router.get("/upgrades")
async def get_upgrades():
    response = await rq.get_all_upgrades()
    return response

@router.post("/users/{tg_id}/buy_upgrade/{upgrade_id}")
async def buy_upgrade(tg_id: int, upgrade_id: int):
    user_id = await rq.get_user_id(tg_id)
    response = await rq.buy_upgrade(user_id, upgrade_id)
    return response

@router.get("/locations")
async def get_locations():
    response = await rq.get_all_locations()
    return response

@router.post("/users/{tg_id}/buy_location/{location_id}")
async def buy_location(tg_id: int, location_id: int):
    user_id = await rq.get_user_id(tg_id)
    response = await rq.buy_location(user_id, location_id)
    return response

@router.post("/users/{tg_id}/set_location/{location_id}")
async def set_location(tg_id: int, location_id: int):
    user_id = await rq.get_user_id(tg_id)
    response = await rq.change_current_location(user_id, location_id)
    return response

@router.post("/users/create")
async def create_user_endpoint(data: UserCreateRequest):
    successful_creation = await rq.add_user(data.tg_id)
    user_id = await rq.get_user_id(data.tg_id)
    user = await rq.get_user(user_id)
    if not user or not successful_creation:
        raise HTTPException(status_code=400, detail="User already exists or creation failed")

    return user

@router.post("/users/{tg_id}/balance/add")
async def add_balance(tg_id: int):
    user_id = await rq.get_user_id(tg_id)
    new_balance = await rq.update_user_balance(user_id)
    if new_balance is None:
        raise HTTPException(status_code=404, detail="User not found")

    return {"tg_id": tg_id, "new_balance": new_balance}

@router.get("/users/{tg_id}/income")
async def get_user_income(tg_id: int):
    user_id = await rq.get_user_id(tg_id)
    income = await rq.get_user_income(user_id)
    return {"income": income}
