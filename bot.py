import os
import random
import logging
import zoneinfo
from datetime import datetime, timezone
from dotenv import load_dotenv
import requests

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ------------------------------
# CONTENT DATA
# ------------------------------
PROMOS = [
    "🎁 Promo A: Get 50% bonus on your next action this week!",
    "🔥 Promo B: Refer a friend and earn a mystery reward.",
    "⭐ Promo C: Weekend special — double points for all users!",
    "💎 Promo D: Daily check-in bonus available now.",
]

QUOTES = [
    "Believe you can and you're halfway there. – Theodore Roosevelt",
    "The future belongs to those who believe in their dreams. – Eleanor Roosevelt",
    "It always seems impossible until it's done. – Nelson Mandela",
    "Do something today that your future self will thank you for.",
    "Success is not final, failure is not fatal. – Winston Churchill",
]

JOKES = [
    "Why don't skeletons fight each other? They don't have the guts.",
    "I told my computer I needed a break. Now it won't stop sending me KitKat ads.",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "Parallel lines have so much in common. It's a shame they'll never meet.",
]

FACTS = [
    "Honey never spoils — 3000-year-old honey has been found edible.",
    "Octopuses have three hearts.",
    "Bananas are berries, but strawberries aren't.",
    "Sharks existed before trees.",
    "A day on Venus is longer than a year on Venus.",
]

SPORTS_FEED = [
    "🏆 Champions League: Real Madrid 2-1 Dortmund (FT)",
    "🏀 NBA: Lakers 112-105 Warriors (FT)",
    "🎾 Tennis: Djokovic advances to next round",
    "🏈 NFL: Chiefs win in overtime thriller",
    "⚽ Premier League: Arsenal 3-0 Chelsea (FT)",
]

USER_BONUS = {}  # user_id -> date string

# ------------------------------
# MAIN MENU
# ------------------------------
def main_menu():
    keyboard = [
        [
            InlineKeyboardButton("⚽ Sports", callback_data="sports"),
            InlineKeyboardButton("🌤️ Weather", callback_data="weather"),
        ],
        [
            InlineKeyboardButton("🕐 Time Zone", callback_data="time"),
            InlineKeyboardButton("🎁 Promos", callback_data="promo"),
        ],
        [
            InlineKeyboardButton("💰 Daily Bonus", callback_data="bonus"),
            InlineKeyboardButton("💬 Quote", callback_data="quote"),
        ],
        [
            InlineKeyboardButton("😂 Joke", callback_data="joke"),
            InlineKeyboardButton("🧠 Fact", callback_data="fact"),
        ],
        [
            InlineKeyboardButton("🆔 My ID", callback_data="myid"),
            InlineKeyboardButton("ℹ️ Help", callback_data="help"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


# ------------------------------
# HELPER: reply (works from command or button)
# ------------------------------
async def _reply(update: Update, text: str):
    if update.callback_query:
        await update.callback_query.message.reply_text(text, parse_mode="Markdown")
    else:
        await update.message.reply_text(text, parse_mode="Markdown")


# ------------------------------
# COMMANDS
# ------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "👋 *Welcome to SB24GZVIP_45bot!*\n\n"
        "I'm your all-in-one assistant:\n"
        "⚽ Sports updates\n"
        "🌤️ Weather check\n"
        "🕐 Time zone conversion\n"
        "🎁 Promos & Daily Bonus\n"
        "😄 Jokes, quotes & facts\n\n"
        "👇 Choose an option below or type /help"
    )
    await update.message.reply_text(
        text, parse_mode="Markdown", reply_markup=main_menu()
    )


async def menu_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📋 *Main Menu*", parse_mode="Markdown", reply_markup=main_menu())


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🧭 *Available Commands*\n\n"
        "/start – Start bot\n"
        "/menu – Show menu\n"
        "/sports – Live sports updates\n"
        "/weather <city> – Weather by city\n"
        "/time <from> <to> <HH:MM> – Convert time\n"
        "/promo – View promos\n"
        "/bonus – Claim daily bonus\n"
        "/quote – Random quote\n"
        "/joke – Random joke\n"
        "/fact – Random fact\n"
        "/calc <expr> – Simple calculator\n"
        "/id – Show your user ID\n"
        "/about – About bot"
    )
    await _reply(update, text)


async def about_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🤖 *SB24GZVIP_45bot*\n\n"
        "Your smart Telegram companion with sports updates, "
        "weather, time tools, promos and fun utilities.\n\n"
        "• Free to use\n"
        "• No spam\n"
        "• Contact: support@sb24gz.example\n"
        "• Built with ❤️"
    )
    await _reply(update, text)


