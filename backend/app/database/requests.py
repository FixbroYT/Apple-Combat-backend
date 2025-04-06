from sqlalchemy import select

from backend.app.database.models import async_session, User


async def add_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if user:
            return None


        new_user = User(tg_id=tg_id)
        session.add(new_user)
        await session.flush()
        await session.commit()

async def get_user_balance(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            return None

        balance = user.balance
        return balance

async def update_user_balance(tg_id, amount):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            return None

        user.balance += amount
        await session.commit()