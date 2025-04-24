from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.dispatcher.filters import Text
from prompts import build_prompt
from database import save_user_data  # Импортируем функцию для сохранения данных в БД

# Функция для обработки возрастного ответа
async def process_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state("gender")
    await message.reply("Какой у вас пол?")

# Функция для обработки ответа на пол
async def process_gender(message: Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await state.set_state("job")
    await message.reply("Какую профессию вы занимаете?")

# Функция для обработки ответа на профессию
async def process_job(message: Message, state: FSMContext):
    await state.update_data(job=message.text)
    await state.set_state("health")
    await message.reply("Как вы оцениваете свое здоровье?")

# Функция для обработки ответа на здоровье
async def process_health(message: Message, state: FSMContext):
    await state.update_data(health=message.text)
    await state.set_state("food")
    await message.reply("Как вы питаетесь?")

# Функция для обработки ответа на питание
async def process_food(message: Message, state: FSMContext):
    await state.update_data(food=message.text)
    await state.set_state("goals")
    await message.reply("Какие у вас цели?")

# Функция для обработки ответа на цели
async def process_goals(message: Message, state: FSMContext):
    await state.update_data(goals=message.text)
    await state.set_state("goals")
    await message.reply("Какие у вас распорядок дня?")

# Функция для обработки ответа на распорядок дня
async def process_routine(message: Message, state: FSMContext):
    await state.update_data(routine=message.text)
    await state.set_state("lifestyle")
    await message.reply("Какой у вас образ жизни?")

# Функция для обработки ответа на образ жизни
async def process_lifestyle(message: Message, state: FSMContext):
    await state.update_data(lifestyle=message.text)
    await state.set_state("social")
    await message.reply("Есть ли у вас социальные связи?")

# Функция для обработки ответа на социальные связи
async def process_social(message: Message, state: FSMContext):
    await state.update_data(social=message.text)

    # Собираем все данные пользователя
    user_data = await state.get_data()

    # Сохраняем данные пользователя в базу данных
    save_user_data(user_data)

    # Генерация промпта для предсказания
    prompt = build_prompt(user_data)

    # Отправляем финальное предсказание пользователю
    await message.reply(prompt)

    # Закрываем состояние
    await state.finish()