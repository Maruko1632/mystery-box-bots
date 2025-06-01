from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import random

# Watch lists
box_3000_watches = [
    "Rolex Oyster Precision 6426", "Rolex Oysterdate Precision 6694", "Rolex Air-King 5500",
    "Rolex Oyster Perpetual 1002", "Rolex Date 1500", "Rolex Oyster Perpetual 6564",
    "Rolex Oyster Perpetual 6430", "Rolex Oyster Date 6517", "Rolex Oyster Perpetual 6284",
    "Rolex Oyster Perpetual 6718 (ladies)", "Rolex Oyster Precision 1210",
    "Rolex Oyster Perpetual Datejust 1601", "Rolex Oyster Royal", "Rolex Precision 9022",
    "Rolex Oyster Perpetual 6618", "Rolex Oyster Perpetual 67193",
    "Rolex Oyster Perpetual 76193 (Ladies)", "Rolex Oysterdate 6694 Linen Dial",
    "Rolex Oyster Perpetual 14233 (Ladies)"
]

box_6000_watches = [
    "Rolex Submariner 16610", "Omega Seamaster 300M", "Rolex GMT-Master 1675",
    "Omega Constellation Pie Pan", "Rolex Explorer 14270", "Omega Speedmaster Reduced",
    "Rolex Air-King 14000", "Omega Railmaster", "Rolex Milgauss 116400",
    "Omega Seamaster Planet Ocean"
]

box_7500_watches = [
    "Omega Speedmaster Moonwatch", "Rolex Oyster Royal", "Omega Moonwatch Chronograph",
    "Rolex Date 1500", "Omega Mission to the Moon"  # Every 5th click should return this
]

# Track clicks
click_counter = {
    "box_3000": 0,
    "box_6000": 0,
    "box_7500": 0
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💵 $3000 Mystery Box", callback_data="box_3000")],
        [InlineKeyboardButton("💰 $6000 Mystery Box", callback_data="box_6000")],
        [InlineKeyboardButton("💎 $7500 Mystery Box", callback_data="box_7500")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🎉 *Congratulations on buying your first mystery box!*\n\n"
        "Please only select the box you purchased.\n"
        "You can only open a box *5 times max* — after that, attempts will be marked invalid.\n\n"
        "Happy hunting and DM once you're done! 📩",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    box = query.data

    if box not in click_counter:
        await query.edit_message_text("Invalid box selected.")
        return

    click_counter[box] += 1
    count = click_counter[box]

    if count > 5:
        await query.edit_message_text("❌ You've exceeded the maximum number of opens for this box.")
        return

    if box == "box_3000":
        selected = random.choice(box_3000_watches)
        price = "$3000"
    elif box == "box_6000":
        selected = random.choice(box_6000_watches)
        price = "$6000"
    elif box == "box_7500":
        if count % 5 == 0:
            selected = "Omega Mission to the Moon"
        else:
            selected = random.choice(box_7500_watches)
        price = "$7500"
    else:
        selected = "Unknown Watch"
        price = "N/A"

    # Show watch result and button to open again
    keyboard = [
        [InlineKeyboardButton(f"🎁 Open Another {price} Box", callback_data=box)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        f"🎉 You got: *{selected}*\n\nDM @YourUsername to claim your watch!",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

def main():
    TOKEN = "7561016807:AAGjG4IwayZLMMYSQmTs6zeLBDCgIWVemcI"
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_button))

    app.run_polling()

if __name__ == "__main__":
    main()
