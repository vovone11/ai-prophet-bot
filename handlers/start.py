
from aiogram import types

async def cmd_start(message: types.Message):
    await message.answer("Привет! Я — AI-прорицатель. Готов ответить на несколько вопросов?")
