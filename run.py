import asyncio

from aiogram import Dispatcher, Bot
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.models import init_db
from app.handlers import rt
from config import BOT_TOKEN
from api_endpoints import router


dp = Dispatcher()
bot = Bot(BOT_TOKEN)
app = FastAPI()

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def start_bot():
    await init_db()
    dp.include_router(rt)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        print("Выход.")
