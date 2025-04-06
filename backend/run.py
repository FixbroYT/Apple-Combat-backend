import asyncio

from aiogram import Dispatcher, Bot
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.database.models import init_db
from backend.app.handlers import rt
from backend.config import BOT_TOKEN
import uvicorn

from backend.server import router

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os


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


async def main():
    print("Bot started!")
    await init_db()
    dp.include_router(rt)
    await dp.start_polling(bot)


app.mount("/", StaticFiles(directory="dist", html=True), name="static")

@app.get("/{full_path:path}")
async def serve_react_app():
    file_path = os.path.join("dist", "index.html")
    return FileResponse(file_path)


async def start_all():
    bot_task = asyncio.create_task(main())
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, loop="asyncio")
    server = uvicorn.Server(config)
    api_task = asyncio.create_task(server.serve())

    await asyncio.gather(bot_task, api_task)


if __name__ == "__main__":
    try:
        asyncio.run(start_all())
    except KeyboardInterrupt:
        print("Exit.")