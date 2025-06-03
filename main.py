from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import random

TOKEN = "7561016807:AAGjG4IwayZLMMYSQmTs6zeLBDCgIWVemcI"

# Define brand quality
BRAND_QUALITY = {
    "rolex": "🟩",
    "audemars": "🟩",
    "patek": "🟩",
    "richard mille": "💎"
}
DEFAULT_QUALITY = "🟥"

# Box contents
BOXES = {
    "box_3000": [
        "Rolex Oysterdate Precision 6694",
        "Rolex Air-King 5500",
        "Rolex Oyster Perpetual 1002",
        "Rolex Date 1500",
        "Rolex Oyster Precision 6426",
        "Rolex Oyster Perpetual 6564",
        "Rolex Oyster Perpetual 6430",
        "Rolex Oyster Date 6517",
        "Rolex Oyster Perpetual 6284",
        "Rolex Oyster Precision 1210"
    ],
    "box_6000": [
        "Rolex Oyster Perpetual Datejust 1601",
        "Rolex Oyster Royal",
        "Rolex Precision 9022",
        "Rolex Oyster Perpetual 6618",
        "Rolex Oyster Perpetual 67193",
        "Rolex Oyster Perpetual 76193 (Ladies)",
        "Rolex Oysterdate 6694 Linen Dial",
        "Rolex Oyster Perpetual 14233 (Ladies)"
    ],
    "box_7500": [
        "Rolex GMT-Master II",
        "Richard Mille RM 011",
        "Audemars Piguet Royal Oak Offshore",
        "Rolex Sky-Dweller",
        "Richard Mille RM 035"
    ]
}

# Custom box for StephenMaruko
CUSTOM_USER = "@StephenMaruko"
CUSTOM_WATCHES = [
    "ROLEX OYSTERDATE PRECISION",
    "Omega Speedmaster Co-Axial",
    "Rolex Oyster Perpetual 6284",
    "Audemars Piguet Royal Oak Lady",
    "TUDOR Black Bay Gmt 41 mm"
]

# User session tracking
user_sessions = {}

def get_brand_emoji(watch):
    lowered = watch.lower()
    for brand in BRAND_QUALITY:
        if brand in lowered:
            return BRAND_QUALITY[brand]
    return DEFAULT_QUALITY

def build_box_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💵 $3000 Mystery Box", callback_data="box_3000")],
        [InlineKeyboardButton("💰 $6000 Mystery Box", callback_data="box_6000")],
        [InlineKeyboardButton("💎 $7500 Mystery Box", callback_data="box_7500")]
    ])

def post_pull_buttons(box):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f"Open another {box[4:]} box", callback_data=box)],
        [InlineKeyboardButton("🎯 Select Watch", callback_data="select_watch")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_sessions[user_id] = {
        "clicks": 0,
        "box": None,
        "pulls": [],
        "last_message_id": None
    }
    await update.message.reply_text(
        "🎉 Congratulations on buying your first mystery box!\n\n"
        "Please only select the box you purchased.\n"
        "You can only open a box **5 times max** — after that, attempts will be marked invalid.\n\n"
        "Happy hunting and DM once you're done! 📩",
        reply_markup=build_box_buttons()
    )

async def handle_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    username = query.from_user.username
    data = query.data

    # Handle final selection
    if data == "select_watch":
        session = user_sessions.get(user_id)
        if not session or session["clicks"] == 0:
            await query.edit_message_text("Please open a box first.")
            return
        selected = session["pulls"][-1]
        emoji = get_brand_emoji(selected)
        await query.edit_message_text(
            f"🎉 Congratulations! You've selected your final watch:\n\n"
            f"{selected}\nBrand Quality: {emoji}\n\n"
            "Please contact us to plan pickup or shipping.\n\n"
            "⚠️ You've reached your 5 box limit."
        )
        return

    # Regular box click
    if data not in BOXES:
        await query.edit_message_text("Invalid box selected.")
        return

    # Init session if not exists
    if user_id not in user_sessions:
        user_sessions[user_id] = {"clicks": 0, "box": data, "pulls": []}

    session = user_sessions[user_id]

    if session["box"] and session["box"] != data:
        await query.edit_message_text("You can only open one box type per session.")
        return

    if session["clicks"] >= 5:
        await query.edit_message_text("⚠️ You've reached your 5 box limit.\nHope to see you again next month!")
        return

    session["clicks"] += 1
    session["box"] = data

    await query.message.reply_text(
        f"📦 Box {session['clicks']} of 5 — {random.choice(['📦 Opening your box…', '🛠 Inspecting contents…', '🧊 Sealed tight… let’s see what’s inside!'])}"
    )

    # Determine the watch
    if f"@{username}" == CUSTOM_USER and data == "box_7500":
        watch = CUSTOM_WATCHES[session["clicks"] - 1]
    elif data == "box_7500" and session["clicks"] == 5:
        watch = "Omega Mission to the Moon"
    else:
        available = [w for w in BOXES[data] if w not in session["pulls"]]
        watch = random.choice(available) if available else random.choice(BOXES[data])

    session["pulls"].append(watch)
    emoji = get_brand_emoji(watch)

    await query.message.reply_text(
        f"🎁 You got:\n{watch}\nBrand Quality: {emoji}",
        reply_markup=post_pull_buttons(data)
    )

    # Final message
    if session["clicks"] == 5:
        summary = "\n".join([f"{i+1}. {w}" for i, w in enumerate(session['pulls'])])
        await query.message.reply_text(
            f"🧾 Summary of your pulls today:\n\n{summary}\n\nSelected: ✅ {session['pulls'][-1]}\n\n🎲 Hope to see you next month"
        )

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_click))
    print("Bot started.")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
