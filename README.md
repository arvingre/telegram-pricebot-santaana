# Telegram Price Bot

This bot reads product listings from a Google Sheets file and displays them in Telegram via `/price`.

## 📦 Features

- Shows product name, price, unit, Chinese name, and image
- Reads live data from Google Sheets
- Deployable on Railway or any VPS

## 🛠 Setup

1. Create a `.env` file:
```
BOT_TOKEN=your_telegram_bot_token
SHEET_URL=your_google_sheet_url
```

2. Add `google-credentials.json` to root directory.

3. Run:
```
pip install -r requirements.txt
python main.py
```
# telegram-pricebot-santaana
