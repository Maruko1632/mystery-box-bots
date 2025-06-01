from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import random

TOKEN = "7561016807:AAGjG4IwayZLMMYSQmTs6zeLBDCgIWVemcI"  # Replace with your actual token

# Store click counts per user and box
user_clicks = {}
user7500_counter = {}

# Box watch lists
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
    "Rolex Datejust 16014",
    "Rolex Datejust 16030",
    "Rolex Datejust 16234",
    "Rolex Datejust 16013",
    "Rolex Datejust 1601"
]

box_7500_watches = [
    "Omega Speedmaster Moonwatch",
    "Rolex Oyster Royal",
    "Omega Moonwatch Chronograph",
    "Rolex Date 1500",
    "Omega Mission to the Moon"
]

WELCOME_MESSAGE = (
    "🎉 Congratulations on buying your first mystery box!\n\n"
    "Please only select the box you purchased.\n"
    "You can only open a box *5 times max* — after that, attempts will be marked invalid.\n\n"
    "Happy hunting and DM once you're done! 📩"
)

def get_box_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💵 $3000 Mystery Box", callback_data="box_3000")],
        [InlineKeyboardButton("💰 $6000 Mystery Box", callback_data="box_6000")],
        [InlineKeyboardButton("💎 $7500 Mystery Box", callback_data="box_7500")]
    ])

def get_open_another_keyboard(box):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f"🎁 Open another ${box[4:]} box", callback_data=box)]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    # Reset their box click counts
    user_clicks[user_id] = {'box_3000': 0, 'box_6000': 0, 'box_7500': 0}
    user7500_counter[user_id] = 0

    await update.message.reply_text(WELCOME_MESSAGE, reply_markup=get_box_keyboard(), parse_mode="Markdown")

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    box = query.data

    # Init user tracking if not set yet
    if user_id not in user_clicks:
        user_clicks[user_id] = {'box_3000': 0, 'box_6000': 0, 'box_7500': 0}
    if user_id not in user7500_counter:
        user7500_counter[user_id] = 0

    if box not in ['box_3000', 'box_6000', 'box_7500']:
        await query.edit_message_text("Invalid box selected.")
        return

    # Check per-user limit
    if user_clicks[user_id][box] >= 5:
        await query.edit_message_text("❌ You've reached your 5 open limit for this box. Contact us if needed.")
        return

    user_clicks[user_id][box] += 1

    # Box behavior
    if box == 'box_3000':
        result = random.choice(box_3000_watches)
    elif box == 'box_6000':
        result = random.choice(box_6000_watches)
    elif box == 'box_7500':
        user7500_counter[user_id] += 1
        if user7500_counter[user_id] % 5 == 0:
            result = "Omega Mission to the Moon"
        else:
            result = random.choice(box_7500_watches)

    message = f"🎁 You got: *{result}*"
    await query.message.reply_text(message, reply_markup=get_open_another_keyboard(box), parse_mode="Markdown")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_button))
    app.run_polling()
