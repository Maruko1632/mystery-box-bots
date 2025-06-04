from pathlib import Path

# Create the correct directory if it doesn't exist
output_dir = Path("/mnt/data")
output_dir.mkdir(parents=True, exist_ok=True)

# Prepare the fixed bot code
bot_code = '''from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import random, asyncio

user_sessions = {}

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

box_7500_watches_red = [
    "Omega Speedmaster Racing 🟥", "Tudor Pelagos FXD 🟥", "Omega Seamaster Aqua Terra 🟥",
    "TUDOR Black Bay Gmt 41 mm 🟥"
]

box_7500_watches_green = [
    "Rolex Datejust 16234 🟩", "Audemars Piguet Royal Oak 15300 🟩", "Rolex Submariner 16610 🟩",
    "Rolex GMT-Master II 🟩", "Audemars Piguet Offshore Diver 🟩", "Rolex Yacht-Master 🟩"
]

box_7500_watches_diamond = [
    "Richard Mille RM 005 💎", "Richard Mille RM 010 💎"
]

stephen_watches = [
    "ROLEX OYSTERDATE PRECISION 🟩", "Omega Speedmaster Co-Axial 🟥", "Rolex Oyster Perpetual 6284 🟩",
    "Audemars Piguet Royal Oak Lady 🟩", "TUDOR Black Bay Gmt 41 mm 🟥"
]

box_condition_messages = [
    "📦 Opening your box...", "🛠 Inspecting contents...", "🧊 Sealed tight… let’s see what’s inside!"
]

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
        "You can only open a box **5 times max** — after that, attempts will be marked invalid.\n\n"
        "Happy hunting and DM once you're done! 📩",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_box(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    username = query.from_user.username or str(user_id)
    data = query.data

    if user_id not in user_sessions:
        user_sessions[user_id] = {"clicks": 0, "history": []}
    session = user_sessions[user_id]

    if data.startswith("box_"):
        box_type = data
        if session["clicks"] >= 5:
            await query.message.reply_text("⚠️ You've reached your 5 box limit.\n\n🎲 Hope to see you next month.")
            return

        session["clicks"] += 1
        box_number = session["clicks"]
        await query.message.reply_text(f"{random.choice(box_condition_messages)}\n📦 Box {box_number} of 5")

        if box_type == "box_7500":
            if username == "StephenMaruko":
                watch = stephen_watches[box_number - 1] if box_number <= 5 else stephen_watches[-1]
            elif box_number == 5:
                watch = "Richard Mille RM 010 💎"
            else:
                # Ensure 2 red, 3 green, no duplicates, never 2 red in a row
                prev_watch = session["history"][-1] if session["history"] else ""
                reds = [w for w in box_7500_watches_red if w not in session["history"]]
                greens = [w for w in box_7500_watches_green if w not in session["history"]]
                if box_number == 1 or (prev_watch and prev_watch.endswith("🟩")):
                    watch = random.choice(reds) if reds else random.choice(box_7500_watches_red)
                else:
                    watch = random.choice(greens) if greens else random.choice(box_7500_watches_green)
        elif box_type == "box_3000":
            pool = [w for w in box_3000_watches if w not in session["history"]]
            watch = random.choice(pool) if pool else random.choice(box_3000_watches)
        elif box_type == "box_6000":
            pool = [w for w in box_6000_watches if w not in session["history"]]
            watch = random.choice(pool) if pool else random.choice(box_6000_watches)
        else:
            await query.message.reply_text("Invalid box selected.")
            return

        session["history"].append(watch)

        buttons = []
        if session["clicks"] < 5:
            buttons.append([InlineKeyboardButton(f"Open another ${box_type.split('_')[1]} box", callback_data=box_type)])
            buttons.append([InlineKeyboardButton("🎯 Select Watch", callback_data="select_watch")])
        elif session["clicks"] == 5:
            summary = "\n".join([f"{i+1}. {w}" for i, w in enumerate(session["history"])])
            summary += f"\n\nSelected: ✅ {watch}"
            await query.message.reply_text(
                f"🎉 Congratulations! You've selected your final watch:\n\n"
                f"{watch}\n\n"
                "Please contact us to plan pickup or shipping.\n\n"
                "⚠️ You've reached your 5 box limit.\n\n"
                f"🧾 Summary of your pulls today:\n{summary}",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎲 Hope to see you next month", callback_data="restart")]])
            )
            return

        await query.message.reply_text(
            f"🎉 You pulled:\n\n{watch}\n\nBrand Quality: {watch.split()[-1]}",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    elif data == "select_watch":
        if session["history"]:
            selected = session["history"][-1]
            session["clicks"] = 5
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

    elif data == "restart":
        user_sessions[user_id] = {"clicks": 0, "history": []}
        await start(update, context)

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

# Save to a new .py file
file_path = output_dir / "mystery_box_bot_copy_paste_final.py"
file_path.write_text(bot_code)

file_path.name
