from telegram.ext import CommandHandler, ContextTypes
from telegram import Update
from services.sheet import get_categories

async def categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        cats = get_categories()
        if not cats:
            await update.message.reply_text("No categories found.")
            return
        await update.message.reply_text("📂 Available Categories:\n" + "\n".join(f"🔹 {c}" for c in cats))
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

handler = CommandHandler("categories", categories)
