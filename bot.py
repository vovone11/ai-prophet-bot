import os
import random
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils import executor
from dotenv import load_dotenv
from openai import OpenAI
from prompts import build_prompt

load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(bot)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DB_FILE = "database.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER,
            question TEXT,
            answer TEXT,
            prediction TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()
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
    data = user_data.get(uid)

    if not data:
        await message.answer("Пожалуйста, начни с команды /start")
        return

    step = data["step"]
    key, _ = questions[step]
    data["answers"][key] = message.text
    data["step"] += 1

    if data["step"] < len(questions):
        next_question = questions[data["step"]][1]
        await message.answer(next_question)
    else:
        await message.answer("Анализирую твое будущее... 🔮")

        prompt = build_prompt(data["answers"])
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            result = response.choices[0].message.content
            await message.answer(result, reply_markup=ReplyKeyboardRemove())

            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            for qkey, qtext in questions:
                c.execute("INSERT INTO users (telegram_id, question, answer, prediction) VALUES (?, ?, ?, ?)",
                          (uid, qkey, data["answers"].get(qkey), result))
            conn.commit()
            conn.close()
        except Exception as e:
            await message.answer("Произошла ошибка при обращении к ИИ 😔")
            print(e)

        del user_data[uid]

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)