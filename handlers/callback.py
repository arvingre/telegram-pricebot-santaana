


from telegram.ext import CallbackQueryHandler, ContextTypes
from services.state import user_page_state
from handlers.price import show_price_page

async def handle_page_nav(update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    if user_id not in user_page_state:
        await query.edit_message_text("Session expired. Please send /price again.")
        return
    page, category = user_page_state[user_id]
    if query.data == "next_page":
        page += 1
    elif query.data == "prev_page":
        page = max(1, page - 1)
    user_page_state[user_id] = (page, category)
    await show_price_page(query.message, context, page, category)

handler = CallbackQueryHandler(handle_page_nav, pattern="^(next_page|prev_page)$")