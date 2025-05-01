import os
import openai
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

user_usage = {}
MAX_QUESTIONS = 50
MAX_TOKENS = 1000

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Kirim pertanyaan kamu ke Casper. Maksimal 50 kali ya.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)

    if user_id not in user_usage:
        user_usage[user_id] = 0

    if user_usage[user_id] >= MAX_QUESTIONS:
        await update.message.reply_text("Kamu sudah mencapai batas 50 pertanyaan. Coba lagi besok ya.")
        return

    user_usage[user_id] += 1

    try:
        user_message = update.message.text
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            max_tokens=MAX_TOKENS,
            messages=[{"role": "user", "content": user_message}]
        )
        reply = response["choices"][0]["message"]["content"]
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text("Error: " + str(e))

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
