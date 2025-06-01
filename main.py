from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import random

# Watches for each box
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
    "Rolex Datejust 16014", "Omega Seamaster Aqua Terra", "Tudor Black Bay 36",
    "Breitling Superocean Heritage", "Cartier Tank Française"
]

box_7500_regular_watches = [
    "Omega Speedmaster Moonwatch", "Rolex Oyster Royal",
    "Omega Moonwatch Chronograph", "Rolex Date 1500"
]
special_7500_watch = "Omega MoonSwatch 'Mission to the Moon'"
box_7500_clicks = 0

WELCOME_MSG = (
    "🎉 Congratulations on buying your first mystery box!\n\n"
    "Please only select the box you purchased.\n"
    "You can only open a box **10 times max** — after that, attempts will be marked invalid.\n\n"
    "Happy hunting and DM once you're done! 📩"
)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💵 $3000 Mystery Box", callback_data="box_3000")],
        [InlineKeyboardButton("💰 $6000 Mystery Box", callback_data="box_6000")],
        [InlineKeyboardButton("💎 $7500 Mystery Box", callback_data="box_7500")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(WELCOME_MSG, reply_markup=reply_markup)

# Button click handler
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global box_7500_clicks
    query = update.callback_query
    await query.answer()
    box = query.data

    if box == "box_3000":
        selected_watch = random.choice(box_3000_watches)
        keyboard = [[InlineKeyboardButton("🔁 Open Another $3000 Box", callback_data="box_3000")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            f"🎁 Box Opened:\n{selected_watch}\n\nDM for more info!", reply_markup=reply_markup
        )

    elif box == "box_6000":
        selected_watch = random.choice(box_6000_watches)
        keyboard = [[InlineKeyboardButton("🔁 Open Another $6000 Box", callback_data="box_6000")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            f"🎁 Box Opened:\n{selected_watch}\n\nDM for more info!", reply_markup=reply_markup
        )

    elif box == "box_7500":
        box_7500_clicks += 1
        if box_7500_clicks % 5 == 0:
            selected_watch = special_7500_watch
        else:
            selected_watch = random.choice(box_7500_regular_watches)
        keyboard = [[InlineKeyboardButton("🔁 Open Another $7500 Box", callback_data="box_7500")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            f"🎁 Box Opened:\n{selected_watch}\n\nDM for more info!", reply_markup=reply_markup
        )

    else:
        await query.edit_message_text("⚠️ Invalid box selection.")

# Main app
def main():
    TOKEN = "7561016807:AAGjG4IwayZLMMYSQmTs6zeLBDCgIWVemcI"
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler_)
