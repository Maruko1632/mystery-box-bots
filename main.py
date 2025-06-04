import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "7561016807:AAGjG4IwayZLMMYSQmTs6zeLBDCgIWVemcI"

# Configure logging
logging.basicConfig(level=logging.INFO)

# In-memory storage for user click sessions
user_sessions = {}

# Watch pools
box_3000_watches = [
    {"name": "Tissot PRX", "brand": "Tissot"},
    {"name": "Seiko Presage", "brand": "Seiko"},
    {"name": "Hamilton Khaki Field", "brand": "Hamilton"},
    {"name": "Citizen Eco-Drive", "brand": "Citizen"},
    {"name": "Orient Bambino", "brand": "Orient"},
]

box_6000_watches = [
    {"name": "Longines HydroConquest", "brand": "Longines"},
    {"name": "Oris Aquis", "brand": "Oris"},
    {"name": "Rado Captain Cook", "brand": "Rado"},
    {"name": "TAG Heuer Formula 1", "brand": "TAG Heuer"},
    {"name": "Raymond Weil Freelancer", "brand": "Raymond Weil"},
]

box_7500_watches = [
    {"name": "Omega Seamaster", "brand": "Omega"},
    {"name": "Tudor Black Bay", "brand": "Tudor"},
    {"name": "IWC Mark XVIII", "brand": "IWC"},
    {"name": "Breitling Navitimer", "brand": "Breitling"},
    {"name": "Grand Seiko SBGA", "brand": "Grand Seiko"},
]
fixed_7500_watch = {"name": "Omega Mission to the Moon", "brand": "Omega"}

custom_stephen_watches = [
    {"name": "Rolex GMT-Master II", "brand": "Rolex"},
    {"name": "Audemars Piguet Royal Oak", "brand": "AP"},
    {"name": "Richard Mille RM 11-03", "brand": "Richard Mille"},
    {"name": "Patek Philippe Nautilus", "brand": "Patek Philippe"},
    {"name": "Hublot Big Bang", "brand": "Hublot"},
]
fixed_stephen_watch = {"name": "Richard Mille RM 055", "brand": "Richard Mille"}

def get_brand_quality(brand):
    red_brands = ["Tissot", "Citizen", "Seiko", "Orient", "Hamilton"]
    green_brands = ["Oris", "Rado", "TAG Heuer", "Raymond Weil", "Longines"]
    diamond_brands = ["Omega", "Tudor", "IWC", "Breitling", "Grand Seiko",
                      "Rolex", "AP", "Patek Philippe", "Richard Mille", "Hublot"]
    if brand in red_brands:
        return "🟥"
    elif brand in green_brands:
        return "🟩"
    elif brand in diamond_brands:
        return "💎"
    return ""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_sessions[user_id] = {
        "clicks": 0,
        "history": [],
        "box": None
    }
    keyboard = [
        [InlineKeyboardButton("$3000 Mystery Box", callback_data="box_3000")],
        [InlineKeyboardButton("$6000 Mystery Box", callback_data="box_6000")],
        [InlineKeyboardButton("$7500 Mystery Box", callback_data="box_7500")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🎁 Welcome to The Watch King Mystery Box!
Select a box below to begin:", reply_markup=reply_markup)

async def handle_box_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    box = query.data
    session = user_sessions.get(user_id, {"clicks": 0, "history": []})

    if session["clicks"] >= 5:
        await query.edit_message_text("⚠️ You've reached your 5 box limit.")
        return

    session["clicks"] += 1
    user_sessions[user_id] = session
    watch = {}

    if box == "box_7500":
        if query.from_user.username == "StephenMaruko":
            if session["clicks"] % 5 == 0:
                watch = fixed_stephen_watch
            else:
                watch = random.choice(custom_stephen_watches)
        else:
            if session["clicks"] % 5 == 0:
                watch = fixed_7500_watch
            else:
                watch = random.choice(box_7500_watches)
    elif box == "box_3000":
        watch = random.choice(box_3000_watches)
    elif box == "box_6000":
        watch = random.choice(box_6000_watches)

    quality = get_brand_quality(watch["brand"])
    session["history"].append(watch)

    if session["clicks"] >= 5:
        final_message = f"🎉 You pulled: {watch['name']} {quality}

⚠️ You've reached your 5 box limit."
        await query.edit_message_text(
            final_message,
            reply_markup=InlineKeyboardMarkup([])
        )
    else:
        await query.edit_message_text(
            f"🎉 You pulled: {watch['name']} {quality}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Open Another Box", callback_data=box)],
                [InlineKeyboardButton("Select Watch", callback_data="select_watch")]
            ])
        )

async def handle_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    session = user_sessions.get(user_id)
    if not session or not session["history"]:
        await query.edit_message_text("No selection history found.")
        return
    final_watch = session["history"][-1]
    quality = get_brand_quality(final_watch["brand"])
    await query.edit_message_text(f"✅ You selected: {final_watch['name']} {quality}
Please contact @TheWatchKing to complete your purchase.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_box_selection, pattern="^box_"))
    app.add_handler(CallbackQueryHandler(handle_selection, pattern="^select_watch$"))
    app.run_polling()
