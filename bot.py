import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler
import sqlite3
from config import BOT_TOKEN, OPENAI_TOKEN
import openai

openai.api_key = OPENAI_TOKEN

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Стейты
ASK_NAME, ASK_AGE, ASK_HABITS = range(3)

# База данных
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER, habits TEXT)")
conn.commit()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Привет! Я AI-Прорицатель. Как тебя зовут?")
    return ASK_NAME

async def ask_age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Сколько тебе лет?")
    return ASK_AGE

async def ask_habits(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["age"] = update.message.text
    await update.message.reply_text("Какие у тебя привычки? (например: спорт, курение, медитация...)")
    return ASK_HABITS

async def show_result(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["habits"] = update.message.text
    name = context.user_data["name"]
    age = context.user_data["age"]
    habits = context.user_data["habits"]

    # Сохраняем в БД
    cursor.execute("INSERT INTO users (name, age, habits) VALUES (?, ?, ?)", (name, age, habits))
    conn.commit()

    await update.message.reply_text(f"Спасибо, {name}! Я предсказываю, что при текущем образе жизни у тебя большие перспективы 😉")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Опрос отменён. Увидимся позже!")
    return ConversationHandler.END

if __name__ == "__main__":
    import os
    TOKEN = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_age)],
            ASK_AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_habits)],
            ASK_HABITS: [MessageHandler(filters.TEXT & ~filters.COMMAND, show_result)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    app.run_polling()
