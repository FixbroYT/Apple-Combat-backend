import asyncio
import time

import uvicorn
from aiogram import Dispatcher, Bot
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.models import init_db
from app.handlers import rt
from config import BOT_TOKEN
from api_endpoints import router

time.sleep(3) #waiting for db

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
    print("Bot started!")
    await init_db()
    dp.include_router(rt)
    await dp.start_polling(bot)

async def start_all():
    bot_task = asyncio.create_task(start_bot())
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, loop="asyncio")
    server = uvicorn.Server(config)
    api_task = asyncio.create_task(server.serve())

    await asyncio.gather(bot_task, api_task)

if __name__ == "__main__":
    try:
        asyncio.run(start_all())
    except KeyboardInterrupt:
        print("Exit.")
