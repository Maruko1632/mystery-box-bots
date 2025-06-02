from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import random

user_clicks = {}
user_last_message = {}

watch_boxes = {
    'box_3000': [
        "Rolex Oyster Precision 6426",
        "Rolex Oysterdate Precision 6694",
        "Rolex Air-King 5500",
        "Rolex Oyster Perpetual 1002",
        "Rolex Date 1500"
    ],
    'box_6000': [
        "Rolex Submariner 16610",
        "Rolex Explorer 214270",
        "Rolex Datejust II 116300",
        "Rolex Milgauss 116400",
        "Rolex Oyster Perpetual 114300"
    ],
    'box_7500': [
        "Rolex Daytona 116500LN",
        "Richard Mille RM 010",
        "Audemars Piguet Royal Oak Offshore",
        "Rolex Yacht-Master II",
        "Richard Mille RM 055"
    ]
}

custom_user = "StephenMaruko"
custom_7500 = [
    "ROLEX OYSTERDATE PRECISION",
    "Omega Speedmaster Co-Axial",
    "Rolex Oyster Perpetual 6284",
    "Audemars Piguet Royal Oak Lady",
    "TUDOR Black Bay Gmt 41 mm"
]

brand_quality = {
    'rolex': '🟩',
    'audemars': '🟩',
    'richard': '💎',
    'patek': '🟩'
}

def get_brand_quality(watch_name):
    name_lower = watch_name.lower()
    for brand, emoji in brand_quality.items():
        if brand in name_lower:
            return f"{emoji}"
    return '🟥'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_clicks[user_id] = {'box_3000': 0, 'box_6000': 0, 'box_7500': 0}
    user_last_message[user_id] = None

    keyboard = [
        [InlineKeyboardButton("💵 $3000 Mystery Box", callback_data="box_3000")],
        [InlineKeyboardButton("💰 $6000 Mystery Box", callback_data="box_6000")],
        [InlineKeyboardButton("💎 $7500 Mystery Box", callback_data="box_7500")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome = (
        "🎉 Congratulations on buying your first mystery box!\n\n"
        "Please only select the box you purchased.\n"
        "You can only open a box *5 times max* — after that, attempts will be marked invalid.\n\n"
        "Happy hunting and DM once you're done! 📩"
    )
    await update.message.reply_text(welcome, reply_markup=reply_markup)

async def handle_box(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    username = user.username
    user_id = user.id
    box = query.data

    await query.answer()

    if box not in ['box_3000', 'box_6000', 'box_7500']:
        await query.edit_message_text("Invalid box selection.")
        return

    if user_clicks.get(user_id, {}).get(box, 0) >= 5:
        await query.edit_message_text("⚠️ You've reached your 5 box limit.")
        return

    if user_last_message.get(user_id):
        try:
            await context.bot.edit_message_reply_markup(
                chat_id=user_id,
                message_id=user_last_message[user_id],
                reply_markup=None
            )
        except:
            pass

    if box == 'box_7500' and username == custom_user:
        watch_list = custom_7500
    else:
        watch_list = watch_boxes[box]

    count = user_clicks[user_id][box]
    if box == 'box_7500' and (count + 1) % 5 == 0 and username != custom_user:
        watch = "Omega Mission to the Moon"
    else:
        watch = random.choice(watch_list)

    emoji = get_brand_quality(watch)
    user_clicks[user_id][box] += 1
    caption = f"🎁 Box Opened: {watch}\nBrand Quality: {emoji}"

    buttons = []
    if user_clicks[user_id][box] < 5:
        buttons = [
            [InlineKeyboardButton(f"Open another ${box[-4:]} box", callback_data=box)],
            [InlineKeyboardButton("✅ Select this watch", callback_data=f"select_{box}")]
        ]

    reply_markup = InlineKeyboardMarkup(buttons)
    sent_msg = await context.bot.send_message(chat_id=user_id, text=caption, reply_markup=reply_markup)
    user_last_message[user_id] = sent_msg.message_id

    if user_clicks[user_id][box] == 5:
        final_msg = (
            f"🎉 Congratulations! You've selected your final watch:\n\n"
            f"{watch}\nBrand Quality: {emoji}\n\n"
            f"Please contact us to plan pickup or shipping.\n\n"
            f"⚠️ You've reached your 5 box limit."
        )
        await context.bot.send_message(chat_id=user_id, text=final_msg)

async def select_watch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    try:
        await context.bot.edit_message_reply_markup(chat_id=user_id, message_id=query.message.message_id, reply_markup=None)
    except:
        pass

    await context.bot.send_message(
        chat_id=user_id,
        text="✅ Final watch selected! Contact us to arrange pickup or shipping.\n\n⚠️ You've reached your 5 box limit."
    )

def main():
    app = ApplicationBuilder().token("7561016807:AAGjG4IwayZLMMYSQmTs6zeLBDCgIWVemcI").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_box, pattern="^box_"))
    app.add_handler(CallbackQueryHandler(select_watch, pattern="^select_"))
    app.run_polling()

if __name__ == "__main__":
    main()
