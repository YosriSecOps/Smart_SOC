from telegram.ext import ApplicationBuilder, MessageHandler, filters
from telegram import Update
from telegram.ext import ContextTypes
import os
from soc_agent import ask_llm, run_command

TOKEN = os.getenv("TELEGRAM_TOKEN")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_message = update.message.text

    # special commands
    if user_message.startswith("run "):
        response = run_command(user_message[4:])

    elif user_message == "read alerts":
        response = run_command(
            "cat /var/ossec/logs/alerts/alerts.json | tail -n 30"
        )

    else:
        response = ask_llm(user_message)

    # telegram max size protection
    if len(response) > 4000:
        response = response[:4000]

    await update.message.reply_text(response)


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT, handle))

print("[+] Telegram SOC Agent started...")

app.run_polling()
