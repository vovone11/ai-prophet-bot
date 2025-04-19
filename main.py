
from aiogram import Bot, Dispatcher, executor, types
from handlers import register_handlers
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

register_handlers(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
