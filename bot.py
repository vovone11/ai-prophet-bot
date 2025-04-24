from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Command, Text
import logging
import os
from dotenv import load_dotenv  # Подключаем dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv('BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if API_TOKEN is None:
    raise ValueError("BOT_TOKEN не найден в файле .env")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY не найден в файле .env")


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Подключаем хранилище состояний (MemoryStorage для тестирования)
from aiogram.contrib.fsm_storage.memory import MemoryStorage
storage = MemoryStorage()
dp.storage = storage  # Подключаем хранилище

class Form(StatesGroup):
    age = State()  # Стартовый вопрос (возраст)
    gender = State()  # Следующий вопрос (пол)
    job = State()  # Следующий вопрос (профессия)
    routine = State()
    lifestyle = State()
    health = State()
    food = State()
    goals = State()
    social = State()

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    """
    Отправка первого вопроса: возраст.
    """
    await Form.age.set()
    await message.reply("Привет! Я твой AI-прорицатель. Скажи, сколько тебе лет?")

# Обработчик получения возраста
@dp.message_handler(state=Form.age)
async def process_age(message: types.Message, state: FSMContext):
    """
    Обрабатываем введенный возраст и переходим к следующему вопросу (пол).
    """
    logging.info(f"Получен возраст: {message.text}")
    await state.update_data(age=message.text)
    await Form.next()  # Переход к следующему состоянию
    logging.info("Переход к следующему вопросу: пол")
    await message.reply("Какой у тебя пол?")

# Обработчик получения пола
@dp.message_handler(state=Form.gender)
async def process_gender(message: types.Message, state: FSMContext):
    """
    Обрабатываем введенный пол и переходим к следующему вопросу (профессия).
    """
    logging.info(f"Получен пол: {message.text}")
    await state.update_data(gender=message.text)
    await Form.next()  # Переход к следующему состоянию
    logging.info("Переход к следующему вопросу: профессия")
    await message.reply("Какая у тебя профессия?")

# Обработчик получения профессии
@dp.message_handler(state=Form.job)
async def process_job(message: types.Message, state: FSMContext):
    """
    Обрабатываем введенную профессию и переходим к следующему вопросу (например, здоровье).
    """
    logging.info(f"Получена профессия: {message.text}")
    await state.update_data(job=message.text)
    data = await state.get_data()
    if 'health' not in data:
        await Form.next()  # Переход к следующему состоянию
        logging.info("Переход к следующему вопросу: здоровье")
        await message.reply("Какое у тебя здоровье?")
    else:
        # Если все вопросы пройдены, можно завершить
        await message.reply("Спасибо за информацию! Я сформирую прогноз.")
        # Генерация прогноза и завершение процесса
        await state.finish()

# Обработчик получения информации о здоровье
@dp.message_handler(state=Form.health)
async def process_health(message: types.Message, state: FSMContext):
    """
    Обрабатываем информацию о здоровье и переходим к следующему вопросу (например, питание).
    """
    logging.info(f"Получено состояние здоровья: {message.text}")
    await state.update_data(health=message.text)
    await Form.next()
    logging.info("Переход к следующему вопросу: питание")
    await message.reply("Какое у тебя питание?")

# Обработчик получения питания
@dp.message_handler(state=Form.food)
async def process_food(message: types.Message, state: FSMContext):
    """
    Обрабатываем информацию о питании и переходим к следующему вопросу (например, социальные связи).
    """
    logging.info(f"Получено питание: {message.text}")
    await state.update_data(food=message.text)
    await Form.next()
    logging.info("Переход к следующему вопросу: информация о целях")
    await message.reply("Какие у тебя цели?")

# Обработчик получения информации о целях
@dp.message_handler(state=Form.goals)
async def process_social(message: types.Message, state: FSMContext):
    """
    Обрабатываем информацию о целях.
    """
    logging.info(f"Получены цели: {message.text}")
    await state.update_data(goals=message.text)
    await Form.next()
    logging.info("Переход к следующему вопросу: распорядок дня")
    await message.reply("Опиши свой распорядок дня")

# Обработчик получения распорядка дня
@dp.message_handler(state=Form.goals)
async def process_social(message: types.Message, state: FSMContext):
    """
    Обрабатываем информацию о целях.
    """
    logging.info(f"Получен распорядок дня: {message.text}")
    await state.update_data(routine=message.text)
    await Form.next()
    logging.info("Переход к следующему вопросу: образ жизни")
    await message.reply("Какой у тебя образ жизни?")

    # Обработчик получения образа жизни
@dp.message_handler(state=Form.goals)
async def process_social(message: types.Message, state: FSMContext):
    """
    Обрабатываем информацию о целях.
    """
    logging.info(f"Получен образ жизни: {message.text}")
    await state.update_data(lifestyle=message.text)
    await Form.next()
    logging.info("Переход к следующему вопросу: социальные связи")
    await message.reply("Есть ли у тебя социальные связи?")

# Обработчик получения информации о социальных связях
@dp.message_handler(state=Form.social)
async def process_social(message: types.Message, state: FSMContext):
    """
    Обрабатываем информацию о социальных связях и завершаем сбор данных.
    """
    logging.info(f"Получены социальные связи: {message.text}")
    await state.update_data(social=message.text)
    # Завершаем процесс сбора данных, можно передать в OpenAI или обработать другие данные
    await message.reply("Спасибо за информацию! Теперь я могу сделать прогноз.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
