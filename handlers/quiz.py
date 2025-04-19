
from aiogram import types, Dispatcher
from utils import generate_prediction
from database import save_answers

questions = [
    "Как ты себя чувствуешь сегодня? (0-5)",
    "Сколько часов ты спал прошлой ночью?",
    "Как часто ты ощущаешь вдохновение?"
]

user_data = {}

async def start_quiz(message: types.Message):
    user_data[message.from_user.id] = {"step": 0, "answers": []}
    await message.answer(questions[0])

async def handle_answer(message: types.Message):
    user_id = message.from_user.id
    data = user_data.get(user_id)

    if data is None:
        await message.answer("Напиши /start чтобы начать сначала.")
        return

    try:
        answer = int(message.text.strip())
        data["answers"].append(answer)
        data["step"] += 1
    except ValueError:
        await message.answer("Пожалуйста, введи число.")
        return

    if data["step"] < len(questions):
        await message.answer(questions[data["step"]])
    else:
        prediction = generate_prediction(data["answers"])
        await message.answer(f"🔮 {prediction}")
        save_answers(user_id, data["answers"])
        del user_data[user_id]

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_quiz, commands=["quiz"])
    dp.register_message_handler(handle_answer)
