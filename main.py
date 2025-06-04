import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "7561016807:AAGjG4IwayZLMMYSQmTs6zeLBDCgIWVemcI"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Watch pools
box_7500_watches = [
    {"name": "Rolex Datejust", "brand": "Rolex", "quality": "🟥"},
    {"name": "Omega Speedmaster", "brand": "Omega", "quality": "🟥"},
    {"name": "Cartier Santos", "brand": "Cartier", "quality": "🟩"},
    {"name": "Tag Heuer Carrera", "brand": "Tag Heuer", "quality": "🟩"},
    {"name": "IWC Portofino", "brand": "IWC", "quality": "🟩"},
    {"name": "Patek Philippe Nautilus", "brand": "Patek", "quality": "💎"},
    {"name": "Audemars Piguet Royal Oak", "brand": "AP", "quality": "💎"},
]

# Store per-user state
user_sessions = {}

def get_random_watch_by_quality(quality, exclude_names=[], limit=None):
    pool = [w for w in box_7500_watches if w["quality"] == quality and w["name"] not in exclude_names]
    selected = random.sample(pool, min(len(pool), limit or len(pool)))
    return selected

def generate_box_7500_selection(user_id):
    if user_sessions.get(user_id, {}).get("diamond_given"):
        diamond_pool = []
    else:
        diamond_pool = get_random_watch_by_quality("💎", limit=1)
        user_sessions[user_id]["diamond_given"] = True if diamond_pool else False

    red_pool = get_random_watch_by_quality("🟥", exclude_names=[w["name"] for w in diamond_pool], limit=2)
    green_pool = get_random_watch_by_quality("🟩", exclude_names=[w["name"] for w in diamond_pool], limit=3)

    combined = red_pool + green_pool + diamond_pool
    random.shuffle(combined)
    return combined[:5]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_sessions[user_id] = {"clicks": 0, "diamond_given": False}
    keyboard = [
        [InlineKeyboardButton("Open $7500 Box 💎", callback_data="open_box_7500")],
    ]
    await update.message.reply_text("🎁 Welcome! Choose a mystery box to open:", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_box_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    session = user_sessions.setdefault(user_id, {"clicks": 0, "diamond_given": False})
    if session["clicks"] >= 5:
        await query.edit_message_text("⚠️ You've reached your 5 box limit.")
        return

    selection = generate_box_7500_selection(user_id)
    selected_watch = random.choice(selection)
    session["clicks"] += 1

    result_text = (
        f"🎉 You pulled: {selected_watch['name']}
"
        f"Brand: {selected_watch['brand']}
"
        f"Quality: {selected_watch['quality']}
"
        f"Box: 💎 $7500 Tier

"
        f"{'⚠️ You've reached your 5 box limit.' if session['clicks'] == 5 else 'You have ' + str(5 - session['clicks']) + ' pulls left.'}"
    )

    keyboard = []
    if session["clicks"] < 5:
        keyboard.append([InlineKeyboardButton("Open Another", callback_data="open_box_7500")])

    await query.edit_message_text(result_text, reply_markup=InlineKeyboardMarkup(keyboard) if keyboard else None)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handle_box_click, pattern="open_box_7500"))
app.run_polling()
