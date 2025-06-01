from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import random

TOKEN = "7561016807:AAGjG4IwayZLMMYSQmTs6zeLBDCgIWVemcI"  # 🔁 Replace this with your real bot token

# Store per-user click counts
user_clicks = {}

# Watch lists
box_3000_watches = [
    "Rolex Oyster Precision 6426",
    "Rolex Oysterdate Precision 6694",
    "Rolex Air-King 5500",
    "Rolex Oyster Perpetual 1002",
    "Rolex Date 1500",
    "Rolex Oyster Perpetual 6564",
    "Rolex Oyster Perpetual 6430",
    "Rolex Oyster Date 6517",
    "Rolex Oyster Perpetual 6284",
    "Rolex Oyster Perpetual 6718 (ladies)",
    "Rolex Oyster Precision 1210",
    "Rolex Oyster Perpetual Datejust 1601",
    "Rolex Oyster Royal",
    "Rolex Precision 9022",
    "Rolex Oyster Perpetual 6618",
    "Rolex Oyster Perpetual 67193",
    "Rolex Oyster Perpetual 76193 (Ladies)",
    "Rolex Oysterdate 6694 Linen Dial",
    "Rolex Oyster Perpetual 14233 (Ladies)"
]

box_7500_watches = [
    "Omega Speedmaster Moonwatch",
    "Rolex Oyster Royal",
    "Omega Moonwatch Chronograph",
    "Rolex Date 1500",
    "Omega Mission to the Moon"  # Always 5th
]

box_6000_message = "🎁 Box 6000 feature coming soon!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_clicks[user_id] = {"box_3000": 0, "box_6000": 0, "box_7500": 0}

    welcome_message = (
        "🎉 Congratulations on buying your first mystery box!\n\n"
        "Please only select the box you purchased.\n"
        "You can only open a box *10 times max* — after that, attempts will be marked invalid.\n\n"
        "Happy hunting and DM once you're done! 📩"
    )

    keyboard = [
        [InlineKeyboardButton("💵 $3000 Mystery Box", callback_data="box_3000")],
        [InlineKeyboardButton("💰 $6000 Mystery Box", callback_data="box_6000")],
        [InlineKeyboardButton("💎 $7500 Mystery Box", callback_data="box_7500")]
    ]

    await update.message.reply_text(welcome_message, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def handle_box_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    box = query.data
    user_id = query.from_user.id

    # Initialize user tracking if not set
    if user_id not in user_clicks:
        user_clicks[user_id] = {"box_3000": 0, "box_6000": 0, "box_7500": 0}

    if user_clicks[user_id][box] >= 10:
        await query.message.reply_text("❌ You've reached the maximum number of tries for this box.")
        return

    user_clicks[user_id][box] += 1
    attempt = user_clicks[user_id][box]

    if box == "box_3000":
        result = random.choice(box_3000_watches)
    elif box == "box_6000":
        result = box_6000_message
    elif box == "box_7500":
        if attempt % 5 == 0:
            result = "Omega Mission to the Moon"
        else:
            result = random.choice(box_7500_watches[:-1])
    else:
        result = "❌ Invalid box."

    open_button = [[InlineKeyboardButton(f"🔁 Open another ${box[4:]} box", callback_data=box)]]

    await query.message.reply_text(f"🎉 You got: {result}", reply_markup=InlineKeyboardMarkup(open_button))

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_box_click))
    app.run_polling()

if __name__ == "__main__":
    main()
