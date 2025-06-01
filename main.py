from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ChatMemberHandler, ContextTypes
import random

TOKEN = "7561016807:AAGjG4IwayZLMMYSQmTs6zeLBDCgIWVemcI"

# List of watches for $3000 box
watches_3000 = [
    "Rolex Oyster Precision 6426",
    "Rolex Oysterdate Precision 6694",
    "Rolex Air-King 5500",
    "Rolex Oyster Perpetual 1002",
    "Rolex Date 1500",
    "Rolex Oyster Perpetual 6564",
    "Rolex Oyster Perpetual 6430",
    "Rolex Oyster Date 6517",
    "Rolex Oyster Perpetual 6284",
    "Rolex Oyster Perpetual 6718 (Ladies)",
    "Rolex Oyster Precision 1210",
    "Rolex Oyster Perpetual Datejust 1601",
    "Rolex Oyster Royal",
    "Rolex Precision 9022",
    "Rolex Oyster Perpetual 6618",
    "Rolex Oyster Perpetual 67193",
    "Rolex Oyster Perpetual 76193 (Ladies)",
    "Rolex Oysterdate 6694 Linen Dial",
    "Rolex Oyster Perpetual 14233 (Ladies)"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💵 $3000 Mystery Box", callback_data="box_3000")],
        [InlineKeyboardButton("💰 $6000 Mystery Box", callback_data="box_6000")],
        [InlineKeyboardButton("💎 $7500 Mystery Box", callback_data="box_7500")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose your mystery box:", reply_markup=reply_markup)

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    box = query.data

    if box == "box_3000":
        selected_watch = random.choice(watches_3000)
        await context.bot.send_message(
            chat_id=query.message.chat.id,
            text=f"🎉 Congratulations! You received:\n**{selected_watch}**\n\nDM us for more information.",
            parse_mode="Markdown"
        )
    else:
        await query.edit_message_text("❌ Invalid box selected or not yet supported.")

async def welcome_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_members = update.chat_member.new_chat_members
    if new_members:
        for member in new_members:
            welcome_text = (
                f"🎉 Welcome to Nazur Mystery Boxes, {member.first_name}!\n\n"
                "Congrats on buying your first mystery box 📦\n"
                "➡️ Please only select the box you purchased.\n"
                "🔁 You can change your selection **10 times max** — after that, it's invalid.\n\n"
                "🧠 Good luck & happy hunting!\n"
                "DM us once you're done."
            )
            await context.bot.send_message(chat_id=update.chat_member.chat.id, text=welcome_text, parse_mode="Markdown")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_button))
    app.add_handler(ChatMemberHandler(welcome_user, chat_member_types=["member"]))
    app.run_polling()

if __name__ == "__main__":
    main()
