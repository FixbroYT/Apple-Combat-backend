from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo


rt = Router()

@rt.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Hello! Welcome to bot!", reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="PLAY!", web_app=WebAppInfo(url="https://applecombat-9bcee.web.app/"))]
    ]))