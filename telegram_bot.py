import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# TOKENS
API_TOKEN = "ML7GtK2ECdFYVrkEXtkFqwtXz7rSrfCCzhjpgVlyEjPOrk16SYAc52azjaSu"
BOT_TOKEN = "8745289261:AAE_YFIAY13QomJtQ0rBqXRbNc1pXCmsrgQ"

# START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "⚽ AI Goal Predictor Ready\n\nUse:\n/scan MATCH_ID"
    )

# SCAN COMMAND
async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        # MATCH ID YOXDURSA
        if len(context.args) == 0:

            await update.message.reply_text(
                "Usage:\n/scan MATCH_ID"
            )

            return

        fixture_id = context.args[0]

        # API URL
        url = f"https://api.sportmonks.com/v3/football/fixtures/{fixture_id}?api_token={API_TOKEN}&include=participants;statistics"

        response = requests.get(url)

        print("STATUS:", response.status_code)

        data = response.json()

        match = data.get("data", {})

        participants = match.get("participants", [])

        if len(participants) < 2:

            await update.message.reply_text(
                "❌ Match not found."
            )

            return

        # TEAMS
        home = participants[0]["name"]
        away = participants[1]["name"]

        print(home, "vs", away)

        # STATS
        statistics = match.get("statistics", [])

        shots = 0
        dangerous = 0
        possession = 50

        print("\nLIVE STATS:\n")

        for stat in statistics:

            type_id = stat.get("type_id")

            value = stat.get("data", {}).get("value", 0)

            print("TYPE:", type_id, "VALUE:", value)

            # SHOTS ON TARGET
            if type_id in [41, 86]:
                shots += value

            # DANGEROUS ATTACKS
            elif type_id in [49, 50, 108]:
                dangerous += value

            # POSSESSION
            elif type_id == 45:
                possession = value

        # AI SCORE
        score = (shots * 15) + (dangerous * 2) + possession

        # PREDICTION
        prediction = "LOW GOAL CHANCE"

        if score >= 170:
            prediction = "🔥 EXTREME GOAL PRESSURE"

        elif score >= 130:
            prediction = "🚨 VERY HIGH CHANCE OF GOAL"

        elif score >= 95:
            prediction = "⚠ HIGH CHANCE OF GOAL"

        # MESSAGE
        message = f"""
⚽ LIVE MATCH SCAN

🏟 {home} vs {away}

📊 LIVE STATS

🎯 Shots On Target: {shots}
🔥 Dangerous Attacks: {dangerous}
📈 Possession: {possession}%

🧠 AI SCORE:
{score}

🚨 NEXT GOAL PREDICTION:
{prediction}
"""

        await update.message.reply_text(message)

    except Exception as e:

        print("ERROR:", e)

        await update.message.reply_text(
            f"❌ ERROR:\n{e}"
        )

# BOT APP
app = ApplicationBuilder().token(BOT_TOKEN).build()

# COMMANDS
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("scan", scan))

print("⚽ TELEGRAM AI SCANNER STARTED...")

# RUN
app.run_polling()