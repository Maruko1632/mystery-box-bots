from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import random

TOKEN = "7561016807:AAGjG4IwayZLMMYSQmTs6zeLBDCgIWVemcI"

# Watch pools
box_3000 = [
    "Rolex Oysterdate Precision 6694", "Omega Seamaster", "Tudor Black Bay", "Rolex Air-King 5500",
    "Omega Speedmaster Date", "Tudor Prince", "Omega Seamaster Aqua Terra", "Tudor Glamour",
    "Rolex Date 1500", "Omega Genève", "Tudor Style", "Rolex Oyster Precision 6426",
    "Omega De Ville", "Tudor Heritage Chrono"
]

box_6000 = [
    "Rolex Explorer II 16570", "Omega Speedmaster Racing", "Tudor Pelagos", "Rolex Submariner 14060",
    "Omega Constellation", "Tudor Grantour", "Rolex GMT-Master 16700", "Tudor North Flag",
    "Omega Planet Ocean", "Tudor Heritage Black Bay", "Rolex Datejust 16014", "Tudor Submariner"
]

box_7500_default = [
    "Rolex Sky-Dweller", "Richard Mille RM 11-03", "Audemars Piguet Royal Oak", "Patek Philippe Aquanaut",
    "Omega Speedmaster Co-Axial", "Tudor Royal", "Omega Dark Side of the Moon", "Tudor Chronograph",
    "Omega Speedmaster '57", "Tudor Pelagos FXD", "Audemars Piguet Royal Oak Chronograph"
]

stephen_watches = [
    "Audemars Piguet Royal Oak",
    "Rolex Datejust 16233",
    "Rolex Submariner 14060",
    "Rolex Oyster Perpetual 1002",
    "Rolex Day-Date 40"
]

crypto_saicho_watches = [
    "Rolex Oyster Precision 6426",
    "Omega Speedster",
    "Tudor Royal",
    "Richard Mille RM010",
    "Rolex Date 1500"
]

user_clicks = {}
user_history = {}
final_selection = {}

def get_brand_stars(watch_name: str):
    name = watch_name.lower()
    if any(b in name for b in ["rolex", "richard mille", "audemars", "patek"]):
        return "⭐️⭐️⭐️⭐️⭐️"
    if any(b in name for b in ["omega", "swiss"]):
        return "⭐️⭐️"
    if "tudor" in name:
        return "⭐️⭐️"
    return ""

def get_watch_list(user):
    if user == "StephenMaruko":
        return stephen_watches
    elif user == "Crypto_Saicho":
        return crypto_saicho_watches
    else:
        return box_7500_default

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
        "🎉 Congratulations on buying your first mystery box!\n\n"
        "Please only select the box you purchased.\n"
        "You can only open a box **5 times max** — after that, attempts will be marked invalid.\n\n"
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
            selected = "Omega Mission to the Moon"
        else:
            used = user_history[user]
            options = [w for w in pool if w not in used]
            selected = random.choice(options)

    if box != "box_7500":
        used = user_history[user]
        options = [w for w in pool if w not in used]
        selected = random.choice(options)

    user_clicks[user] += 1
    user_history[user].append(selected)
    stars = get_brand_stars(selected)

    text = f"🎁 You opened:\n\n{selected}\nBrand Quality: {stars}"

    buttons = []
    if user_clicks[user] < 5:
        buttons.append([
            InlineKeyboardButton(f"🔁 Open another {box.replace('box_', '$')} box", callback_data=box),
            InlineKeyboardButton("✅ Select Watch", callback_data="select")
        ])
    else:
        final_selection[user] = selected
        final_text = (
            f"🎉 Congratulations! You've selected your final watch:\n\n"
            f"Watch: {selected}\n\n"
            "Please contact us to plan pickup or shipping.\n\n"
            "⚠️ You've reached your 5 box limit."
        )
        await query.message.reply_text(final_text)
        return

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
