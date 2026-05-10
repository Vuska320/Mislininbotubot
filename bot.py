import asyncio

try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

BOT_TOKEN = "8745289261:AAE_YFIAY13QomJtQ0rBqXRbNc1pXCmsrgQ"
SPORTMONKS_TOKEN = "ML7GtK2ECdFYVrkEXtkFqwtXz7rSrfCCzhjpgVlyEjPOrk16SYAc52azjaSu"

print("TELEGRAM AI BOT STARTED...")


menu = [
    ["/start", "/help"],
    ["/live", "/scan"]
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = ReplyKeyboardMarkup(menu, resize_keyboard=True)

    text = """
⚽ Misli AI Goal Bot Aktivdir

Komandalar:

/live → canlı oyunlar
/scan ID → oyun analiz et
/help → bütün komandalar
"""

    await update.message.reply_text(text, reply_markup=keyboard)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
📚 BOT KOMANDALARI

/start → botu başlat
/live → canlı oyunlar
/scan ID → oyunu analiz et

Nümunə:
/scan 19439592
"""

    await update.message.reply_text(text)


async def live(update: Update, context: ContextTypes.DEFAULT_TYPE):

    url = f"https://api.sportmonks.com/v3/football/livescores?api_token={SPORTMONKS_TOKEN}"

    response = requests.get(url)
    data = response.json()

    matches = data.get("data", [])

    if not matches:
        await update.message.reply_text("Hazırda canlı oyun yoxdur.")
        return

    text = "🔥 CANLI OYUNLAR\n\n"

    for match in matches[:20]:

        home = "Unknown"
        away = "Unknown"

        participants = match.get("participants", [])

        if len(participants) >= 2:
            home = participants[0].get("name", "Home")
            away = participants[1].get("name", "Away")

        match_id = match.get("id")

        text += f"{match_id}\n{home} vs {away}\n\n"

    await update.message.reply_text(text)


async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) == 0:
        await update.message.reply_text(
            "İstifadə:\n/scan MATCH_ID"
        )
        return

    match_id = context.args[0]

    url = f"https://api.sportmonks.com/v3/football/fixtures/{match_id}?api_token={SPORTMONKS_TOKEN}&include=participants;statistics"

    response = requests.get(url)
    data = response.json()

    fixture = data.get("data")

    if not fixture:
        await update.message.reply_text("Oyun tapılmadı.")
        return

    participants = fixture.get("participants", [])

    home = "Home"
    away = "Away"

    if len(participants) >= 2:
        home = participants[0].get("name", "Home")
        away = participants[1].get("name", "Away")

    stats = fixture.get("statistics", [])

    shots = 0
    dangerous = 0
    possession = 50

    for stat in stats:

        stat_type = str(stat.get("type_id"))

        value = stat.get("data", {}).get("value", 0)

        try:
            value = int(value)
        except:
            value = 0

        if stat_type == "86":
            shots += value

        if stat_type == "84":
            dangerous += value

        if stat_type == "45":
            possession = value

    goal_score = (
        shots * 5 +
        dangerous * 2 +
        possession
    )

    if goal_score > 120:
        next_goal = 3
        prediction_team = home

        zərbə = 72
        baş = 12
        cərimə = 7
        penalti = 5
        qol_yoxdur = 4

    elif goal_score > 80:
        next_goal = 2
        prediction_team = home

        zərbə = 64
        baş = 14
        cərimə = 9
        penalti = 8
        qol_yoxdur = 5

    else:
        next_goal = 1
        prediction_team = away

        zərbə = 49
        baş = 17
        cərimə = 12
        penalti = 10
        qol_yoxdur = 12

    text = f"""
⚽ NÖVBƏTİ QOL PROQNOZU

🆔 Oyun:
{match_id}

🏟 {home} vs {away}

🥅 Ehtimal Komanda:
{prediction_team}

🔢 Növbəti Qol:
{next_goal}

📊 EHTİMALLAR

👟 Zərbə → {zərbə}%
🧠 Baş zərbəsi → {baş}%
🎯 Cərimə zərbəsi → {cərimə}%
✋ Penalti → {penalti}%
❌ Qol olmayacaq → {qol_yoxdur}%
"""

    await update.message.reply_text(text)


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("live", live))
app.add_handler(CommandHandler("scan", scan))

print("Menu")

app.run_polling()