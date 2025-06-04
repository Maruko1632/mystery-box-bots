import logging
import random
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Replace this with your actual bot token
TOKEN = "7561016807:AAGjG4IwayZLMMYSQmTs6zeLBDCgIWVemcI"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Watch pools
watch_pool_3000 = [
    {"name": "Tudor Black Bay 58", "brand": "Tudor"},
    {"name": "Tag Heuer Carrera", "brand": "Tag Heuer"},
    {"name": "Omega Seamaster", "brand": "Omega"},
    {"name": "Oris Aquis", "brand": "Oris"},
    {"name": "Longines HydroConquest", "brand": "Longines"},
]

watch_pool_6000 = [
    {"name": "Rolex Datejust", "brand": "Rolex"},
    {"name": "Omega Speedmaster", "brand": "Omega"},
    {"name": "Grand Seiko SBGA211", "brand": "Grand Seiko"},
    {"name": "Panerai Luminor", "brand": "Panerai"},
    {"name": "IWC Pilot Chronograph", "brand": "IWC"},
]

default_watch_pool_7500 = [
    {"name": "Audemars Piguet Royal Oak", "brand": "AP"},
    {"name": "Rolex Submariner", "brand": "Rolex"},
    {"name": "Omega Speedmaster Snoopy", "brand": "Omega"},
    {"name": "Hublot Big Bang", "brand": "Hublot"},
    {"name": "Zenith Defy", "brand": "Zenith"},
]

custom_maruko_7500 = [
    {"name": "Richard Mille RM 011", "brand": "RM"},
    {"name": "AP Royal Oak Chronograph", "brand": "AP"},
    {"name": "Rolex GMT Pepsi", "brand": "Rolex"},
    {"name": "FP Journe Elegante", "brand": "FP Journe"},
    {"name": "Omega Planet Ocean", "brand": "Omega"},
]

# Session storage
user_sessions = {}

# Brand quality tags
brand_tags = {
    "AP": "💎",
    "Richard Mille": "💎",
    "RM": "💎",
    "FP Journe": "💎",
    "Rolex": "🟥",
    "Omega": "🟥",
    "Hublot": "🟥",
    "IWC": "🟥",
    "Panerai": "🟥",
    "Tudor": "🟩",
    "Tag Heuer": "🟩",
    "Oris": "🟩",
    "Longines": "🟩",
    "Zenith": "🟩",
    "Grand Seiko": "🟩",
}

# Helper function
def format_watch(watch):
    tag = brand_tags.get(watch["brand"], "")
    return f"{tag} {watch['name']}"

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_sessions[user_id] = {
        "clicks": 0,
        "history": [],
    }

    keyboard = [
        [InlineKeyboardButton("💵 Open $3000 Box", callback_data="box_3000")],
        [InlineKeyboardButton("💸 Open $6000 Box", callback_data="box_6000")],
        [InlineKeyboardButton("💰 Open $7500 Box", callback_data="box_7500")],
    ]
    await update.message.reply_text(
        "🎁 Welcome to The Watch King Mystery Box! Choose a box below to get started.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Button click
async def handle_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    username = query.from_user.username or ""

    await query.answer()

    session = user_sessions.get(user_id)
    if not session:
        user_sessions[user_id] = {"clicks": 0, "history": []}
        session = user_sessions[user_id]

    if session["clicks"] >= 5:
        await query.edit_message_text("⚠️ You've reached your 5 box limit.")
        return

    session["clicks"] += 1
    box_type = query.data
    is_maruko = (username.lower() == "stephenmaruko")

    if box_type == "box_3000":
        selected_watch = random.choice(watch_pool_3000)
    elif box_type == "box_6000":
        selected_watch = random.choice(watch_pool_6000)
    elif box_type == "box_7500":
        pool = custom_maruko_7500 if is_maruko else default_watch_pool_7500
        if session["clicks"] % 5 == 0:
            selected_watch = {"name": "Omega Mission to the Moon", "brand": "Omega"}
        else:
            selected_watch = random.choice(pool)
    else:
        return

    session["history"].append(selected_watch)
    if session["clicks"] >= 5:
        history_text = "\n".join([f"{i+1}. {format_watch(w)}" for i, w in enumerate(session["history"])])
        await query.edit_message_text(
            f"📦 Your box pulls are:\n\n{history_text}\n\n⚠️ You've reached your 5 box limit."
        )
    else:
        keyboard = [
            [InlineKeyboardButton("🧠 Select This Watch", callback_data="select_watch")],
            [InlineKeyboardButton("📦 Open Another Box", callback_data=box_type)],
        ]
        await query.edit_message_text(
            f"🎉 You pulled: {format_watch(selected_watch)}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# Select watch
async def handle_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    session = user_sessions.get(user_id)
    if not session or not session["history"]:
        await query.edit_message_text("⚠️ No watch selected.")
        return

    selected = session["history"][-1]
    await query.edit_message_text(f"✅ You've selected: {format_watch(selected)}. Our team will contact you shortly!")

# Main
async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_click, pattern="^box_"))
    app.add_handler(CallbackQueryHandler(handle_selection, pattern="^select_watch$"))
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
