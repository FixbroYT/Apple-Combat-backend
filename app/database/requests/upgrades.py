from sqlalchemy import select

from app.database.models import async_session, User, UserUpgrade, Upgrade

async def buy_upgrade(user_id, upgrade_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))
        upgrade = await session.scalar(select(Upgrade).where(Upgrade.id == upgrade_id))
        user_upgrade = await session.scalar(select(UserUpgrade).where(UserUpgrade.user_id == user_id, UserUpgrade.upgrade_id == upgrade_id))
        upgrade_cost = await get_user_upgrade_cost(user_id, upgrade_id)

        if not upgrade or not upgrade_cost:
            return None

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

async def get_user_upgrade_cost(user_id, upgrade_id):
    async with async_session() as session:
        upgrade = await session.scalar(select(Upgrade).where(Upgrade.id == upgrade_id))
        user_upgrade = await session.scalar(select(UserUpgrade).where(UserUpgrade.user_id == user_id, UserUpgrade.upgrade_id == upgrade_id))

        if not upgrade:
            return None
        if not user_upgrade:
            return upgrade.cost

        upgrade_cost = upgrade.cost * user_upgrade.count

        return upgrade_cost

async def passive_income_loop():
    while True:
        async with async_session() as session:
            users = await session.scalars(select(User).join(UserUpgrade).where(UserUpgrade.upgrade_id == 2))
            upgrade = await session.scalar(select(Upgrade).where(Upgrade.id == 2))

            if not users or not upgrade:
                return None

            for user in users:
                user_upgrade = await session.scalar(select(UserUpgrade).where(UserUpgrade.user_id == user.id, UserUpgrade.upgrade_id == 2))
                if not user_upgrade:
                    return None

                user.coins += upgrade.bonus * user_upgrade.count
                await session.flush()
                await session.commit()