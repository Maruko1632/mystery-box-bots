import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    ContextTypes, Application
)

# START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💵 $3000 Mystery Box", callback_data="box_3000")],
        [InlineKeyboardButton("💰 $6000 Mystery Box", callback_data="box_6000")],
        [InlineKeyboardButton("💎 $7500 Mystery Box", callback_data="box_7500")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose your mystery box:", reply_markup=reply_markup)

# HANDLE BUTTON SELECTION
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    box = query.data

    folder_path = os.path.join("images", box)
    if not os.path.exists(folder_path):
        await query.edit_message_text("Invalid box selected.")
        return

    files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
    if not files:
        await query.edit_message_text("No watches available in this box yet.")
        return

    selected_file = random.choice(files)
    photo_path = os.path.join(folder_path, selected_file)

    with open(photo_path, "rb") as photo:
        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=photo,
            caption="🎉 Congratulations! 👏\nDM for more information."
        )

# MAIN WEBHOOK APP
def main():
    TOKEN = os.getenv("7561016807:AAGjG4IwayZLMMYSQmTs6zeLBDCgIWVemcI")
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_button))

    PORT = int(os.environ.get("PORT", 8443))
    URL = f"https://{os.environ.get('RAILWAY_STATIC_URL')}/"

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=URL,
    )

if __name__ == "__main__":
    main()
