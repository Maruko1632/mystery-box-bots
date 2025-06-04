import random
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

# Replace with your bot token
TOKEN = "7561016807:AAGjG4IwayZLMMYSQmTs6zeLBDCgIWVemcI"

# Logging setup
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Define brand qualities
brand_qualities = {
    "Rolex": "🟥",
    "Omega": "🟩",
    "Audemars Piguet": "💎",
    "Richard Mille": "💎",
    "Cartier": "🟩",
    "Tag Heuer": "🟥"
}

# Watch pools
box_3000 = [
    {"name": "Rolex Datejust", "brand": "Rolex"},
    {"name": "Omega Seamaster", "brand": "Omega"},
    {"name": "Tag Heuer Formula 1", "brand": "Tag Heuer"},
    {"name": "Cartier Tank", "brand": "Cartier"},
    {"name": "Rolex Oyster Perpetual", "brand": "Rolex"}
]

box_6000 = [
    {"name": "Omega Speedmaster", "brand": "Omega"},
    {"name": "Cartier Santos", "brand": "Cartier"},
    {"name": "Rolex Explorer", "brand": "Rolex"},
    {"name": "Tag Heuer Carrera", "brand": "Tag Heuer"},
    {"name": "Rolex Submariner", "brand": "Rolex"}
]

box_7500_pool = [
    {"name": "Audemars Piguet Royal Oak", "brand": "Audemars Piguet"},
    {"name": "Richard Mille RM 011", "brand": "Richard Mille"},
    {"name": "Rolex Day-Date", "brand": "Rolex"},
    {"name": "Omega Constellation", "brand": "Omega"},
    {"name": "Cartier Ballon Bleu", "brand": "Cartier"}
]

# Fixed reward for every 5th pull on box_7500
fixed_reward = {"name": "Omega Mission to the Moon", "brand": "Omega"}

# Per-user session data
user_sessions = {}

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🟫 Open $3,000 Box", callback_data="box_3000")],
        [InlineKeyboardButton("⬛️ Open $6,000 Box", callback_data="box_6000")],
        [InlineKeyboardButton("🟪 Open $7,500 Box", callback_data="box_7500")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🎁 Welcome to The Watch King Mystery Box!
Choose a box below to get started.", reply_markup=reply_markup)

# Generate watches from pool with quality logic
def get_box_7500_watches():
    pool = box_7500_pool.copy()
    random.shuffle(pool)

    reds = [w for w in pool if brand_qualities[w["brand"]] == "🟥"]
    greens = [w for w in pool if brand_qualities[w["brand"]] == "🟩"]
    diamonds = [w for w in pool if brand_qualities[w["brand"]] == "💎"]

    selected = []

    # Always start with a red
    if reds:
        selected.append(reds.pop())

    # Alternate filling up to 5 total
    while len(selected) < 5:
        if len([w for w in selected if brand_qualities[w["brand"]] == "🟥"]) < 2 and reds:
            selected.append(reds.pop())
        elif len([w for w in selected if brand_qualities[w["brand"]] == "🟩"]) < 3 and greens:
            selected.append(greens.pop())
        elif diamonds:
            selected.append(diamonds.pop())
        else:
            break

    while len(selected) < 5:
        filler = pool.pop()
        if filler not in selected:
            selected.append(filler)

    return selected

# Handle button click
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    session = user_sessions.setdefault(user_id, {"count": 0})
    session["count"] += 1
    box_type = query.data

    if session["count"] > 5:
        await query.edit_message_text("⚠️ You've reached your 5 box limit.")
        return

    if box_type == "box_3000":
        selected_watch = random.choice(box_3000)
    elif box_type == "box_6000":
        selected_watch = random.choice(box_6000)
    elif box_type == "box_7500":
        if session["count"] % 5 == 0:
            selected_watch = fixed_reward
        else:
            watches = get_box_7500_watches()
            selected_watch = random.choice(watches)
    else:
        return

    quality = brand_qualities[selected_watch["brand"]]
    keyboard = [[InlineKeyboardButton("🎯 Select Watch", callback_data="final_selection")]]
    await query.edit_message_text(
        f"🎉 You pulled: {selected_watch['name']}
Brand: {selected_watch['brand']} {quality}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Final selection
async def final_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    await query.edit_message_text("✅ Watch selected. We’ll contact you shortly.")
    user_sessions[user_id]["count"] = 5

# Main function
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button, pattern="^box_"))
    app.add_handler(CallbackQueryHandler(final_selection, pattern="^final_selection$"))
    app.run_polling()
