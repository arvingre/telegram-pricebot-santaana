


from telegram.ext import CommandHandler, ContextTypes
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from services.sheet import get_sheet_data
from services.state import user_page_state
from utils.paginator import paginate_products

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    category_filter = " ".join(context.args) if context.args else None
    page = 1
    user_page_state[user_id] = (page, category_filter)
    await show_price_page(update, context, page, category_filter)

async def show_price_page(update, context, page, category=None):
    records = get_sheet_data()
    if category:
        records = [r for r in records if r.get("Category", "").lower() == category.lower()]
    total = len(records)
    if total == 0:
        await update.message.reply_text("No products found.")
        return
    items = paginate_products(records, page)
    for row in items:
        text = f"📦 {row.get('Product','')} / {row.get('中文名称','')}\n💰 {row.get('Price','')} / {row.get('Unit','')}"
        image = row.get("Image Formula (Google Sheets)", "")
        if 'IMAGE("' in image:
            url = image.split('IMAGE("')[1].split('"')[0]
            await update.message.reply_photo(photo=url, caption=text)
        else:
            await update.message.reply_text(text)
    buttons = []
    if page > 1:
        buttons.append(InlineKeyboardButton("⬅️ Prev", callback_data="prev_page"))
    if page * 5 < total:
        buttons.append(InlineKeyboardButton("➡️ Next", callback_data="next_page"))
    if buttons:
        await update.message.reply_text("Page controls:", reply_markup=InlineKeyboardMarkup([buttons]))

handler = CommandHandler("price", price)