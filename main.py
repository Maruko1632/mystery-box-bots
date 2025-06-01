from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os, random
from telegram import Update

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💵 $3000 Mystery Box", callback_data="box_3000")],
        [InlineKeyboardButton("💰 $6000 Mystery Box", callback_data="box_6000")],
        [InlineKeyboardButton("💎 $7500 Mystery Box", callback_data="box_7500")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose your mystery box:", reply_markup=reply_markup)

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    box = query.data

    if box in ['box_3000', 'box_6000', 'box_7500']:
        folder_path = os.path.join("images", box)
        files = os.listdir(folder_path)
        if not files:
            await query.edit_message_text("No watches available in this box yet.")
            return

        selected_file = random.choice(files)
        photo_path = os.path.join(folder_path, selected_file)

        await context.bot.send_photo(chat_id=query.message.chat_id, photo=open(photo_path, 'rb'),
                                     caption="🎉 Congratulations! DM for more information.")
    else:
        await query.edit_message_text("Invalid box selected.")
from telegram.ext import Application

def main():
    TOKEN = "7561016807:AAGjG4IwayZLMMYSQmTs6zeLBDCgIWVemcI"
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_button))

    app.run_polling()

if __name__ == '__main__':
    main()
