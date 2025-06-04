import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "7561016807:AAGjG4IwayZLMMYSQmTs6zeLBDCgIWVemcI"

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Watch pools
box_7500 = [
    {"name": "Rolex Submariner", "brand": "Rolex", "quality": "🟥"},
    {"name": "Omega Seamaster", "brand": "Omega", "quality": "🟥"},
    {"name": "Tudor Black Bay", "brand": "Tudor", "quality": "🟩"},
    {"name": "Tag Heuer Monaco", "brand": "Tag Heuer", "quality": "🟩"},
    {"name": "Cartier Santos", "brand": "Cartier", "quality": "🟩"},
    {"name": "Richard Mille RM11", "brand": "Richard Mille", "quality": "💎"},
]

user_sessions = {}

def build_selection():
    red = [w for w in box_7500 if w["quality"] == "🟥"]
    green = [w for w in box_7500 if w["quality"] == "🟩"]
    diamond = [w for w in box_7500 if w["quality"] == "💎"]

    selection = []
    selection.extend(random.sample(red, 2))
    selection.extend(random.sample(green, 3))

    if random.random() < 0.3:
        selection[random.randint(0, 4)] = random.choice(diamond)

    random.shuffle(selection)
    return selection

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_sessions[user_id] = {"clicks": 0, "history": []}
    keyboard = [[InlineKeyboardButton("Open $7500 Box", callback_data="box_7500")]]
    await update.message.reply_text("🎁 Choose a mystery box:", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if user_id not in user_sessions:
        user_sessions[user_id] = {"clicks": 0, "history": []}

    if user_sessions[user_id]["clicks"] >= 5:
        await query.edit_message_text("⚠️ You've reached your 5 box limit.")
        return

    selected_watches = build_selection()
    selected_watch = random.choice(selected_watches)

    user_sessions[user_id]["clicks"] += 1
    user_sessions[user_id]["history"].append(selected_watch["name"])

    keyboard = []
    if user_sessions[user_id]["clicks"] < 5:
        keyboard.append([InlineKeyboardButton("Open Another", callback_data="box_7500")])
    else:
        keyboard.append([InlineKeyboardButton("Done", callback_data="done")])

    await query.edit_message_text(
        text=f"🎉 You pulled: {selected_watch['name']} {selected_watch['quality']}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Thanks for playing!")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_click, pattern="box_7500"))
    app.add_handler(CallbackQueryHandler(done, pattern="done"))
    app.run_polling()
