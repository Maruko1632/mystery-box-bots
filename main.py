# telegram_mystery_box_bot.py

import logging
import random
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder, ContextTypes,
    CommandHandler, CallbackQueryHandler
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Session storage
user_sessions = {}

# Watch data
watch_data = {
    "box_3000": [
        {"name": "Rolex Oyster Precision 6426", "brand": "Rolex"},
        {"name": "Rolex Oysterdate Precision 6694", "brand": "Rolex"},
        {"name": "Rolex Air-King 5500", "brand": "Rolex"},
        {"name": "Omega Seamaster 300M", "brand": "Omega"},
        {"name": "Tudor Prince Date", "brand": "Tudor"},
        {"name": "Tag Heuer Formula 1", "brand": "Tag"},
    ],
    "box_6000": [
        {"name": "Rolex Datejust 16220", "brand": "Rolex"},
        {"name": "Omega Aqua Terra", "brand": "Omega"},
        {"name": "Tudor Pelagos", "brand": "Tudor"},
        {"name": "Tag Heuer Carrera", "brand": "Tag"},
        {"name": "Rolex Explorer", "brand": "Rolex"},
    ],
    "box_7500": [
        {"name": "Rolex Day-Date 18038", "brand": "Rolex"},
        {"name": "Richard Mille RM 011", "brand": "Richard Mille"},
        {"name": "Audemars Piguet Royal Oak", "brand": "Audemars"},
        {"name": "Rolex Yacht-Master II", "brand": "Rolex"},
        {"name": "Richard Mille RM 030", "brand": "Richard Mille"},
    ]
}

brand_quality = {
    "Rolex": "🟩",
    "Audemars": "🟩",
    "Richard Mille": "💎",
    "Patek": "🟩",
    "Omega": "🟥",
    "Tudor": "🟥",
    "Tag": "🟥",
    "Seiko": "🟥",
}

def get_box_flavor():
    return random.choice([
        "📦 Opening your box…",
        "🛠 Inspecting contents…",
        "🧊 Sealed tight… let’s see what’s inside!"
    ])

def get_session_summary(watches, selected_watch):
    summary = "\n".join([f"{i+1}. {w}" for i, w in enumerate(watches)])
    return (
        f"🧾 Summary of your pulls today:\n\n"
        f"{summary}\n\n"
        f"Selected: ✅ {selected_watch}\n\n"
        f"🎲 Hope to see you next month!"
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_sessions[user_id] = {
        "opened": 0,
        "history": [],
        "final": None
    }

    keyboard = [
        [InlineKeyboardButton("💵 $3000 Mystery Box", callback_data="box_3000")],
        [InlineKeyboardButton("💰 $6000 Mystery Box", callback_data="box_6000")],
        [InlineKeyboardButton("💎 $7500 Mystery Box", callback_data="box_7500")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🎉 Congratulations on buying your first mystery box!\n\n"
        "Please only select the box you purchased.\n"
        "You can only open a box 5 times max — after that, attempts will be marked invalid.\n\n"
        "Happy hunting and DM once you're done! 📩",
        reply_markup=reply_markup
    )

async def handle_box_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    box = query.data

    session = user_sessions.get(user_id)
    if not session:
        await query.edit_message_text("Session expired. Please /start again.")
        return

    if session["opened"] >= 5:
        await query.edit_message_text("⚠️ You've reached your 5 box limit.\n\n🎲 Hope to see you next month!")
        return

    session["opened"] += 1
    progress = f"📦 Box {session['opened']} of 5"

    if box not in watch_data:
        await query.edit_message_text("Invalid box selected.")
        return

    available = [w for w in watch_data[box] if w["name"] not in session["history"]]
    if not available:
        await query.edit_message_text("No new watches available.")
        return

    selected = random.choice(available)
    session["history"].append(selected["name"])

    brand = selected["brand"]
    quality = brand_quality.get(brand, "🟥")

    flavor = get_box_flavor()

    message = (
        f"{flavor}\n"
        f"{progress}\n\n"
        f"🎁 You got: {selected['name']}\n"
        f"Brand Quality: {quality}"
    )

    if session["opened"] == 5:
        session["final"] = selected["name"]
        message += (
            f"\n\n🎉 Congratulations! You've selected your final watch:\n"
            f"{selected['name']}\n"
            f"Brand Quality: {quality}\n\n"
            f"Please contact us to plan pickup or shipping.\n\n"
            f"⚠️ You've reached your 5 box limit."
        )
        message += "\n\n" + get_session_summary(session["history"], session["final"])
        await context.bot.send_message(chat_id=query.message.chat_id, text=message)
    else:
        keyboard = [
            [InlineKeyboardButton(f"🔁 Open another {box.replace('_', ' ').title()} Box", callback_data=box)],
            [InlineKeyboardButton("🎯 Select this watch", callback_data=f"select_{session['opened']}")]
        ]
        await context.bot.send_message(chat_id=query.message.chat_id, text=message, reply_markup=InlineKeyboardMarkup(keyboard))

def main():
    import os
    TOKEN = os.environ.get("7561016807:AAGjG4IwayZLMMYSQmTs6zeLBDCgIWVemcI")
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_box_selection))

    app.run_polling()

if __name__ == "__main__":
    main()
