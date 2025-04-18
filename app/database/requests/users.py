from random import randint

from sqlalchemy import select

from app.database.models import async_session, User, UserUpgrade, Upgrade, Location, UserLocation

import app.database.requests as requests


async def add_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if user:
            return None

        new_user = User(tg_id=tg_id, location_id=1)
        session.add(new_user)
        await session.flush()
        await session.commit()
        user_id = await get_user_id(tg_id)
        await requests.locations.add_location_connection(user_id, 1)
        return {"success": True}

async def get_user_id(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            return None

        user_id = user.id
        return user_id

async def update_user_balance(user_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))
        amount = await get_user_income(user_id)

        user.coins += amount
        await session.commit()
        return user.coins

async def get_user_balance(user_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))

        if not user:
            return None

        balance = user.coins
        return balance

async def get_user(user_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))

        location_name = await requests.locations.get_location_name(user.location_id)
        upgrades = await get_user_upgrades(user_id)
        locations = await get_user_locations(user_id)

        response = {
            "tg_id": user.tg_id,
            "coins": user.coins,
            "location": location_name,
            "upgrades": upgrades,
            "locations": locations
        }

        return response

async def get_user_upgrades(user_id):
    async with async_session() as session:
        upgrades = await session.scalars(select(UserUpgrade).where(UserUpgrade.user_id == user_id))

        response = []
        for upgrade in upgrades:
            upgrade_name = await requests.upgrades.get_upgrade_name(upgrade.upgrade_id)

            response.append({
                "id": upgrade.upgrade_id, "name": upgrade_name, "count": upgrade.count
            })

        return response

async def get_user_locations(user_id):
    async with async_session() as session:
        user_locations = await session.scalars(select(UserLocation).where(UserLocation.user_id == user_id))

        response = []
        for user_location in user_locations:
            location_name = await requests.locations.get_location_name(user_location.location_id)
            response.append(location_name)

        return response

async def get_user_income(user_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))
        amount = 1

        upgrade_1 = await session.scalar(select(UserUpgrade).where(UserUpgrade.user_id == user_id, UserUpgrade.upgrade_id == 1))
        upgrade_1_bonus = await session.scalar(select(Upgrade).where(Upgrade.id == 1))

        if upgrade_1 and upgrade_1_bonus:
            upgrade_1_bonus = upgrade_1_bonus.bonus
            amount = (upgrade_1.count * upgrade_1_bonus) + amount


        location_id = user.location_id
        location_bonus = await session.scalar(select(Location).where(Location.id == location_id))
        location_bonus = location_bonus.bonus_multiplier

        if location_bonus:
            amount *= location_bonus

        amount = round(amount)

        return amount

async def change_current_user_location(user_id, location_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))
        location = await session.scalar(select(UserLocation).where(UserLocation.user_id == user_id, UserLocation.location_id == location_id))

        if not location:
            return None

        user.location_id = location_id
        await session.commit()

        location_name = await requests.locations.get_location_name(user.location_id)

        return {
            "success": True,
            "current_location": location_name
        }

async def casino(user_id, bet):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))

        if bet > user.coins or bet > 1000 or bet < 1:
            return None

        user.coins -= bet
        await session.flush()

        random_num = randint(1, 100)

        if random_num <= 5:
            coefficient = 4
            win_amount = bet * coefficient
        elif 5 < random_num <= 20:
            coefficient = 3
            win_amount = bet * coefficient
        elif 20 < random_num <= 50:
            coefficient = 2
            win_amount = bet * coefficient
        else:
            return {"win": False, "user_coins": user.coins}

        user.coins += win_amount
        await session.flush()
        await session.commit()

        return {"win": True,"coefficient": coefficient, "win_amount": win_amount, "user_coins": user.coins}