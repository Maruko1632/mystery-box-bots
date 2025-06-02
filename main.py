from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import random

# Per-user click tracking
user_clicks = {}

# Personalized watches for @StephenMaruko
stephen_watches = [
    "ROLEX OYSTERDATE PRECISION",
    "Omega Speedmaster Co-Axial",
    "Rolex Oyster Perpetual 6284",
    "Audemars Piguet Royal Oak Lady",
    "TUDOR Black Bay Gmt 41 mm"
]

# Generic box_7500 watches (non-Stephen)
box_7500_watches = [
    "Rolex Submariner Date",
    "Richard Mille RM 010",
    "Audemars Piguet Royal Oak Black Dial",
    "Rolex Sky-Dweller Steel",
    "Omega Mission to the Moon"
]

# box_3000 watches
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

# box_6000 watches
box_6000_watches = [
    "Tudor Black Bay",
    "Omega Seamaster Aqua Terra",
    "Tag Heuer Carrera",
    "Longines HydroConquest",
    "Breitling Superocean",
    "Rado Captain Cook",
    "Oris Aquis",
    "Tissot Gentleman",
    "Raymond Weil Freelancer",
    "Baume & Mercier Clifton"
]

# Get brand quality icon
def get_brand_quality(watch_name):
    high_end = ["Rolex", "Richard Mille", "Audemars Piguet"]
    if any(brand in watch_name for brand in high_end):
        return "🟩"
    else:
        return "🟥"

# /start handler
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
        "You can only open a box **5 times max** — after that, attempts will be marked invalid.\n\n"
        "Happy hunting and DM once you're done! 📩"
    )

    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

# Box click handler
async def handle_box_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    username = query.from_user.username
    box = query.data

    if box not in ["box_3000", "box_6000", "box_7500"]:
        await query.edit_message_text("Invalid box selected.")
        return

    if user_id not in user_clicks:
        user_clicks[user_id] = {"box_3000": 0, "box_6000": 0, "box_7500": 0}

    if user_clicks[user_id][box] >= 5:
        await context.bot.send_message(chat_id=query.message.chat_id, text="⚠️ You've reached your 5 box limit.")
        return

    user_clicks[user_id][box] += 1
    click_count = user_clicks[user_id][box]

    if box == "box_3000":
        watch = random.choice(box_3000_watches)
    elif box == "box_6000":
        watch = random.choice(box_6000_watches)
    elif box == "box_7500":
        if username == "StephenMaruko":
            watch = stephen_watches[(click_count - 1) % len(stephen_watches)]
        else:
            if click_count % 5 == 0:
                watch = "Omega Mission to the Moon"
            else:
                watch = random.choice(box_7500_watches[:-1])  # exclude the 5th watch

    quality = get_brand_quality(watch)
    caption = f"🎁 You got: {watch}\nBrand Quality: {quality}"

    next_button = InlineKeyboardMarkup([[InlineKeyboardButton(f"Open another ${box[-4:]} box", callback_data=box)]])
    await context.bot.send_message(chat_id=query.message.chat_id, text=caption, reply_markup=next_button)

# Main runner
def main():
    TOKEN = "7561016807:AAGjG4IwayZLMMYSQmTs6zeLBDCgIWVemcI"  # Replace with your actual bot token
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_box_click))
    app.run_polling()

if __name__ == "__main__":
    main()
