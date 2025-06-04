from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import random

TOKEN = "7561016807:AAGjG4IwayZLMMYSQmTs6zeLBDCgIWVemcI"

# Watch pools
box_3000 = [
    "Rolex Oyster Precision 6426", "Rolex Oysterdate Precision 6694", "Rolex Air-King 5500",
    "Rolex Oyster Perpetual 1002", "Rolex Date 1500", "Rolex Oyster Perpetual 6564",
    "Rolex Oyster Perpetual 6430", "Rolex Oyster Date 6517", "Rolex Oyster Perpetual 6284",
    "Rolex Oyster Perpetual 6718 (ladies)", "Rolex Oyster Precision 1210",
    "Rolex Oyster Perpetual Datejust 1601", "Rolex Oyster Royal", "Rolex Precision 9022",
    "Rolex Oyster Perpetual 6618", "Rolex Oyster Perpetual 67193",
    "Rolex Oyster Perpetual 76193 (Ladies)", "Rolex Oysterdate 6694 Linen Dial",
    "Rolex Oyster Perpetual 14233 (Ladies)", "Rolex Bubbleback", "Rolex Zephyr",
    "Rolex Cellini", "Rolex Prince", "Rolex Commando"
]

box_6000 = [
    "Rolex Datejust 16233", "Rolex Explorer II 16570", "Rolex Milgauss 116400",
    "Rolex GMT-Master 16700", "Rolex Sea-Dweller 16600", "Rolex Submariner 14060",
    "Rolex Yacht-Master 16622", "Rolex Air-King 14000M", "Rolex Datejust Turn-O-Graph",
    "Rolex Oysterquartz Datejust", "Rolex Datejust 16014", "Rolex Precision 6426",
    "Rolex Datejust 116200", "Rolex Air-King 114200", "Rolex Datejust 16030",
    "Rolex Explorer 1016", "Rolex Submariner 16610", "Rolex GMT-Master II 16710",
    "Rolex Day-Date 18238", "Rolex Oyster Perpetual 114300", "Rolex Date 15200"
]

box_7500_default = [
    "Rolex Sky-Dweller", "Richard Mille RM 11-03", "Audemars Piguet Royal Oak",
    "Rolex Day-Date 40", "Richard Mille RM 055", "Rolex GMT-Master II Root Beer",
    "Audemars Piguet Royal Oak Offshore", "Rolex Submariner Date 41mm",
    "Audemars Piguet Royal Oak Chronograph", "Rolex Yacht-Master II",
    "Rolex Sea-Dweller Deepsea", "Audemars Piguet Royal Oak Concept",
    "Patek Philippe Aquanaut", "Patek Philippe Nautilus", "Rolex Sky-Dweller Blue"
]

stephen_watches = [
    "ROLEX OYSTERDATE PRECISION", "Omega Speedmaster Co-Axial", "Rolex Oyster Perpetual 6284",
    "Audemars Piguet Royal Oak Lady", "TUDOR Black Bay Gmt 41 mm"
]

user_clicks = {}
user_history = {}
final_selection = {}

def get_watch_list(user):
    return stephen_watches if user == "StephenMaruko" else box_7500_default

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.username or str(update.effective_user.id)
    user_clicks[user] = 0
    user_history[user] = []
    final_selection[user] = None
    keyboard = [
        [InlineKeyboardButton("💵 $3000 Mystery Box", callback_data="box_3000")],
        [InlineKeyboardButton("💰 $6000 Mystery Box", callback_data="box_6000")],
        [InlineKeyboardButton("💎 $7500 Mystery Box", callback_data="box_7500")]
    ]
    welcome = (
        "🎁 Welcome to The Watch King Mystery Box!\n\n"
        "Please only select the box you purchased.\n"
        "You can only open a box 5 times max — after that, attempts will be marked invalid.\n\n"
        "Happy hunting and DM once you're done! 📩"
    )
    await update.message.reply_text(welcome, reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user.username or str(query.from_user.id)
    await query.answer()
    box = query.data

    if box not in ["box_3000", "box_6000", "box_7500"]:
        return

    if user not in user_clicks:
        user_clicks[user] = 0
        user_history[user] = []

    if user_clicks[user] >= 5:
        return

    if box == "box_3000":
        pool = box_3000
    elif box == "box_6000":
        pool = box_6000
    else:
        pool = get_watch_list(user)
        if user == "StephenMaruko" and user_clicks[user] == 4:
            selected = "Omega Speedmaster Co-Axial"
        else:
            options = [w for w in pool if w not in user_history[user]]
            selected = random.choice(options)

    if box != "box_7500":
        options = [w for w in pool if w not in user_history[user]]
        selected = random.choice(options)

    user_clicks[user] += 1
    user_history[user].append(selected)

    if user_clicks[user] >= 5:
        final_selection[user] = selected
        final_text = (
            f"🎉 Congratulations! You've selected your final watch:\n\n"
            f"Watch: {selected}\n\n"
            "Please contact us to plan pickup or shipping.\n\n"
            "⚠️ You've reached your 5 box limit."
        )
        await query.message.reply_text(final_text)
        return

    text = f"🎁 You opened box #{user_clicks[user]}:\n\n{selected}"

    buttons = [
        [InlineKeyboardButton(f"🔁 Open another {box.replace('box_', '$')} box", callback_data=box)],
        [InlineKeyboardButton("✅ Select Watch", callback_data="select")]
    ]

    await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons))

async def handle_select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user.username or str(query.from_user.id)
    await query.answer()

    if not user_history.get(user):
        return

    selected = user_history[user][-1]
    final_selection[user] = selected
    final_msg = (
        f"🎉 Congratulations! You've selected your final watch:\n\n"
        f"Watch: {selected}\n\n"
        "Please contact us to plan pickup or shipping.\n\n"
        "⚠️ You've reached your 5 box limit."
    )
    await query.message.reply_text(final_msg)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_button, pattern="^box_"))
    app.add_handler(CallbackQueryHandler(handle_select, pattern="^select$"))
    app.run_polling()

if __name__ == "__main__":
    main()
