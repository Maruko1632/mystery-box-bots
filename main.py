import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "7561016807:AAGjG4IwayZLMMYSQmTs6zeLBDCgIWVemcI"

# User click history and limits
user_clicks = {}

# Watch pools
box_3000 = [
    {"name": "Tissot Gentleman", "quality": "🟩"},
    {"name": "Longines HydroConquest", "quality": "🟥"},
    {"name": "Hamilton Jazzmaster", "quality": "🟩"},
    {"name": "Seiko Presage", "quality": "🟩"},
    {"name": "Mido Ocean Star", "quality": "🟥"},
]

box_6000 = [
    {"name": "Tudor Black Bay", "quality": "🟥"},
    {"name": "Tag Heuer Carrera", "quality": "🟩"},
    {"name": "Oris Aquis", "quality": "🟩"},
    {"name": "Rado Captain Cook", "quality": "🟥"},
    {"name": "Raymond Weil Freelancer", "quality": "🟩"},
]

box_7500 = [
    {"name": "Omega Seamaster", "quality": "🟥"},
    {"name": "IWC Pilot", "quality": "🟩"},
    {"name": "Cartier Santos", "quality": "🟥"},
    {"name": "Zenith Chronomaster", "quality": "🟩"},
    {"name": "Breitling Navitimer", "quality": "🟩"},
]

special_watch = {"name": "Omega Mission to the Moon", "quality": "💎"}

def get_random_watches(pool):
    selected = []
    reds = [w for w in pool if w["quality"] == "🟥"]
    greens = [w for w in pool if w["quality"] == "🟩"]
    selected.append(random.choice(reds))
    greens_selected = random.sample(greens, 3)
    selected += greens_selected
    reds.remove(selected[0])
    selected.append(random.choice(reds))
    random.shuffle(selected)
    return selected

def get_user_clicks(user_id):
    return user_clicks.setdefault(user_id, {"clicks": 0, "history": []})

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_clicks[user_id] = {"clicks": 0, "history": []}
    buttons = [
        [InlineKeyboardButton("🎁 Open $3,000 Box", callback_data="box_3000")],
        [InlineKeyboardButton("🎁 Open $6,000 Box", callback_data="box_6000")],
        [InlineKeyboardButton("🎁 Open $7,500 Box", callback_data="box_7500")],
    ]
    await update.message.reply_text("Choose a mystery box:", reply_markup=InlineKeyboardMarkup(buttons))

async def open_box(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    clicks = get_user_clicks(user_id)

    if clicks["clicks"] >= 5:
        await query.edit_message_text("⚠️ You've reached your 5 box limit.")
        return

    box_type = query.data
    if box_type == "box_3000":
        pool = box_3000
    elif box_type == "box_6000":
        pool = box_6000
    else:
        if clicks["clicks"] == 4:
            selected_watch = special_watch
        else:
            pool = box_7500
            selected_watch = random.choice(pool)

    if box_type in ["box_3000", "box_6000"]:
        selected_watch = random.choice(pool)

    clicks["clicks"] += 1
    clicks["history"].append(selected_watch)

    response = (
        f"🎉 You pulled: {selected_watch['name']}
"
        f"Brand Quality: {selected_watch['quality']}

"
        f"({clicks['clicks']}/5 openings used)"
    )

    if clicks["clicks"] < 5:
        buttons = [
            [InlineKeyboardButton("🔁 Open Another", callback_data=box_type)],
            [InlineKeyboardButton("✅ Select Watch", callback_data="select_watch")]
        ]
    else:
        buttons = [
            [InlineKeyboardButton("✅ Select Watch", callback_data="select_watch")]
        ]

    await query.edit_message_text(response, reply_markup=InlineKeyboardMarkup(buttons))

async def select_watch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    last_pull = user_clicks.get(user_id, {}).get("history", [])[-1] if user_clicks.get(user_id) else None
    if last_pull:
        msg = f"🎯 You've selected: {last_pull['name']} - Brand Quality: {last_pull['quality']}"
    else:
        msg = "❗ No watch selected yet."
    await query.edit_message_text(msg)

def main():
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(open_box, pattern="^box_"))
    app.add_handler(CallbackQueryHandler(select_watch, pattern="^select_watch$"))
    app.run_polling()

if __name__ == "__main__":
    main()
