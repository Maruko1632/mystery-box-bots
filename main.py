from pathlib import Path

# Full, corrected bot code based on the final validated version
bot_code = '''
import asyncio
import random
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)
TOKEN = "7561016807:AAGjG4IwayZLMMYSQmTs6zeLBDCgIWVemcI"
MAX_OPENS = 5

user_sessions = {}

BOXES = {
    "box_3000": [
        ("Rolex Oyster Precision 6426", "🟩"),
        ("Rolex Oysterdate Precision 6694", "🟩"),
        ("Rolex Air-King 5500", "🟩"),
        ("Omega Seamaster", "🟥"),
        ("Tissot Visodate", "🟥"),
        ("Hamilton Jazzmaster", "🟥"),
        ("Longines HydroConquest", "🟥"),
        ("Seiko Presage", "🟥"),
        ("Citizen Promaster", "🟥"),
    ],
    "box_6000": [
        ("Rolex Date 1500", "🟩"),
        ("Omega Aqua Terra", "🟥"),
        ("Tudor Black Bay", "🟥"),
        ("Tag Heuer Carrera", "🟥"),
        ("Raymond Weil Freelancer", "🟥"),
        ("Seiko SPB143", "🟥"),
        ("Longines Master Collection", "🟥"),
    ],
    "box_7500": [
        ("Rolex Submariner", "🟩"),
        ("Richard Mille RM 005", "💎"),
        ("Audemars Piguet Royal Oak", "🟩"),
        ("Rolex Yacht-Master", "🟩"),
        ("Richard Mille RM 010", "💎"),
        ("Omega Seamaster", "🟥"),
        ("Tag Heuer Formula 1", "🟥"),
        ("Tissot Gentleman", "🟥"),
        ("Hamilton Khaki", "🟥"),
    ]
}

CUSTOM_USERS = {
    "StephenMaruko": [
        ("ROLEX OYSTERDATE PRECISION", "🟩"),
        ("Omega Speedmaster Co-Axial", "🟥"),
        ("Rolex Oyster Perpetual 6284", "🟩"),
        ("Audemars Piguet Royal Oak Lady", "🟩"),
        ("TUDOR Black Bay Gmt 41 mm", "🟥")
    ]
}

def get_box_flavor():
    return random.choice([
        "📦 Opening your box…",
        "🛠 Inspecting contents…",
        "🧊 Sealed tight… let’s see what’s inside!"
    ])

def select_watches(box, username):
    if box == "box_7500" and username == "StephenMaruko":
        return CUSTOM_USERS["StephenMaruko"]
    pool = BOXES[box][:]
    red = [w for w in pool if w[1] == "🟥"]
    green = [w for w in pool if w[1] == "🟩"]
    diamond = [w for w in pool if w[1] == "💎"]
    random.shuffle(red)
    random.shuffle(green)
    selected = [red.pop(), green.pop(), red.pop(), green.pop()]
    if box == "box_7500" and diamond:
        selected.append(diamond.pop())
    random.shuffle(selected[1:])  # Always start with red
    return [selected[0]] + sorted(selected[1:], key=lambda x: x[1])

def get_session(user_id):
    if user_id not in user_sessions:
        user_sessions[user_id] = {"pulls": [], "final": None}
    return user_sessions[user_id]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_sessions[user_id] = {"pulls": [], "final": None}
    keyboard = [
        [InlineKeyboardButton("💼 $3000 Box", callback_data="box_3000")],
        [InlineKeyboardButton("🧳 $6000 Box", callback_data="box_6000")],
        [InlineKeyboardButton("🎁 $7500 Box", callback_data="box_7500")],
    ]
    await update.message.reply_text(
        "🎉 Congratulations on buying your first mystery box!\n\n"
        "Please only select the box you purchased.\n"
        "You can only open a box 5 times max — after that, attempts will be marked invalid.\n\n"
        "Happy hunting and DM once you're done! 📩",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    session = get_session(user_id)
    if session["final"]:
        return await query.edit_message_text("⚠️ You've already selected your final watch.")
    box = query.data
    if len(session["pulls"]) >= MAX_OPENS:
        return await query.edit_message_text(
            "⚠️ You've reached your 5 box limit.\n\n"
            "🎉 Congratulations! You've selected your final watch:\n\n"
            f"{session['pulls'][-1][0]}\n"
            f"Brand Quality: {session['pulls'][-1][1]}\n\n"
            "Please contact us to plan pickup or shipping."
        )
    selected_watches = select_watches(box, query.from_user.username or "")
    watch = selected_watches[len(session["pulls"]) % 5]
    session["pulls"].append(watch)
    flavor = get_box_flavor()
    progress = f"📦 Box {len(session['pulls'])} of {MAX_OPENS}"
    text = f"{flavor}\n\n{progress}\n\n🎯 You got:\n{watch[0]}\nBrand Quality: {watch[1]}"
    buttons = []
    if len(session["pulls"]) < MAX_OPENS:
        buttons.append([InlineKeyboardButton(f"Open another {box[-4:]} box", callback_data=box)])
        buttons.append([InlineKeyboardButton("🎯 Select Watch", callback_data="select")])
    else:
        session["final"] = watch
        buttons.append([InlineKeyboardButton("🎲 Hope to see you next month", callback_data="reset")])
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(buttons))

async def select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    session = get_session(user_id)
    if not session["pulls"]:
        return await query.edit_message_text("❗ You haven't opened any boxes yet.")
    session["final"] = session["pulls"][-1]
    pulls_summary = "\n".join([f"{i+1}. {w[0]}" for i, w in enumerate(session["pulls"])])
    await query.edit_message_text(
        f"🧾 Summary of your pulls today:\n\n{pulls_summary}\n\n"
        f"Selected: ✅ {session['final'][0]}\n\n"
        "🎉 Congratulations! You've selected your final watch:\n\n"
        f"{session['final'][0]}\n"
        f"Brand Quality: {session['final'][1]}\n\n"
        "Please contact us to plan pickup or shipping.\n\n"
        "⚠️ You've reached your 5 box limit."
    )

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await start(update, context)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button, pattern="^box_"))
    app.add_handler(CallbackQueryHandler(select, pattern="^select$"))
    app.add_handler(CallbackQueryHandler(reset, pattern="^reset$"))
    app.run_polling()

if __name__ == "__main__":
    main()
'''

# Save it to a file so the user can copy or download
output_path = Path("/mnt/data/mystery_box_bot_final.py")
output_path.write_text(bot_code)
output_path
