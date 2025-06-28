import logging
import os
import gspread
import telegram
import base64
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from oauth2client.service_account import ServiceAccountCredentials

b64_data = os.getenv("GOOGLE_CREDENTIALS_B64")
if b64_data:
    with open("google-credentials.json", "wb") as f:
        f.write(base64.b64decode(b64_data))
else:
    raise ValueError("GOOGLE_CREDENTIALS_B64 is not set")


# === CONFIG ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
SHEET_URL = os.getenv("SHEET_URL")
GOOGLE_CREDENTIALS_JSON = "google-credentials.json"

# === Logging ===
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# === Sheets Setup ===
def get_sheet_data():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_CREDENTIALS_JSON, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(SHEET_URL).sheet1
    return sheet.get_all_records()

# === Bot Handlers ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Send /price to get the product list with images.")

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        records = get_sheet_data()
        count = 0
        for row in records:
            product = row.get("Product", "")
            price = row.get("Price", "")
            unit = row.get("Unit", "")
            name_cn = row.get("中文名称", "")
            image = row.get("Image Formula (Google Sheets)", "")

            if 'IMAGE("' in image:
                img_url = image.split('IMAGE("')[1].split('"')[0]
            else:
                img_url = None

            text = f"📦 {product} / {name_cn}\n💰 {price} / {unit}"
            if img_url:
                await update.message.reply_photo(photo=img_url, caption=text)
            else:
                await update.message.reply_text(text)

            count += 1
            if count >= 10:
                break

    except Exception as e:
        await update.message.reply_text(f"❌ Error fetching prices: {e}")

# === Main App ===
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", price))
    print("Bot is running...")
    app.run_polling()
