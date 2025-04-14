from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

import app.database.requests as requests

router = APIRouter()

class UserCreateRequest(BaseModel):
    tg_id: int


async def get_internal_user_id(tg_id: int)-> int:
    user_id = await requests.users.get_user_id(tg_id)
    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")
    return user_id


@router.get("/users/{tg_id}")
async def get_user(user_id: int = Depends(get_internal_user_id)):
    response = await requests.users.get_user(user_id)
    return response

@router.get("/upgrades")
async def get_upgrades():
    response = await requests.upgrades.get_all_upgrades()
    if not response:
        raise HTTPException(status_code=404, detail="Upgrades not found")
    return response

@router.post("/users/{tg_id}/buy_upgrade/{upgrade_id}")
async def buy_upgrade(upgrade_id: int, user_id: int = Depends(get_internal_user_id)):
    response = await requests.upgrades.buy_upgrade(user_id, upgrade_id)
    if not response:
        raise HTTPException(status_code=400, detail="Upgrade not found or not enough coins")
    return response

@router.get("/locations")
async def get_locations():
    response = await requests.locations.get_all_locations()
    if not response:
        raise HTTPException(status_code=404, detail="Locations not found")
    return response

@router.post("/users/{tg_id}/buy_location/{location_id}")
async def buy_location(location_id: int, user_id: int = Depends(get_internal_user_id)):
    response = await requests.locations.buy_location(user_id, location_id)
    if not response:
        raise HTTPException(status_code=400, detail="Location not found or not enough coins")

    return response

@router.post("/users/{tg_id}/set_location/{location_id}")
async def set_location(location_id: int, user_id: int = Depends(get_internal_user_id)):
    response = await requests.users.change_current_user_location(user_id, location_id)
    if not response:
        raise HTTPException(status_code=404, detail="Location not found")

    return response

@router.post("/users/create")
async def create_user_endpoint(data: UserCreateRequest):
    successful_creation = await requests.users.add_user(data.tg_id)
    user_id = await requests.users.get_user_id(data.tg_id)
    if not user_id or not successful_creation:
        raise HTTPException(status_code=400, detail="User already exists or creation failed")

    user = await requests.users.get_user(user_id)
    return user

@router.post("/users/{tg_id}/balance/add")
async def add_balance(tg_id: int):
    user_id = await requests.users.get_user_id(tg_id)
    new_balance = await requests.users.update_user_balance(user_id)
    if user_id is None:
        raise HTTPException(status_code=404, detail="User not found")

    return {"tg_id": tg_id, "new_balance": new_balance}

@router.get("/users/{tg_id}/income")
async def get_user_income(user_id: int = Depends(get_internal_user_id)):
    income = await requests.users.get_user_income(user_id)
    return {"income": income}
