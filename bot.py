from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from fastapi import FastAPI
from aiogram import Bot
from dotenv import load_dotenv
import logging
from aiohttp import ClientSession
from aiogram.types import Update
import os
from openai import OpenAI
from contextlib import asynccontextmanager

from prompts import build_prompt

load_dotenv()
logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv('BOT_TOKEN')
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if API_TOKEN is None:
    raise ValueError("BOT_TOKEN не найден в .env")

if OPENAI_API_KEY is None:
    raise ValueError("OPENAI_API_KEY не найден в .env")

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

client = OpenAI(api_key=OPENAI_API_KEY)

class Form(StatesGroup):
    age = State()
    gender = State()
    job = State()
    health = State()
    food = State()
    goals = State()
    routine = State()
    lifestyle = State()
    social = State()

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message, state: FSMContext):
    await state.set_state(Form.age)
    await message.reply("Привет! Я твой AI-прорицатель. Сколько тебе лет?")

@dp.message_handler(state=Form.age)
async def process_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(state=Form.gender)
    await message.reply("Какой у тебя пол?")

@dp.message_handler(state=Form.gender)
async def process_gender(message: types.Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await state.set_state(state=Form.job)
    await message.reply("Какая у тебя профессия?")

@dp.message_handler(state=Form.job)
async def process_job(message: types.Message, state: FSMContext):
    await state.update_data(job=message.text)
    await state.set_state(state=Form.health)
    await message.reply("Какое у тебя здоровье?")

@dp.message_handler(state=Form.health)
async def process_health(message: types.Message, state: FSMContext):
    await state.update_data(health=message.text)
    await state.set_state(state=Form.food)
    await message.reply("Какое у тебя питание?")

@dp.message_handler(state=Form.food)
async def process_food(message: types.Message, state: FSMContext):
    await state.update_data(food=message.text)
    await state.set_state(state=Form.goals)
    await message.reply("Какие у тебя цели?")

@dp.message_handler(state=Form.goals)
async def process_goals(message: types.Message, state: FSMContext):
    await state.update_data(goals=message.text)
    await state.set_state(state=Form.routine)
    await message.reply("Опиши свой распорядок дня.")

@dp.message_handler(state=Form.routine)
async def process_routine(message: types.Message, state: FSMContext):
    await state.update_data(routine=message.text)
    await state.set_state(state=Form.lifestyle)
    await message.reply("Какой у тебя образ жизни?")

@dp.message_handler(state=Form.lifestyle)
async def process_lifestyle(message: types.Message, state: FSMContext):
    await state.update_data(lifestyle=message.text)
    await state.set_state(state=Form.social)
    await message.reply("Есть ли у тебя социальные связи?")

@dp.message_handler(state=Form.social)
async def process_social(message: types.Message, state: FSMContext):
    await state.update_data(social=message.text)
    user_data = await state.get_data()
    prompt = build_prompt(user_data)
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.7
        )
        answer = response.choices[0].message.content
        await message.reply("Вот твой прогноз будущего:" + answer)
    except Exception as e:
        logging.error(f"Ошибка OpenAI: {e}")
        await message.reply("Произошла ошибка. Попробуй позже.")
    await state.finish()

WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/webhook")
WEBHOOK_URL = f"{os.getenv('WEBHOOK_HOST')}{WEBHOOK_PATH}"
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.getenv("PORT", 8000))

@asynccontextmanager
async def lifespan(app: FastAPI):
    await bot.set_webhook(WEBHOOK_URL)
    logging.info(f"Webhook установлен: {WEBHOOK_URL}")
    yield
    await bot.delete_webhook()
    logging.info("Webhook удалён")

app = FastAPI(lifespan=lifespan)

@app.post("/webhook")
async def telegram_webhook(update: dict):
    telegram_update = Update(**update)
    Bot.set_current(bot)
    await dp.process_update(telegram_update)
    return {"ok": True}

@app.api_route("/", methods=["GET", "HEAD"])
async def root():
    return {"status": "ok", "message": "AI-прорицатель работает"}

# Запуск webhook для aiogram
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=WEBAPP_HOST, port=WEBAPP_PORT)
