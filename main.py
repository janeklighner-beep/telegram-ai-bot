import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

from openai import OpenAI

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я живой 🙂 Напиши мне любой вопрос.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        resp = client.responses.create(
            model="gpt-5-mini",
            input=user_text
        )
        answer = (resp.output_text or "").strip()
        if not answer:
            answer = "Не смог сформировать ответ. Попробуй переформулировать."
    except Exception as e:
        logging.exception("OpenAI error")
        answer = "Ошибка при обращении к ИИ. Проверь OPENAI_API_KEY и логи Railway."

    await update.message.reply_text(answer)

def main():
    if not BOT_TOKEN:
        raise RuntimeError("Переменная BOT_TOKEN не найдена. Добавь её в Railway Variables.")
    if not OPENAI_API_KEY:
        raise RuntimeError("Переменная OPENAI_API_KEY не найдена. Добавь её в Railway Variables.")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
