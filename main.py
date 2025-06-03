from pathlib import Path

# Full updated code with 7500 box logic fixed, ensuring:
# - 2 reds, 2 greens, and a 15% chance of 1 diamond
# - No back-to-back same quality
# - Starts with a red
code = '''import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes

TOKEN = "7561016807:AAGjG4IwayZLMMYSQmTs6zeLBDCgIWVemcI"

user_clicks = {}
user_histories = {}

red_watches = [
    "Tudor Black Bay 58", "Omega Seamaster", "TAG Heuer Aquaracer", "Longines HydroConquest",
    "Oris Aquis Date", "Hamilton Jazzmaster", "Tissot PRX", "Rado Captain Cook"
]

green_watches = [
    "Rolex Explorer", "Audemars Piguet Royal Oak", "Rolex Submariner", "Rolex Datejust",
    "Patek Philippe Aquanaut", "Cartier Santos", "Vacheron Constantin Fiftysix"
]

diamond_watches = [
    "Richard Mille RM 011", "Richard Mille RM 035"
]

BRAND_QUALITY = {
    "Tudor": "🟥",
    "Omega": "🟥",
    "TAG": "🟥",
    "Longines": "🟥",
    "Oris": "🟥",
    "Hamilton": "🟥",
    "Tissot": "🟥",
    "Rado": "🟥",
    "Cartier": "🟩",
    "Vacheron": "🟩",
    "Patek": "🟩",
    "Rolex": "🟩",
    "Audemars": "🟩",
    "Richard": "💎"
}

def get_brand_quality(watch_name):
    for brand, quality in BRAND_QUALITY.items():
        if brand in watch_name:
            return quality
    return "🟥"

def generate_7500_box():
    box = []
    red_choices = random.sample(red_watches, 2)
    green_choices = random.sample(green_watches, 2)
    diamond_choice = random.sample(diamond_watches, 1) if random.random() < 0.15 else []

    full_box = red_choices + green_choices + diamond_choice
    random.shuffle(full_box)

    # Ensure first item is red
    red_first = next((w for w in full_box if get_brand_quality(w) == "🟥"), None)
    if red_first:
        full_box.remove(red_first)
        full_box.insert(0, red_first)

    # Ensure no back-to-back same brand quality
    for i in range(len(full_box) - 1):
        while get_brand_quality(full_box[i]) == get_brand_quality(full_box[i + 1]):
            random.shuffle(full_box[i+1:])

    return full_box[:5]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.effective_user.username
    user_clicks[username] = 0
    user_histories[username] = []
    buttons = [
        [InlineKeyboardButton("$3000 Box", callback_data="box_3000")],
        [InlineKeyboardButton("$6000 Box", callback_data="box_6000")],
        [InlineKeyboardButton("$7500 Box", callback_data="box_7500")]
    ]
    await update.message.reply_text(
        "🎉 Congratulations on buying your first mystery box!\n\n"
        "Please only select the box you purchased.\n"
        "You can only open a box 5 times max — after that, attempts will be marked invalid.\n\n"
        "Happy hunting and DM once you're done! 📩",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

async def handle_box_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    username = query.from_user.username
    box_type = query.data

    if username not in user_clicks:
        user_clicks[username] = 0
        user_histories[username] = []

    if user_clicks[username] >= 5:
        await query.edit_message_text("⚠️ You've reached your 5 box limit.\n"
                                      "🎉 Congratulations! You've selected your final watch:\n"
                                      f"✅ {user_histories[username][-1]} \n"
                                      f"Brand Quality: {get_brand_quality(user_histories[username][-1])}\n\n"
                                      "Please contact us to plan pickup or shipping.\n\n"
                                      "🎲 Hope to see you next month.")
        return

    if box_type == "box_7500":
        if user_clicks[username] == 0:
            context.user_data["box7500_watches"] = generate_7500_box()
        selected_watch = context.user_data["box7500_watches"][user_clicks[username]]
        brand_quality = get_brand_quality(selected_watch)
        user_histories[username].append(selected_watch)
        user_clicks[username] += 1

        message = (
            f"📦 Box {user_clicks[username]} of 5\n"
            f"🧊 Sealed tight... let's see what’s inside!\n\n"
            f"{selected_watch}\n"
            f"Brand Quality: {brand_quality}"
        )

        if user_clicks[username] == 5:
            message += "\n\n⚠️ You've reached your 5 box limit.\n" \
                       f"🎉 Congratulations! You've selected your final watch:\n" \
                       f"✅ {selected_watch} \n" \
                       f"Brand Quality: {brand_quality}\n\n" \
                       "Please contact us to plan pickup or shipping.\n\n" \
                       "🎲 Hope to see you next month."

        await query.edit_message_text(message)

application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(handle_box_click))
application.run_polling()
'''

# Save to file for user to copy
file_path = Path("/mnt/data/mystery_box_bot_fixed.py")
file_path.write_text(code)
file_path
