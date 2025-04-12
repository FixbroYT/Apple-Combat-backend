from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo


rt = Router()

@rt.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Hello! Welcome to bot!")