# ------------------------------
# SPORTS
# ------------------------------
async def sports(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "⚽ *Sports Update*\n\n" + "\n".join(SPORTS_FEED) + "\n\n_Updates refreshed daily._"
    await _reply(update, msg)


# ------------------------------
# WEATHER
# ------------------------------
async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        city = " ".join(context.args)
    else:
        city = "London"
    try:
        r = requests.get(f"https://wttr.in/{city}?format=3", timeout=10)
        data = r.text.strip() or "No data available."
    except Exception:
        data = "⚠️ Could not fetch weather right now."

    text = f"🌤️ *Weather for {city.title()}*\n\n{data}"
    await _reply(update, text)


# ------------------------------
# TIME ZONE
# ------------------------------
async def time_zone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 3:
        text = (
            "🕐 *Time Zone Converter*\n\n"
            "Usage:\n"
            "`/time from to HH:MM`\n\n"
            "Example:\n"
            "`/time Africa/Lagos Europe/London 14:30`\n\n"
            "Common zones:\n"
            "Africa/Lagos, Europe/London, America/New_York,\n"
            "Asia/Tokyo, Asia/Dubai, Europe/Paris"
        )
        await _reply(update, text)
        return

    src, dst, hhmm = context.args[0], context.args[1], context.args[2]
    try:
        h, m = map(int, hhmm.split(":"))
        tz_src = zoneinfo.ZoneInfo(src)
        tz_dst = zoneinfo.ZoneInfo(dst)
        now = datetime.now(tz_src)
        dt = now.replace(hour=h, minute=m, second=0, microsecond=0)
        converted = dt.astimezone(tz_dst)
        text = (
            f"🕐 *Time Conversion*\n\n"
            f"`{dt.strftime('%Y-%m-%d %H:%M')}` ({src})\n"
            f"⬇️\n"
            f"`{converted.strftime('%Y-%m-%d %H:%M')}` ({dst})"
        )
    except Exception as e:
        text = f"⚠️ Error: {e}"
    await _reply(update, text)


# ------------------------------
# PROMO + BONUS
# ------------------------------
async def promo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "🎁 *Current Promos*\n\n" + "\n".join(PROMOS)
    text += "\n\nUse /bonus to claim your daily bonus!"
    await _reply(update, text)


async def bonus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    today = datetime.now(timezone.utc).date().isoformat()

    if USER_BONUS.get(user_id) == today:
        text = "⏳ You already claimed your bonus today!\nCome back tomorrow for more. 🎁"
    else:
        USER_BONUS[user_id] = today
        amount = random.randint(10, 100)
        text = (
            f"🎉 *Daily Bonus Claimed!*\n\n"
            f"You received *{amount} SB Points* today!\n"
            f"Come back tomorrow for more. 💎"
        )
    await _reply(update, text)


# ------------------------------
# QUOTE / JOKE / FACT
# ------------------------------
async def quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _reply(update, f"💬 *Quote of the moment*\n\n_{random.choice(QUOTES)}_")


async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _reply(update, f"😂 *Joke*\n\n{random.choice(JOKES)}")


async def fact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _reply(update, f"🧠 *Fun Fact*\n\n{random.choice(FACTS)}")


# ------------------------------
# CALCULATOR
# ------------------------------
async def calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await _reply(update, "Usage: `/calc 5+3*2`")
        return
    expr = " ".join(context.args)
    try:
        allowed = set("0123456789+-*/().% ")
        if not all(c in allowed for c in expr):
            raise ValueError("Invalid characters")
        result = eval(expr, {"__builtins__": {}}, {})
        await _reply(update, f"🧮 `{expr}` = *{result}*")
    except Exception:
        await _reply(update, "⚠️ Invalid expression.")


# ------------------------------
# USER ID
# ------------------------------
async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    text = (
        f"🆔 *Your Info*\n\n"
        f"Name: {u.first_name}\n"
        f"Username: @{u.username if u.username else 'none'}\n"
        f"User ID: `{u.id}`"
    )
    await _reply(update, text)


# ------------------------------
# BUTTON ROUTER
# ------------------------------
async def button_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    d = q.data

    if d == "sports":
        await sports(update, context)
    elif d == "weather":
        await weather(update, context)
    elif d == "time":
        await time_zone(update, context)
    elif d == "promo":
        await promo(update, context)
    elif d == "bonus":
        await bonus(update, context)
    elif d == "quote":
        await quote(update, context)
    elif d == "joke":
        await joke(update, context)
    elif d == "fact":
        await fact(update, context)
    elif d == "myid":
        await myid(update, context)
    elif d == "help":
        await help_cmd(update, context)


# ------------------------------
# MAIN
# ------------------------------
def main():
    if not BOT_TOKEN:
        raise SystemExit("❌ BOT_TOKEN missing. Set it as env var.")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu_cmd))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("about", about_cmd))
    app.add_handler(CommandHandler("sports", sports))
    app.add_handler(CommandHandler("weather", weather))
    app.add_handler(CommandHandler("time", time_zone))
    app.add_handler(CommandHandler("promo", promo))
    app.add_handler(CommandHandler("bonus", bonus))
    app.add_handler(CommandHandler("quote", quote))
    app.add_handler(CommandHandler("joke", joke))
    app.add_handler(CommandHandler("fact", fact))
    app.add_handler(CommandHandler("calc", calc))
    app.add_handler(CommandHandler("id", myid))
    app.add_handler(CallbackQueryHandler(button_router))

    logger.info("✅ Bot is running...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
