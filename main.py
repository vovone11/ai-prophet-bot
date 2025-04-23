import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils import executor
from dotenv import load_dotenv
import openai
from prompts import build_prompt

load_dotenv()
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(bot)
openai.api_key = os.getenv("OPENAI_API_KEY")

user_data = {}

questions = [
    ("age", "Сколько тебе лет?"),
    ("gender", "Укажи пол (М/Ж):"),
    ("job", "Чем ты занимаешься?"),
    ("routine", "Опиши свой обычный день:"),
    ("lifestyle", "Какой у тебя образ жизни (активный/сидячий)?"),
    ("health", "Как ты оцениваешь своё здоровье?"),
    ("food", "Как ты питаешься?"),
    ("goals", "Какие у тебя цели на ближайшие годы?"),
    ("social", "Есть ли у тебя близкие друзья/партнёр?"),
]

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_data[message.from_user.id] = {"step": 0, "answers": {}}
    await message.answer("Привет! Я ИИ-прорицатель. Давай узнаем, куда ты движешься.")
    await message.answer(questions[0][1])

@dp.message_handler()
async def handle_answers(message: types.Message):
    uid = message.from_user.id
    data = user_data[uid]
    step = data["step"]
    key, _ = questions[step]
    data["answers"][key] = message.text
    data["step"] += 1

    if data["step"] < len(questions):
        next_question = questions[data["step"]][1]
        await message.answer(next_question)
    else:
        await message.answer("Анализирую твое будущее...")

        prompt = build_prompt(data["answers"])
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        result = response.choices[0].message["content"]
        await message.answer(result, reply_markup=ReplyKeyboardRemove())
        del user_data[uid]

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

