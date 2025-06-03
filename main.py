import asyncio
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)
import random

TOKEN = "7561016807:AAGjG4IwayZLMMYSQmTs6zeLBDCgIWVemcI"

# ============================
# Watch Pools Configuration
# ============================

box_3000_watches = [
    "Rolex Oyster Precision 6426 🟩", "Rolex Oysterdate Precision 6694 🟩",
    "Rolex Air-King 5500 🟩", "Rolex Oyster Perpetual 1002 🟩",
    "Rolex Date 1500 🟩", "Omega Seamaster 🟥", "Tissot Chrono XL 🟥",
    "Hamilton Jazzmaster 🟥", "Seiko Presage 🟥", "Tag Heuer Formula 1 🟥"
]

box_6000_watches = [
    "Rolex Oyster Perpetual Datejust 1601 🟩", "Omega Seamaster Aqua Terra 🟥",
    "Tudor Black Bay Fifty-Eight 🟥", "Cartier Santos 🟥", "Longines Spirit 🟥",
    "Rolex Oyster Perpetual 6618 🟩", "Rolex Oysterdate 6694 Linen Dial 🟩",
    "Rolex Oyster Perpetual 67193 🟩", "TAG Heuer Aquaracer 🟥", "Breitling Colt 🟥"
]

box_7500_pool_general = [
    "Rolex Submariner Date 🟩", "Richard Mille RM 010 💎",
    "Audemars Piguet Royal Oak 15450ST 🟩", "Rolex GMT-Master II 🟩",
    "Richard Mille RM 005 💎", "Omega Planet Ocean 🟥", "Tudor Pelagos 🟥",
    "IWC Pilot’s Watch 🟥", "Breitling Navitimer 🟥"
]

box_7500_stephen = [
    "ROLEX OYSTERDATE PRECISION 🟩",
    "Omega Speedmaster Co-Axial 🟥",
    "Rolex Oyster Perpetual 6284 🟩",
    "Audemars Piguet Royal Oak Lady 🟩",
    "TUDOR Black Bay GMT 41mm 🟥"
]

box_7500_fifth_watch = "Omega Mission to the Moon 🟥"

# ============================
# User Session Tracking
# ============================

user_sessions = {}

# ============================
# Message Generators
# ============================

def get_random_pack(watch_pool):
    red_watches = [w for w in watch_pool if "🟥" in w]
    green_watches = [w for w in watch_pool if "🟩" in w or "💎" in w]
    pack = []

    while True:
        red_choices = random.sample(red_watches, 2)
        green_choices = random.sample(green_watches, 3)
        temp_pack = [red_choices[0], green_choices[0], red_choices[1], green_choices[1], green_choices[2]]
        if "🟥" not in [temp_pack[1], temp_pack[2]]:  # no back-to-back reds
            return temp_pack

def get_box_flavor():
    return random.choice([
        "📦 Opening your box...",
        "🛠 Inspecting contents...",
        "🧊 Sealed tight… let’s see what’s inside!"
    ])

def get_box_caption(watch, box_num, count):
    return f"{get_box_flavor()}

📦 Box {count} of 5

🎁 {watch}"

def get_end_summary(pulls, selected):
    summary = "🧾 Summary of your pulls today:

"
    for i, w in enumerate(pulls, 1):
        summary += f"{i}. {w}
"
    summary += f"
Selected: ✅ {selected}

🎲 Hope to see you next month!"
    return summary

# ============================
# Handlers
# ============================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_sessions[user_id] = {"box": None, "count": 0, "history": []}
    keyboard = [
        [InlineKeyboardButton("💵 $3000 Mystery Box", callback_data="box_3000")],
        [InlineKeyboardButton("💰 $6000 Mystery Box", callback_data="box_6000")],
        [InlineKeyboardButton("💎 $7500 Mystery Box", callback_data="box_7500")]
    ]
    await update.message.reply_text(
        "🎉 Congratulations on buying your first mystery box!

"
        "Please only select the box you purchased.
"
        "You can only open a box *5 times max* — after that, attempts will be marked invalid.

"
        "Happy hunting and DM once you're done! 📩",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    username = query.from_user.username
    data = query.data
    session = user_sessions.setdefault(user_id, {"box": None, "count": 0, "history": []})

    if data.startswith("box_"):
        session["box"] = data
        session["count"] = 0
        session["history"] = []

    if session["count"] >= 5:
        await query.answer()
        await query.message.reply_text("⚠️ You've reached your 5 box limit.

Please use /start to reset.")
        return

    if session["box"] == "box_3000":
        pool = get_random_pack(box_3000_watches)
    elif session["box"] == "box_6000":
        pool = get_random_pack(box_6000_watches)
    elif session["box"] == "box_7500":
        if username == "StephenMaruko":
            pool = box_7500_stephen
        else:
            pool = get_random_pack(box_7500_pool_general)
    else:
        await query.answer("Invalid selection.")
        return

    index = session["count"]
    if session["box"] == "box_7500" and index == 4:
        watch = box_7500_fifth_watch
    else:
        watch = pool[index % len(pool)]

    session["history"].append(watch)
    session["count"] += 1

    caption = get_box_caption(watch, session['box'], session['count'])

    keyboard = []
    if session["count"] < 5:
        keyboard = [[
            InlineKeyboardButton(f"🎁 Open another {session['box'].split('_')[1]} box", callback_data=session["box"]),
            InlineKeyboardButton("✅ Select this watch", callback_data="select")
        ]]
    elif session["count"] == 5:
        caption = (
            f"🎉 Congratulations! You've selected your final watch:

"
            f"{watch}

Please contact us to plan pickup or shipping.

⚠️ You've reached your 5 box limit."
        )
        summary = get_end_summary(session["history"], watch)
        await query.message.reply_text(summary)

    await query.answer()
    await query.message.reply_text(caption, reply_markup=InlineKeyboardMarkup(keyboard) if keyboard else None)

async def select_watch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    session = user_sessions.get(user_id)
    if not session or not session["history"]:
        await update.callback_query.answer("No watch selected yet.")
        return
    final_watch = session["history"][-1]
    summary = (
        f"🎉 Congratulations! You've selected your final watch:

"
        f"{final_watch}

Please contact us to plan pickup or shipping.

"
        "⚠️ You've reached your 5 box limit."
    )
    await update.callback_query.message.reply_text(summary)

# ============================
# Main
# ============================

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_button, pattern="^box_"))
    app.add_handler(CallbackQueryHandler(select_watch, pattern="^select$"))
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
