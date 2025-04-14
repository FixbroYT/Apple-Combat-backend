from sqlalchemy import select

from app.database.models import async_session, User, Location, UserLocation

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
            return None

        if user.coins >= location.cost:
            user.coins -= location.cost
            await session.flush()
            await session.commit()
        else:
            return None

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

async def get_location_name(location_id):
    async with async_session() as session:
        location = await session.scalar(select(Location).where(Location.id == location_id))

        if not location:
            return None

        location_name = location.name
        return location_name

async def get_location_bonus(location_id):
    async with async_session() as session:
        location = await session.scalar(select(Location).where(Location.id == location_id))

        if not location:
            return None

        location_bonus = location.bonus
        return location_bonus

async def get_all_locations():
    async with async_session() as session:
        locations = await session.scalars(select(Location))

        if not locations:
            return None

        response = []

        for location in locations:
            response.append({"id": location.id, "name": location.name, "bonus_multiplier": location.bonus_multiplier})

        return response
