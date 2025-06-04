from pathlib import Path

# Load the final corrected version of the mystery box bot with all features preserved
bot_code = """
import logging
import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# TOKEN setup (replace this with your actual token)
TOKEN = "7561016807:AAGjG4IwayZLMMYSQmTs6zeLBDCgIWVemcI"

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Watch pools
box_3000 = [
    {"name": "Tudor Black Bay", "quality": "🟩"},
    {"name": "Cartier Tank", "quality": "🟥"},
    {"name": "Tag Heuer Carrera", "quality": "🟩"},
    {"name": "Oris Aquis", "quality": "🟩"},
    {"name": "Longines HydroConquest", "quality": "🟥"},
]

box_6000 = [
    {"name": "Omega Seamaster", "quality": "🟥"},
    {"name": "Breitling Navitimer", "quality": "🟩"},
    {"name": "IWC Pilot", "quality": "🟩"},
    {"name": "Cartier Santos", "quality": "🟥"},
    {"name": "Zenith Chronomaster", "quality": "🟩"},
]

default_7500_pool = [
    {"name": "Rolex Datejust", "quality": "🟥"},
    {"name": "Omega Speedmaster", "quality": "🟩"},
    {"name": "Panerai Luminor", "quality": "🟩"},
    {"name": "Hublot Classic Fusion", "quality": "🟥"},
    {"name": "Tudor Pelagos", "quality": "🟩"},
]
special_watch = {"name": "Omega Mission to the Moon", "quality": "💎"}

stephen_custom_pool = [
    {"name": "Audemars Piguet Royal Oak", "quality": "💎"},
    {"name": "Rolex Submariner", "quality": "🟥"},
    {"name": "Patek Philippe Nautilus", "quality": "💎"},
    {"name": "Omega Speedmaster '57", "quality": "🟩"},
    {"name": "IWC Portugieser", "quality": "🟩"},
]

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data[user_id] = {
        "click_count": 0,
        "history": [],
    }
    keyboard = [
        [InlineKeyboardButton("🎁 Open $3000 Box", callback_data='box_3000')],
        [InlineKeyboardButton("🎁 Open $6000 Box", callback_data='box_6000')],
        [InlineKeyboardButton("🎁 Open $7500 Box", callback_data='box_7500')],
    ]
    await update.message.reply_text("Welcome to The Watch King Mystery Box Bot!\nSelect a box to open:", reply_markup=InlineKeyboardMarkup(keyboard))

def get_box_watches(user_id, box_type):
    if box_type == "box_7500":
        pool = stephen_custom_pool if user_id == 123456789 else default_7500_pool
        click_count = user_data[user_id]["click_count"]
        if click_count == 4:
            return [special_watch]
        return random.sample(pool, 5)
    return random.sample(box_3000 if box_type == "box_3000" else box_6000, 5)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    box_type = query.data

    if user_id not in user_data:
        user_data[user_id] = {"click_count": 0, "history": []}

    if user_data[user_id]["click_count"] >= 5:
        await query.edit_message_text("⚠️ You've reached your 5 box limit.")
        return

    watches = get_box_watches(user_id, box_type)
    selected_watch = watches[0]

    user_data[user_id]["click_count"] += 1
    user_data[user_id]["history"].append(selected_watch)

    message = f"🎉 You pulled: {selected_watch['name']} {selected_watch['quality']}\n\n"
    message += f"Box: {box_type.upper()} | Pull #{user_data[user_id]['click_count']}/5"

    keyboard = []
    if user_data[user_id]["click_count"] < 5:
        keyboard.append([InlineKeyboardButton("🔁 Open another box", callback_data=box_type)])
    else:
        message += "\n\n⚠️ You've reached your 5 box limit."

    await query.edit_message_text(message, reply_markup=InlineKeyboardMarkup(keyboard) if keyboard else None)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

if __name__ == "__main__":
    import asyncio
    asyncio.run(app.run_polling())
"""

# Save the corrected final version
output_path = Path("/mnt/data/mystery_box_bot_final_fixed_full.py")
output_path.write_text(bot_code)
output_path
