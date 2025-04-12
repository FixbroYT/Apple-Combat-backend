from sqlalchemy import select

from app.database.models import async_session, User, Location, UserLocation, UserUpgrade, Upgrade


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
        await add_location_connection(user_id, 1)
        return {"success": True}

async def get_user_id(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            return None

        user_id = user.id
        return user_id

async def add_location_connection(user_id, location_id):
    async with async_session() as session:
        location = await session.scalar(select(Location).where(Location.id == location_id))

        if not location:
            return None

        new_connection = UserLocation(user_id=user_id, location_id=location_id)
        session.add(new_connection)
        await session.flush()
        await session.commit()

async def buy_location(user_id, location_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))
        location = await session.scalar(select(Location).where(Location.id == location_id))

        if not location:
            return {"success": False}

        if user.coins >= location.cost:
            user.coins -= location.cost
            await session.flush()
            await session.commit()
        else:
            return {"success": False}

        await add_location_connection(user_id, location_id)
        owned_locations = await session.scalars(select(UserLocation).where(UserLocation.user_id == user_id))
        owned_locations_id = []

        for owned_location in owned_locations:
            owned_locations_id.append(owned_location.location_id)

        response = {
            "success": True,
            "new_coins": user.coins,
            "owned_locations":  owned_locations_id
        }

        return response

async def change_current_location(user_id, location_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))

        if not user:
            return {"success": False}

        location = await session.scalar(select(UserLocation).where(UserLocation.user_id == user_id, UserLocation.location_id == location_id))

        if not location:
            return None

        user.location_id = location_id
        await session.commit()

        location_name = await get_location_name(user.location_id)

        return {
            "success": True,
            "current_location": location_name
        }

async def buy_upgrade(user_id, upgrade_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))

        if not user:
            return {"success": False}

        upgrade = await session.scalar(select(Upgrade).where(Upgrade.id == upgrade_id))

        if not upgrade:
            return {"success": False}

        if user.coins >= upgrade.cost:
            user.coins -= upgrade.cost
            await session.flush()
            await session.commit()
        else:
            return {"success": False}

        user_upgrade = await session.scalar(select(UserUpgrade).where(UserUpgrade.user_id == user_id, UserUpgrade.upgrade_id == upgrade_id))

        if not user_upgrade:
            new_connection = UserUpgrade(user_id=user_id, upgrade_id=upgrade_id)
            session.add(new_connection)
            await session.flush()
            await session.commit()
            count = 1
        else:
            user_upgrade.count += 1
            await session.flush()
            await session.commit()
            count = user_upgrade.count

        response = {"success": True, "new_coins": user.coins, "upgrade_count": count}
        return response

async def get_user_balance(user_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))

        if not user:
            return None

        balance = user.coins
        return balance

async def update_user_balance(user_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))
        amount = await get_user_income(user_id)

        if not user:
            return None

        user.coins += amount
        await session.commit()
        return user.coins

async def get_location_name(location_id):
    async with async_session() as session:
        location = await session.scalar(select(Location).where(Location.id == location_id))

        if not location:
            return None

        location_name = location.name
        return location_name

async def get_user(user_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))

        location_name = await get_location_name(user.location_id)
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
            upgrade_name = await get_upgrade_name(upgrade.upgrade_id)

            response.append({
                "id": upgrade.id, "name": upgrade_name, "count": upgrade.count
            })

        return response

async def get_upgrade_name(upgrade_id):
    async with async_session() as session:
        upgrade = await session.scalar(select(Upgrade).where(Upgrade.id == upgrade_id))

        if not upgrade:
            return None

        upgrade_name = upgrade.name
        return upgrade_name

async def get_user_locations(user_id):
    async with async_session() as session:
        user_locations = await session.scalars(select(UserLocation).where(UserLocation.user_id == user_id))

        response = []
        for user_location in user_locations:
            location_name = await get_location_name(user_location.location_id)
            response.append(location_name)

        return response

async def get_all_upgrades():
    async with async_session() as session:
        upgrades = await session.scalars(select(Upgrade))

        if not upgrades:
            return None

        response = []

        for upgrade in upgrades:
            response.append({"id": upgrade.id, "name": upgrade.name, "description": upgrade.description, "cost": upgrade.cost, "bonus": upgrade.bonus})

        return response

async def get_all_locations():
    async with async_session() as session:
        locations = await session.scalars(select(Location))

        if not locations:
            return None

        response = []

        for location in locations:
            response.append({"id": location.id, "name": location.name, "bonus_multiplier": location.bonus_multiplier})

        return response

async def get_location_bonus(location_id):
    async with async_session() as session:
        location = await session.scalar(select(Location).where(Location.id == location_id))

        if not location:
            return None

        location_bonus = location.bonus
        return location_bonus

async def get_user_income(user_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))
        amount = 1

        if not user:
            return None

        upgrade_1 = await session.scalar(select(UserUpgrade).where(UserUpgrade.user_id == user_id, UserUpgrade.upgrade_id == 1))
        upgrade_1_bonus = await session.scalar(select(Upgrade).where(Upgrade.id == 1))
        upgrade_1_bonus = upgrade_1_bonus.bonus

        if upgrade_1:
            amount = (upgrade_1.count * upgrade_1_bonus) + amount

        location_id = user.location_id
        location_bonus = await session.scalar(select(Location).where(Location.id == location_id))
        location_bonus = location_bonus.bonus_multiplier

        if location_bonus:
            amount *= location_bonus

        amount = round(amount)

        return amount