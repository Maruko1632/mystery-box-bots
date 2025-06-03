from pathlib import Path

# Full fixed bot code with user's required features and structure
bot_code = '''
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import random, asyncio

user_sessions = {}

# WATCH POOLS

box_3000_watches = [
    "Rolex Oyster Precision 6426 🟩", "Rolex Oysterdate Precision 6694 🟩", "Rolex Air-King 5500 🟩",
    "Rolex Oyster Perpetual 1002 🟩", "Rolex Date 1500 🟩", "Rolex Oyster Perpetual 6564 🟩",
    "Rolex Oyster Perpetual 6430 🟩", "Rolex Oyster Date 6517 🟩", "Rolex Oyster Perpetual 6284 🟩",
    "Rolex Oyster Precision 1210 🟩", "Rolex Datejust 1601 🟩", "Rolex Oyster Royal 🟩"
]

box_6000_watches = [
    "Omega Seamaster Aqua Terra 🟥", "Tudor Pelagos FXD 🟥", "Omega Speedmaster Racing 🟥",
    "Tudor Heritage Chrono 🟥", "Breitling Colt 🟥", "Longines HydroConquest 🟥",
    "Tag Heuer Carrera 🟥", "Rado Captain Cook 🟥"
]

box_7500_green = [
    "Rolex Datejust 16234 🟩", "Audemars Piguet Royal Oak 15300 🟩",
    "Rolex Submariner 16610 🟩", "Rolex GMT-Master II 🟩",
    "Audemars Piguet Offshore Diver 🟩", "Rolex Yacht-Master 🟩",
    "Rolex Day-Date 18038 🟩", "Patek Philippe Calatrava 🟩"
]

box_7500_red = [
    "Omega Speedmaster '57 🟥", "Tudor Black Bay Fifty-Eight 🟥", "Tag Heuer Monaco 🟥",
    "Longines Master Collection 🟥", "Breitling SuperOcean 🟥"
]

box_7500_diamond = [
    "Richard Mille RM 005 💎", "Richard Mille RM 010 💎"
]

stephen_watches = [
    "ROLEX OYSTERDATE PRECISION 🟩", "Omega Speedmaster Co-Axial 🟥",
    "Rolex Oyster Perpetual 6284 🟩", "Audemars Piguet Royal Oak Lady 🟩",
    "TUDOR Black Bay Gmt 41 mm 🟥"
]

box_condition_messages = [
    "📦 Opening your box...", "🛠 Inspecting contents...", "🧊 Sealed tight… let’s see what’s inside!"
]

# FUNCTIONS

def generate_7500_watch(username, box_number, history):
    if username == "StephenMaruko":
        return stephen_watches[box_number - 1] if box_number <= 4 else stephen_watches[4]

    if box_number == 5:
        return random.choice(box_7500_diamond)

    while True:
        red = random.sample([w for w in box_7500_red if w not in history], 2)
        green = random.sample([w for w in box_7500_green if w not in history], 3)
        picks = red + green

        # Add 1 diamond if lucky (20% chance)
        if random.random() < 0.2 and not any("💎" in w for w in history):
            picks[random.randint(0, 4)] = random.choice(box_7500_diamond)

        random.shuffle(picks)
        if picks[0].endswith("🟥") and not any(picks[i].split()[-1] == picks[i+1].split()[-1] for i in range(len(picks)-1)):
            return picks[0]

def get_brand_emoji(watch):
    return watch.split()[-1]

# COMMANDS

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_sessions[user_id] = {"clicks": 0, "history": []}

    keyboard = [
        [InlineKeyboardButton("💵 $3000 Mystery Box", callback_data="box_3000")],
        [InlineKeyboardButton("💰 $6000 Mystery Box", callback_data="box_6000")],
        [InlineKeyboardButton("💎 $7500 Mystery Box", callback_data="box_7500")]
    ]
    await update.message.reply_text(
        "🎉 Congratulations on buying your first mystery box!\n\n"
        "Please only select the box you purchased.\n"
        "You can only open a box **5 times max** — after that, attempts will be blocked.\n\n"
        "Happy hunting and DM once you're done! 📩",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# CALLBACK

async def handle_box(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    username = query.from_user.username or str(user_id)
    data = query.data

    if user_id not in user_sessions:
        user_sessions[user_id] = {"clicks": 0, "history": []}
    session = user_sessions[user_id]

    if session["clicks"] >= 5 and data != "restart":
        return

    if data.startswith("box_"):
        box_type = data
        session["clicks"] += 1
        box_number = session["clicks"]
        await query.message.reply_text(f"{random.choice(box_condition_messages)}\n📦 Box {box_number} of 5")

        if box_type == "box_7500":
            watch = generate_7500_watch(username, box_number, session["history"])
        elif box_type == "box_3000":
            pool = [w for w in box_3000_watches if w not in session["history"]]
            watch = random.choice(pool)
        elif box_type == "box_6000":
            pool = [w for w in box_6000_watches if w not in session["history"]]
            watch = random.choice(pool)

        session["history"].append(watch)

        if box_number < 5:
            keyboard = [
                [InlineKeyboardButton(f"Open another ${box_type.split('_')[1]} box", callback_data=box_type)],
                [InlineKeyboardButton("🎯 Select Watch", callback_data="select_watch")]
            ]
            await query.message.reply_text(
                f"🎉 You pulled:\n\n{watch}\n\nBrand Quality: {get_brand_emoji(watch)}",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            await send_final_summary(query, session, watch)

    elif data == "select_watch":
        if session["history"]:
            selected = session["history"][-1]
            session["clicks"] = 5
            await send_final_summary(query, session, selected)

    elif data == "restart":
        await start(update, context)

async def send_final_summary(query, session, selected):
    summary = "\n".join([f"{i+1}. {w}" for i, w in enumerate(session["history"])])
    summary += f"\n\nSelected: ✅ {selected}"
    await query.message.reply_text(
        f"🎉 Congratulations! You've selected your final watch:\n\n"
        f"{selected}\n\n"
        "Please contact us to plan pickup or shipping.\n\n"
        "⚠️ You've reached your 5 box limit.\n\n"
        f"🧾 Summary of your pulls today:\n{summary}",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎲 Hope to see you next month", callback_data="restart")]])
    )

# RUN

async def main():
    app = ApplicationBuilder().token("7561016807:AAGjG4IwayZLMMYSQmTs6zeLBDCgIWVemcI").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_box))
    await app.run_polling()

try:
    asyncio.get_running_loop().create_task(main())
except RuntimeError:
    asyncio.run(main())
'''

output_path = Path("/mnt/data/mystery_box_bot_complete.py")
output_path.write_text(bot_code)
output_path
