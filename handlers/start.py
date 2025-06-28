from telegram.ext import CommandHandler, ContextTypes
from telegram import Update

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Santa Ana Fresh Supply Bot!\n"
        "Use /price to view product list.\n"
        "Use /categories to browse by category.\n"
        "Tap buttons to flip pages or view more."
    )

handler = CommandHandler("start", start)
