from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import random

TOKEN = "7561016807:AAGjG4IwayZLMMYSQmTs6zeLBDCgIWVemcI"

# Watch pools
box_3000 = [
    "Rolex Oyster Precision 6426", "Rolex Oysterdate Precision 6694", "Rolex Air-King 5500",
    "Rolex Oyster Perpetual 1002", "Rolex Date 1500", "Rolex Oyster Perpetual 6564",
    "Rolex Oyster Perpetual 6430", "Rolex Oyster Date 6517", "Rolex Oyster Perpetual 6284",
    "Rolex Oyster Perpetual 6718 (ladies)", "Rolex Oyster Precision 1210", "Rolex Oyster Perpetual Datejust 1601",
    "Rolex Oyster Royal", "Rolex Precision 9022", "Rolex Oyster Perpetual 6618"
]

box_6000 = [
    "Rolex Datejust 16233", "Rolex Explorer II 16570", "Rolex Milgauss 116400", "Rolex GMT-Master 16700",
    "Rolex Sea-Dweller 16600", "Rolex Submariner 14060", "Rolex Yacht-Master 16622", "Rolex Air-King 14000M",
    "Rolex Datejust Turn-O-Graph", "Rolex Oysterquartz Datejust", "Rolex Datejust 16014", "Rolex Precision 6426",
    "Rolex Datejust 116200", "Rolex Air-King 114200", "Rolex Datejust 16030"
]

box_7500_default = [
    "Rolex Sky-Dweller", "Richard Mille RM 11-03", "Audemars Piguet Royal Oak", "Rolex Day-Date 40",
    "Richard Mille RM 055", "Rolex GMT-Master II Root Beer", "Audemars Piguet Royal Oak Offshore",
    "Rolex Submariner Date 41mm", "Audemars Piguet Royal Oak Chronograph", "Rolex Yacht-Master II",
    "Rolex Sea-Dweller Deepsea", "Audemars Piguet Royal Oak Concept", "Patek Philippe Aquanaut",
    "Patek Philippe Nautilus", "Rolex Sky-Dweller Blue"
]

crypto_saicho_watches = [
    "Omega Speedmaster Moonwatch",
    "ROLEX OYSTER ROYAL PRECISION 1965",
    "Rolex Oyster Perpetual Lady",
    "Rolex Cellini 4109",
    "TUDOR 1926 41 mm Steel Case"
]

stephen_maruko_watches = [
    "ROLEX DATEJUST OYSTERQUARTZ",
    "Rolex Oyster 2014",
    "TUDOR Black Bay Gmt",
    "ROLEX STAINLESS STEEL OYSTER",
    "Rolex Oyster Perpetual Date"
]

user_clicks = {}
user_history = {}
final_selection = {}

def get_brand_stars(watch_name: str):
    name = watch_name.lower()
    if any(b in name for b in ["rolex", "patek", "audemars", "richard mille"]):
        return "⭐️⭐️⭐️⭐️⭐️"
    if any(b in name for b in ["omega", "swiss", "tudor"]):
        return "⭐️⭐️"
    return ""

def get_watch_list(user):
    if user == "Crypto_Saicho":
        return crypto_saicho_watches
    if user == "StephenMaruko":
        return stephen_maruko_watches
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

    used = user_history[user]
    options = [w for w in pool if w not in used]
    if not options:
        return
    selected = random.choice(options)

    stars = get_brand_stars(selected)
    user_clicks[user] += 1
    user_history[user].append(selected)

    text = f"🎁 You opened:\n\n{selected}\nBrand Quality: {stars}"

    buttons = []
    if user_clicks[user] < 5:
        buttons.append([
            InlineKeyboardButton(f"🔁 Open another {box.replace('box_', '$')} box", callback_data=box),
            InlineKeyboardButton("✅ Select Watch", callback_data="select")
        ])
    else:
        final_selection[user] = selected

        if user == "Crypto_Saicho":
            summary = [
                "Omega Speedmaster Moonwatch - 42 mm, Moonshine™ gold\nPrice: 43,000$",
                "ROLEX OYSTER ROYAL PRECISION 6427 - YEAR 1965 CASE 34 MM\nPrice: 2500$",
                "Rolex Oyster Perpetual Lady - Year: 1963\nPrice: 2490$",
                "Rolex Cellini 4109 - Year: 1988\nPrice: 3780$",
                "TUDOR 1926 41 mm Steel Case - Year: 2020\nPrice: 2090$"
            ]
        elif user == "StephenMaruko":
            summary = [
                "ROLEX DATEJUST OYSTERQUARTZ\nYear: 1989\nPrice: 8700$",
                "Rolex Oyster 2014\nYEAR 2014 CASE 34 MM\nPrice: 4780$",
                "TUDOR Black Bay Gmt\nYear: 2020\nPrice: 6500$",
                "ROLEX STAINLESS STEEL OYSTER\nYear: 1988\nPrice: 5960$",
                "Rolex Oyster Perpetual Date\nYear: 1993\nPrice: 9500$"
            ]
        else:
            summary = []

        pulled_summary = "\n\n".join(summary)
        final_text = (
            f"🎉 Congratulations! You've selected your final watch:\n\n"
            f"Watch: {selected}\n\n"
            f"{'Here is a summary of what else you pulled today 👇\n\n' + pulled_summary + '\n\n' if summary else ''}"
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

    if user == "Crypto_Saicho":
        summary = [
            "Omega Speedmaster Moonwatch - 42 mm, Moonshine™ gold\nPrice: 43,000$",
            "ROLEX OYSTER ROYAL PRECISION 6427 - YEAR 1965 CASE 34 MM\nPrice: 2500$",
            "Rolex Oyster Perpetual Lady - Year: 1963\nPrice: 2490$",
            "Rolex Cellini 4109 - Year: 1988\nPrice: 3780$",
            "TUDOR 1926 41 mm Steel Case - Year: 2020\nPrice: 2090$"
        ]
    elif user == "StephenMaruko":
        summary = [
            "ROLEX DATEJUST OYSTERQUARTZ\nYear: 1989\nPrice: 8700$",
            "Rolex Oyster 2014\nYEAR 2014 CASE 34 MM\nPrice: 4780$",
            "TUDOR Black Bay Gmt\nYear: 2020\nPrice: 6500$",
            "ROLEX STAINLESS STEEL OYSTER\nYear: 1988\nPrice: 5960$",
            "Rolex Oyster Perpetual Date\nYear: 1993\nPrice: 9500$"
        ]
    else:
        summary = []

    pulled_summary = "\n\n".join(summary)
    final_msg = (
        f"🎉 Congratulations! You've selected your final watch:\n\n"
        f"Watch: {selected}\n\n"
        f"{'Here is a summary of what else you pulled today 👇\n\n' + pulled_summary + '\n\n' if summary else ''}"
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
