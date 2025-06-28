user_page_state = {}  # user_id: (page, category)
import logging
import os
from dotenv import load_dotenv
import telegram
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.ext import ApplicationHandlerStop
from handlers.start import start
from handlers.categories import categories
from handlers.price import price
from handlers.callback import handle_page_nav

load_dotenv()

# Ensure Google credentials are written after .env is loaded
from credentials.loader import ensure_google_credentials
ensure_google_credentials()

# === CONFIG ===
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable must be set")

# === Logging ===
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# === Error Handler ===
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("⚠️ Exception while handling update:", exc_info=context.error)
    if update and hasattr(update, "message"):
        await update.message.reply_text(f"❌ Internal error: {context.error}")

# === Main App ===
if __name__ == '__main__':
    from telegram.ext import CallbackQueryHandler

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_error_handler(error_handler)

    # Register handlers dynamically
    handlers = [
        CommandHandler("start", start),
        CommandHandler("price", price),
        CommandHandler("categories", categories),
        CallbackQueryHandler(handle_page_nav, pattern="^(next_page|prev_page)$"),
    ]
    for handler in handlers:
        app.add_handler(handler)

    logger.info("Bot is running...")
    print("Bot is running...")
    app.run_polling()
