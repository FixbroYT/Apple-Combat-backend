from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

from backend.app.database import requests as rq

rt = Router()

@rt.message(CommandStart())
async def cmd_start(message: Message):
    await rq.add_user(message.from_user.id)
    await message.answer("Hello! Welcome to bot!")

@rt.message(Command("balance"))
async def cmd_balance(message: Message):
    user_balance = await rq.get_user_balance(message.from_user.id)
    await message.answer(f"Your current balance: {user_balance}.")