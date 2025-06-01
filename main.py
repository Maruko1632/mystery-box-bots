import os
import random
from pathlib import Path
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOX_TIERS = {
    "box_3000": "images/box_3000",
    "box_6000": "images/box_6000",
    "box_7500": "images/box_7500",
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎁 $3,000 Box", callback_data="box_3000")],
        [InlineKeyboardButton("🎁 $6,000 Box", callback_data="box_6000")],
        [InlineKeyboardButton("🎁 $7,500 Box", callback_data="box_7500")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose your mystery box:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    box_type = query.data
    folder_path = BOX_TIERS.get(box_type)

    if folder_path and Path(folder_path).exists():
        images = list(Path(folder_path).glob("*"))
        if images:
            selected_image = random.choice(images)
            await query.message.reply_photo(
                photo=InputFile(selected_image),
                caption="🎉 Congratulations! DM us for more info."
            )
        else:
            await query.message.reply_text("No watches found for this box yet.")
    else:
        await query.message.reply_text("Invalid box selected.")

def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        token = "7561016807:AAGjG4IwayZLMMYSQmTs6zeLBDCgIWVemcI"
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()

if __name__ == "__main__":
    main()
