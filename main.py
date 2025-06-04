from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import random

TOKEN = "7561016807:AAGjG4IwayZLMMYSQmTs6zeLBDCgIWVemcI"

# Watch pools
box_3000 = [
    "Rolex Oyster Precision 6426", "Rolex Oysterdate Precision 6694", "Rolex Air-King 5500",
    "Rolex Oyster Perpetual 1002", "Rolex Date 1500", "Omega Seamaster", "Omega De Ville",
    "Tudor Black Bay 36", "Swiss Military Hanowa", "Tissot PRX", "Omega Genève", "Tudor Royal",
    "Rolex Cellini", "Omega Seamaster Cosmic", "Tudor Pelagos 39"
]

box_6000 = [
    "Rolex Datejust 16233", "Rolex Explorer II 16570", "Omega Speedmaster Co-Axial",
    "Richard Mille RM 005", "Audemars Piguet Royal Oak Lady", "Tudor Black Bay GMT",
    "Omega Constellation", "Swiss Chronograph Heritage", "Rolex Submariner 14060",
    "Tudor Heritage Advisor", "Omega Aqua Terra", "Rolex Yacht-Master 16622",
    "Tissot Seastar 1000", "Rolex Milgauss 116400", "Tudor Black Bay Fifty-Eight"
]

box_7500 = [
    "Rolex Sky-Dweller", "Richard Mille RM 11-03", "Audemars Piguet Royal Oak",
    "Rolex Day-Date 40", "Richard Mille RM 055", "Rolex GMT-Master II Root Beer",
    "Audemars Piguet Royal Oak Offshore", "Rolex Submariner Date 41mm",
    "Audemars Piguet Royal Oak Chronograph", "Rolex Yacht-Master II",
    "Rolex Sea-Dweller Deepsea", "Audemars Piguet Royal Oak Concept",
    "Patek Philippe Aquanaut", "Patek Philippe Nautilus", "Rolex Sky-Dweller Blue"
]

user_clicks = {}
user_history = {}
final_selection = {}

def get_brand_stars(watch_name: str) -> str:
    name = watch_name.lower()
    if any(b in name for b in ["richard mille", "rolex", "audemars", "patek"]):
        return "⭐️⭐️⭐️⭐️⭐️"
    elif "omega" in name or "swiss" in name:
        return "⭐️⭐️"
    elif "tudor" in name:
        return "⭐️⭐️"
    else:
        return "⭐️"

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
        "You can open a box **5 times max** — after that, attempts will be locked.\n\n"
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

    pool = {"box_3000": box_3000, "box_6000": box_6000, "box_7500": box_7500}[box]
    used = user_history[user]
    options = [w for w in pool if w not in used]

    if not options:
        await query.message.reply_text("⚠️ No more unique watches left to pull in this box.")
        return

    selected = random.choice(options)
    stars = get_brand_stars(selected)

    user_clicks[user] += 1
    user_history[user].append(selected)

    text = f"🎁 You opened:\n\nWatch: {selected}\nBrand Quality: {stars}"

    buttons = []
    if user_clicks[user] < 5:
        buttons.append([
            InlineKeyboardButton(f"🔁 Open another {box.replace('box_', '$')} box", callback_data=box),
            InlineKeyboardButton("✅ Select Watch", callback_data="select")
        ])
    else:
        final_text = (
            f"🎉 Congratulations! You've selected your final watch:\n\n"
            f"Watch: {selected}\n\n"
            "Please contact us to plan pickup or shipping.\n\n"
            "⚠️ You've reached your 5 box limit."
        )
        final_selection[user] = selected
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
    stars = get_brand_stars(selected)
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
