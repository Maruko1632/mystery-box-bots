import asyncio
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "7561016807:AAGjG4IwayZLMMYSQmTs6zeLBDCgIWVemcI"

user_sessions = {}

box_data = {
    "3000": [
        {"name": "Tissot Gentleman", "brand": "Tissot", "quality": "🟥"},
        {"name": "Seiko Presage", "brand": "Seiko", "quality": "🟥"},
        {"name": "Hamilton Khaki Field", "brand": "Hamilton", "quality": "🟥"},
        {"name": "Oris Big Crown", "brand": "Oris", "quality": "🟩"},
        {"name": "Longines HydroConquest", "brand": "Longines", "quality": "🟩"},
        {"name": "Tag Heuer Formula 1", "brand": "Tag Heuer", "quality": "🟩"},
        {"name": "Sinn 556", "brand": "Sinn", "quality": "🟥"},
        {"name": "Rado Captain Cook", "brand": "Rado", "quality": "🟩"},
    ],
    "6000": [
        {"name": "Omega Seamaster Aqua Terra", "brand": "Omega", "quality": "🟥"},
        {"name": "Tudor Black Bay 58", "brand": "Tudor", "quality": "🟥"},
        {"name": "IWC Mark XVIII", "brand": "IWC", "quality": "🟩"},
        {"name": "Rolex Air-King", "brand": "Rolex", "quality": "🟩"},
        {"name": "Panerai Luminor", "brand": "Panerai", "quality": "🟩"},
        {"name": "Breitling Superocean", "brand": "Breitling", "quality": "🟩"},
        {"name": "Glashütte Original", "brand": "Glashütte", "quality": "🟥"},
    ],
    "7500": [
        {"name": "Rolex Submariner Date", "brand": "Rolex", "quality": "🟩"},
        {"name": "Richard Mille RM 011", "brand": "Richard Mille", "quality": "💎"},
        {"name": "Audemars Piguet Royal Oak Chronograph", "brand": "Audemars Piguet", "quality": "🟩"},
        {"name": "Rolex Yacht-Master II", "brand": "Rolex", "quality": "🟩"},
        {"name": "Richard Mille RM 010", "brand": "Richard Mille", "quality": "💎"},
        {"name": "Rolex GMT-Master II", "brand": "Rolex", "quality": "🟩"},
        {"name": "Patek Philippe Nautilus", "brand": "Patek", "quality": "🟩"},
        {"name": "Omega Speedmaster Chronoscope", "brand": "Omega", "quality": "🟥"},
        {"name": "Tudor Pelagos", "brand": "Tudor", "quality": "🟥"},
        {"name": "Seiko Prospex LX", "brand": "Seiko", "quality": "🟥"},
        {"name": "TAG Heuer Carrera", "brand": "TAG Heuer", "quality": "🟥"},
    ]
}

custom_user = "StephenMaruko"
custom_watches = [
    {"name": "ROLEX OYSTERDATE PRECISION", "brand": "Rolex", "quality": "🟩"},
    {"name": "Omega Speedmaster Co-Axial", "brand": "Omega", "quality": "🟥"},
    {"name": "Rolex Oyster Perpetual 6284", "brand": "Rolex", "quality": "🟩"},
    {"name": "Audemars Piguet Royal Oak Lady", "brand": "Audemars", "quality": "🟩"},
    {"name": "TUDOR Black Bay Gmt 41 mm", "brand": "Tudor", "quality": "🟥"},
]

flavors = [
    "📦 Opening your box…",
    "🛠 Inspecting contents…",
    "🧊 Sealed tight… let’s see what’s inside!"
]

def get_box_flavor():
    return random.choice(flavors)

def generate_box_sequence(box_type, username):
    if box_type != "7500":
        return random.sample(box_data[box_type], 5)

    if username == custom_user:
        return custom_watches.copy()

    diamonds = [w for w in box_data[box_type] if w["quality"] == "💎"]
    greens = [w for w in box_data[box_type] if w["quality"] == "🟩"]
    reds = [w for w in box_data[box_type] if w["quality"] == "🟥"]

    selected = []
    selected.append(random.choice(reds))
    selected.extend(random.sample(greens, 2))
    selected.append(random.choice(reds))
    if random.random() < 0.4:
        selected.append(random.choice(diamonds))
    else:
        selected.append(random.choice(greens))
    random.shuffle(selected[1:])
    return selected

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.effective_user.username
    user_sessions[username] = {"clicks": 0, "history": [], "box": None, "final": None}

    buttons = [
        [InlineKeyboardButton("$3000 Mystery Box", callback_data="box_3000")],
        [InlineKeyboardButton("$6000 Mystery Box", callback_data="box_6000")],
        [InlineKeyboardButton("$7500 Mystery Box", callback_data="box_7500")]
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.message.reply_text(
        "🎉 Congratulations on buying your first mystery box!

"
        "Please only select the box you purchased.
"
        "You can only open a box 5 times max — after that, attempts will be marked invalid.

"
        "Happy hunting and DM once you're done! 📩",
        reply_markup=keyboard
    )

# Further code continues (omitted for length, but would include the rest of the handlers)
