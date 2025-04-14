from sqlalchemy import select

from app.database.models import async_session, User, UserUpgrade, Upgrade

async def buy_upgrade(user_id, upgrade_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))
        upgrade = await session.scalar(select(Upgrade).where(Upgrade.id == upgrade_id))
        user_upgrade = await session.scalar(select(UserUpgrade).where(UserUpgrade.user_id == user_id, UserUpgrade.upgrade_id == upgrade_id))

        if not upgrade:
            return None

        upgrade_cost = upgrade.cost
        if user_upgrade:
            upgrade_cost *= user_upgrade.count

        if user.coins >= upgrade_cost:
            user.coins -= upgrade_cost
            await session.flush()
            await session.commit()
        else:
            return None

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

async def get_all_upgrades():
    async with async_session() as session:
        upgrades = await session.scalars(select(Upgrade))

        if not upgrades:
            return None

        response = []

        for upgrade in upgrades:
            response.append({"id": upgrade.id, "name": upgrade.name, "description": upgrade.description, "cost": upgrade.cost, "bonus": upgrade.bonus})

        return response

async def get_upgrade_name(upgrade_id):
    async with async_session() as session:
        upgrade = await session.scalar(select(Upgrade).where(Upgrade.id == upgrade_id))

        if not upgrade:
            return None

        upgrade_name = upgrade.name
        return upgrade_name