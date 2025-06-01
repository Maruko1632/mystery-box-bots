from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import random

TOKEN = "7561016807:AAGjG4IwayZLMMYSQmTs6zeLBDCgIWVemcI"  # ← Replace with your actual bot token

# Click counter for box_7500
box_7500_clicks = 0

# Watch lists
box_3000_watches = [
    "Rolex Oyster Precision 6426", "Rolex Oysterdate Precision 6694", "Rolex Air-King 5500",
    "Rolex Oyster Perpetual 1002", "Rolex Date 1500", "Rolex Oyster Perpetual 6564",
    "Rolex Oyster Perpetual 6430", "Rolex Oyster Date 6517", "Rolex Oyster Perpetual 6284",
    "Rolex Oyster Perpetual 6718 (Ladies)", "Rolex Oyster Precision 1210",
    "Rolex Oyster Perpetual Datejust 1601", "Rolex Oyster Royal", "Rolex Precision 9022",
    "Rolex Oyster Perpetual 6618", "Rolex Oyster Perpetual 67193",
    "Rolex Oyster Perpetual 76193 (Ladies)", "Rolex Oysterdate 6694 Linen Dial",
    "Rolex Oyster Perpetual 14233 (Ladies)"
]

box_6000_watches = [
    "Omega Seamaster 300M", "Tudor Black Bay 58", "Breitling Navitimer",
    "IWC Mark XVIII", "Tag Heuer Carrera", "Longines Spirit Zulu",
    "Zenith Elite", "Tudor Pelagos", "Cartier Santos", "Panerai Luminor Base"
]

box_7500_watches = [
    "Omega Speedmaster Moonwatch",  # Reserved for every 5th click
    "Rolex Oyster Royal", "Omega Moonwatch Chronograph",
    "Rolex Date 1500", "Omega Mission to the Moon"
]

# Welcome message
WELCOME_MSG = (
    "🎉 Congratulations on buying your first mystery box!\n\n"
    "📦 Make sure to only select the box you purchased.\n"
    "🔁 You can only change it up to *10 times* — after that, changes will be invalid.\n\n"
    "💬 Contact us once you're done.\n"
    "🔍 Happy hunting!"
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💵 $3000 Mystery Box", callback_data="box_3000")],
        [InlineKeyboardButton("💰 $6000 Mystery Box", callback_data="box_6000")],
        [InlineKeyboardButton("💎 $7500 Mystery Box", callback_data="box_7500")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(WELCOME_MSG, reply_markup=reply_markup)

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global box_7500_clicks

    query = update.callback_query
    await query.answer()
    box = query.data

    if box == "box_3000":
        selected_watch = random.choice(box_3000_watches)
    elif box == "box_6000":
        selected_watch = random.choice(box_6000_watches)
    elif box == "box_7500":
        box_7500_clicks += 1
        if box_7500_clicks % 5 == 0:
            selected_watch = "Omega Speedmaster Moonwatch"
        else:
            selected_watch = random.choice(box_7500_watches[1:])  # exclude first
    else:
        selected_watch = "Error: This box is currently unavailable."

    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=f"🎁 You got: *{selected_watch}*\n\nDM for more info!",
        parse_mode="Markdown"
    )

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_button))
    app.run_polling()

if __name__ == "__main__":
    main()
