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

box_6000_watches = random.sample(box_3000_watches, len(box_3000_watches))  # reuse randomized

box_7500_watches = [
    # Richard Mille watches
    "Richard Mille RM 035 Rafael Nadal",
    "Richard Mille RM 11-03 McLaren",
    "Richard Mille RM 72-01 Flyback Chronograph",
    "Richard Mille RM 67-02 Extra Flat",
    "Richard Mille RM 88 Tourbillon Smiley",
    "Richard Mille RM 16-02 Automatic Extraflat",
    "Richard Mille RM 27-04 Tourbillon Rafael Nadal",
    "Richard Mille RM 65-01 Split-Seconds Chronograph",
    "Richard Mille RM 29 Le Mans",
    "Richard Mille RM 030 Automatic Winding",
    # Rolex watches
    "Rolex Daytona 116503 Black Mother Of Pearl Diamond Dial",
    "Rolex GMT-Master II 'Pepsi' 126719 BLRO White Gold Blue Dial",
    "Rolex Submariner Date 116619LB Blue Dial",
    "Rolex Sky-Dweller 326138 Champagne Dial",
    "Rolex Yacht-Master II 116689 White Gold",
    "Rolex Day-Date 128238 Fluted Bezel Champagne Dial",
    "Rolex Submariner Date 126618LB Blue Dial",
    "Rolex Sky-Dweller 326238 Black Dial",
    "Rolex Oyster Perpetual 124300 'Tiffany' Blue Dial"
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
            result = "Richard Mille RM 035 Rafael Nadal"
        else:
            result = random.choice([w for w in box_7500_watches if w != "Richard Mille RM 035 Rafael Nadal"])
    else:
        result = "❌ Invalid box."

    open_again_button = [[InlineKeyboardButton(f"🔁 Open another ${box[4:]} box", callback_data=box)]]
    await query.message.reply_text(f"🎉 You got: {result}", reply_markup=InlineKeyboardMarkup(open_again_button))

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_button))
    app.run_polling()

if __name__ == "__main__":
    main()
