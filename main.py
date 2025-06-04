import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "7561016807:AAGjG4IwayZLMMYSQmTs6zeLBDCgIWVemcI"

# Watch data organized by box tier
box_data = {
    "3000": {
        "watches": [
            {"name": "Tissot PRX", "brand": "Tissot", "quality": "🟩"},
            {"name": "Hamilton Khaki Field", "brand": "Hamilton", "quality": "🟩"},
            {"name": "Oris Aquis", "brand": "Oris", "quality": "🟥"},
            {"name": "Longines HydroConquest", "brand": "Longines", "quality": "🟥"},
            {"name": "Sinn 556", "brand": "Sinn", "quality": "🟥"}
        ]
    },
    "6000": {
        "watches": [
            {"name": "Omega Seamaster", "brand": "Omega", "quality": "🟥"},
            {"name": "Tudor Black Bay", "brand": "Tudor", "quality": "🟥"},
            {"name": "Breitling Superocean", "brand": "Breitling", "quality": "🟥"},
            {"name": "Tag Heuer Monaco", "brand": "Tag Heuer", "quality": "🟩"},
            {"name": "Nomos Tangente", "brand": "Nomos", "quality": "🟩"}
        ]
    },
    "7500": {
        "watches": [
            {"name": "Rolex Datejust", "brand": "Rolex", "quality": "💎"},
            {"name": "Cartier Santos", "brand": "Cartier", "quality": "💎"},
            {"name": "Omega Speedmaster", "brand": "Omega", "quality": "🟥"},
            {"name": "Grand Seiko Snowflake", "brand": "Grand Seiko", "quality": "🟩"},
            {"name": "Panerai Luminor", "brand": "Panerai", "quality": "🟩"},
            {"name": "Omega Mission to the Moon", "brand": "Omega", "quality": "💎"}  # Guaranteed every 5th pull
        ]
    }
}

user_sessions = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_sessions[user_id] = {"clicks": 0}
    keyboard = [
        [InlineKeyboardButton("$3000 Box", callback_data="box_3000")],
        [InlineKeyboardButton("$6000 Box", callback_data="box_6000")],
        [InlineKeyboardButton("$7500 Box", callback_data="box_7500")]
    ]
    await update.message.reply_text("🎁 Choose a Mystery Box to open:", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_box_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    box_key = query.data.replace("box_", "")
    session = user_sessions.get(user_id, {"clicks": 0})

    if session["clicks"] >= 5:
        await query.edit_message_text("⚠️ You've reached your 5 box limit.")
        return

    session["clicks"] += 1
    box_info = box_data[box_key]
    click_num = session["clicks"]

    # Logic for guaranteed watch on 5th click in 7500 box
    if box_key == "7500" and click_num % 5 == 0:
        selected_watch = next(w for w in box_info["watches"] if w["name"] == "Omega Mission to the Moon")
    else:
        non_guaranteed = [w for w in box_info["watches"] if w["name"] != "Omega Mission to the Moon"]
        selected_watch = random.choice(non_guaranteed)

    user_sessions[user_id] = session  # Save session state
    keyboard = [[InlineKeyboardButton("Open Another Box", callback_data=f"box_{box_key}")]]
    await query.edit_message_text(
        f"🎉 You pulled: {selected_watch['name']}
Brand: {selected_watch['brand']} {selected_watch['quality']}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def main():
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_box_selection))

    app.run_polling()

if __name__ == "__main__":
    main()
