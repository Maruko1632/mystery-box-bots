from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import random

TOKEN = "7561016807:AAGjG4IwayZLMMYSQmTs6zeLBDCgIWVemcI"

user_clicks = {}

# Watch Lists
box_3000 = [
    "Rolex Oyster Precision 6426",
    "Rolex Oysterdate Precision 6694",
    "Rolex Air-King 5500",
    "Rolex Oyster Perpetual 1002",
    "Rolex Date 1500",
    "Rolex Oyster Perpetual 6564",
    "Rolex Oyster Perpetual 6430",
    "Rolex Oyster Date 6517",
    "Rolex Oyster Perpetual 6284",
    "Rolex Oyster Perpetual 6718 (Ladies)"
]

box_6000 = [
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

box_7500_regular = [
    "Rolex Oyster Perpetual 6564",
    "Rolex Datejust 16233",
    "Richard Mille RM 005",
    "Richard Mille RM 67-01",
    "Audemars Piguet Royal Oak Offshore",
    "Rolex Submariner 16610",
    "Richard Mille RM 030",
    "Patek Philippe Nautilus 5711",
    "Omega Speedmaster Moonwatch",
]

box_7500_special = [
    "ROLEX OYSTERDATE PRECISION",
    "Omega Speedmaster Co-Axial",
    "Rolex Oyster Perpetual 6284",
    "Audemars Piguet Royal Oak Lady",
    "TUDOR Black Bay Gmt 41 mm"
]

def get_brand_quality(watch_name):
    if "Richard Mille" in watch_name:
        return "💎"
    elif any(brand in watch_name for brand in ["Rolex", "Audemars", "Patek"]):
        return "🟩"
    else:
        return "🟥"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_clicks[user_id] = {}
    keyboard = [
        [InlineKeyboardButton("💵 $3000 Mystery Box", callback_data="box_3000")],
        [InlineKeyboardButton("💰 $6000 Mystery Box", callback_data="box_6000")],
        [InlineKeyboardButton("💎 $7500 Mystery Box", callback_data="box_7500")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🎉 Congratulations on buying your first mystery box!\n\n"
        "Please only select the box you purchased.\n"
        "You can only open a box *5 times max* — after that, attempts will be marked invalid.\n\n"
        "Happy hunting and DM once you're done! 📩",
        reply_markup=reply_markup
    )

async def handle_box_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    box_type = query.data
    user_id = query.from_user.id
    username = query.from_user.username or ""

    if user_id not in user_clicks:
        user_clicks[user_id] = {}

    if box_type not in user_clicks[user_id]:
        user_clicks[user_id][box_type] = 0

    clicks = user_clicks[user_id][box_type]

    if clicks >= 5:
        await query.message.reply_text("⚠️ You've reached your 5 box limit.")
        return

    user_clicks[user_id][box_type] += 1
    click_num = user_clicks[user_id][box_type]

    # Box 3000
    if box_type == "box_3000":
        selected = random.choice(box_3000)
    # Box 6000
    elif box_type == "box_6000":
        selected = random.choice(box_6000)
    # Box 7500
    elif box_type == "box_7500":
        if username.lower() == "stephenmaruko":
            selected = box_7500_special[(click_num - 1) % len(box_7500_special)]
        else:
            if click_num == 5:
                selected = "Richard Mille Mission to the Moon"
            else:
                available = [w for w in box_7500_regular if "Mission to the Moon" not in w]
                selected = random.choice(available)
    else:
        await query.message.reply_text("Invalid box selected.")
        return

    emoji = get_brand_quality(selected)

    message = f"🎁 Box Opened: {selected}\nBrand Quality: {emoji}"

    if click_num < 5:
        button = InlineKeyboardButton(f"Open another ${box_type[-4:]} box", callback_data=box_type)
        markup = InlineKeyboardMarkup([[button]])
        await query.message.reply_text(message, reply_markup=markup)
    else:
        await query.message.reply_text(
            f"🎉 Congratulations! You've won:\n\n{selected}\nBrand Quality: {emoji}\n\n"
            "Please contact me to plan shipping or pick up your watch.\n\n"
            "⚠️ You've reached your 5 box limit."
        )

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_box_selection))
    app.run_polling()

if __name__ == "__main__":
    main()
