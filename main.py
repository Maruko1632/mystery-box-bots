from pathlib import Path

# Fixed complete mystery box bot code with TOKEN= format
bot_code = """
import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = "7561016807:AAGjG4IwayZLMMYSQmTs6zeLBDCgIWVemcI"

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Per-user click tracking
user_clicks = {}

# Watch pools
box_3000 = [
    ("Tudor Black Bay", "🟥"), ("Longines HydroConquest", "🟩"),
    ("Oris Aquis Date", "🟩"), ("Tag Heuer Formula 1", "🟩"),
    ("Hamilton Khaki Field", "🟥")
]

box_6000 = [
    ("Omega Seamaster", "🟩"), ("Breitling Superocean", "🟩"),
    ("Grand Seiko GMT", "🟥"), ("Tag Heuer Carrera", "🟥"),
    ("Zenith Elite", "🟩")
]

box_7500 = [
    ("Rolex Datejust", "🟩"), ("Omega Speedmaster", "🟥"),
    ("Panerai Luminor", "🟥"), ("IWC Portofino", "🟩"),
    ("Hublot Classic Fusion", "🟩")
]

omega_special = "💎 Omega Mission to the Moon"

def generate_watches(box, user_id, box_name):
    if user_id == "StephenMaruko" and box_name == "7500":
        custom_list = [
            ("AP Royal Oak", "💎"), ("Richard Mille RM010", "💎"),
            ("Rolex Daytona", "💎"), ("Patek Philippe Nautilus", "💎"),
            ("Omega Mission to the Moon", "💎")
        ]
        return custom_list if (user_clicks[user_id]["count"] + 1) % 5 == 0 else random.sample(custom_list, 5)
    if box_name == "7500" and (user_clicks[user_id]["count"] + 1) % 5 == 0:
        return [("Omega Mission to the Moon", "💎")] * 5
    return random.sample(box, 5)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.username or update.effective_user.id)
    user_clicks[user_id] = {"count": 0, "history": []}

    keyboard = [
        [InlineKeyboardButton("$3000 Mystery Box", callback_data="box_3000")],
        [InlineKeyboardButton("$6000 Mystery Box", callback_data="box_6000")],
        [InlineKeyboardButton("$7500 Mystery Box", callback_data="box_7500")]
    ]
    await update.message.reply_text("🎉 Welcome to the Mystery Box Bot! Choose a box:", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = str(query.from_user.username or query.from_user.id)

    if user_id not in user_clicks:
        user_clicks[user_id] = {"count": 0, "history": []}

    if user_clicks[user_id]["count"] >= 5:
        await query.answer()
        await query.edit_message_text("⚠️ You've reached your 5 box limit.")
        return

    box_name = query.data.split("_")[1]
    box_pool = box_3000 if box_name == "3000" else box_6000 if box_name == "6000" else box_7500
    watches = generate_watches(box_pool, user_id, box_name)

    display = "\n".join([f"{quality} {watch}" for watch, quality in watches])
    user_clicks[user_id]["count"] += 1
    user_clicks[user_id]["history"].append(watches)

    button_text = "Open Another Box" if user_clicks[user_id]["count"] < 5 else "Select Watch"
    reply_markup = InlineKeyboardMarkup.from_button(
        InlineKeyboardButton(button_text, callback_data=query.data)
    )

    await query.answer()
    await query.edit_message_text(f"🎁 Box {user_clicks[user_id]['count']} Results:\n\n{display}", reply_markup=reply_markup)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_click))
    app.run_polling()

if __name__ == "__main__":
    main()
"""

# Save the full working bot code to a file
output_path = Path("/mnt/data/mystery_box_bot_final_token_style.py")
output_path.write_text(bot_code)
output_path
