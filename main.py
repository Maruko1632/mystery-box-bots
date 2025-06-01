from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import random

# Track user click history
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

box_6000_watches = [
    "Rolex Submariner 14060",
    "Rolex Explorer 14270",
    "Rolex Datejust 16014",
    "Rolex GMT-Master 16750",
    "Rolex Sea-Dweller 16600",
    "Rolex Milgauss 116400",
    "Rolex Yacht-Master 16622",
    "Rolex Datejust Turn-O-Graph 16264",
    "Rolex Explorer II 16570",
    "Rolex Air-King 114200"
]

box_7500_watches_sequence = [
    "Rolex Day-Date 18238",
    "Richard Mille RM 005",
    "Audemars Piguet Royal Oak 15300ST",
    "Rolex GMT-Master II 126710BLRO",
    "Richard Mille RM 010"
]

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_clicks[user_id] = {"box_3000": 0, "box_6000": 0, "box_7500": 0}

    keyboard = [
        [InlineKeyboardButton("💵 $3000 Mystery Box", callback_data="box_3000")],
        [InlineKeyboardButton("💰 $6000 Mystery Box", callback_data="box_6000")],
        [InlineKeyboardButton("💎 $7500 Mystery Box", callback_data="box_7500")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_message = (
        "🎉 Congratulations on buying your first mystery box!\n\n"
        "Please only select the box you purchased.\n"
        "You can only open a box *5 times max* — after that, attempts will be marked invalid.\n\n"
        "Happy hunting and DM once you're done! 📩"
    )
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

# Handle box selection
async def handle_box_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    box_type = query.data

    if user_id not in user_clicks:
        user_clicks[user_id] = {"box_3000": 0, "box_6000": 0, "box_7500": 0}

    if user_clicks[user_id][box_type] >= 5:
        await query.message.reply_text("⚠️ You've reached your 5 box limit.")
        return

    user_clicks[user_id][box_type] += 1

    # Choose watch based on box
    if box_type == "box_3000":
        selected_watch = random.choice(box_3000_watches)
    elif box_type == "box_6000":
        selected_watch = random.choice(box_6000_watches)
    elif box_type == "box_7500":
        click_count = user_clicks[user_id][box_type]
        index = (click_count - 1) % 5
        selected_watch = box_7500_watches_sequence[index]
    else:
        await query.message.reply_text("❌ Invalid box selection.")
        return

    # Build button to open another
    button = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"🎁 Open another {box_type.replace('_', ' $').upper()} box", callback_data=box_type)]
    ])
    
    await query.message.reply_text(f"🎁 You got: *{selected_watch}*", parse_mode='Markdown', reply_markup=button)

# Main bot runner
def main():
    import os
    TOKEN = "7561016807:AAGjG4IwayZLMMYSQmTs6zeLBDCgIWVemcI"
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_box_selection))

    app.run_polling()

if __name__ == "__main__":
    main()
