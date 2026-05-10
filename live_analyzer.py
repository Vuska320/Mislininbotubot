import requests
import time
import asyncio
from telegram import Bot

# TOKENS
SPORTMONKS_TOKEN = "ML7GtK2ECdFYVrkEXtkFqwtXz7rSrfCCzhjpgVlyEjPOrk16SYAc52azjaSu"
TELEGRAM_TOKEN = "8745289261:AAE_YFIAY13QomJtQ0rBqXRbNc1pXCmsrgQ"
CHAT_ID = "960585833"

bot = Bot(token=TELEGRAM_TOKEN)

MATCH_ID = input("MATCH ID daxil et: ")

last_message = ""

print("⚽ ULTRA AI GOAL ENGINE STARTED...")

async def scan_match():

    global last_message

    while True:

        try:

            print("\nChecking live match...")

            url = f"https://api.sportmonks.com/v3/football/fixtures/{MATCH_ID}?api_token={SPORTMONKS_TOKEN}&include=participants;statistics"

            response = requests.get(url)

            print("STATUS:", response.status_code)

            data = response.json()

            if "data" not in data:
                print("No data.")
                time.sleep(15)
                continue

            match = data["data"]

            participants = match.get("participants", [])
            statistics = match.get("statistics", [])

            home = "Home"
            away = "Away"

            for team in participants:

                if team["meta"]["location"] == "home":
                    home = team["name"]

                if team["meta"]["location"] == "away":
                    away = team["name"]

            # HOME STATS
            home_shots = 0
            away_shots = 0

            home_danger = 0
            away_danger = 0

            home_poss = 50
            away_poss = 50

            home_goals = 0
            away_goals = 0

            home_red = 0
            away_red = 0

            # READ STATS
            for stat in statistics:

                type_id = stat["type_id"]
                value = stat["data"]["value"]
                location = stat["location"]

                # SHOTS ON TARGET
                if type_id == 86:

                    if location == "home":
                        home_shots = value

                    if location == "away":
                        away_shots = value

                # DANGEROUS ATTACKS
                if type_id == 108:

                    if location == "home":
                        home_danger = value

                    if location == "away":
                        away_danger = value

                # POSSESSION
                if type_id == 45:

                    if location == "home":
                        home_poss = value

                    if location == "away":
                        away_poss = value

                # GOALS
                if type_id == 52:

                    if location == "home":
                        home_goals = value

                    if location == "away":
                        away_goals = value

                # RED CARDS
                if type_id == 83:

                    if location == "home":
                        home_red = value

                    if location == "away":
                        away_red = value

            # TOTAL GOALS
            total_goals = home_goals + away_goals
            next_goal = total_goals + 1

            # AI PRESSURE ENGINE

            home_score = (
                (home_shots * 7) +
                (home_danger * 2) +
                (home_poss * 0.5)
            )

            away_score = (
                (away_shots * 7) +
                (away_danger * 2) +
                (away_poss * 0.5)
            )

            # RED CARD EFFECT
            if home_red > away_red:
                away_score += 15

            if away_red > home_red:
                home_score += 15

            # WHICH TEAM WILL SCORE
            if home_score > away_score:

                scoring_team = home
                dominant_score = home_score

            else:

                scoring_team = away
                dominant_score = away_score

            # AI CONFIDENCE
            confidence = int(abs(home_score - away_score))

            if confidence > 99:
                confidence = 99

            # xG STYLE SCORE
            xg = round(dominant_score / 25, 2)

            # GOAL TYPE AI

            normal_shot = 45 + int(dominant_score * 0.2)
            header = 10 + int(dominant_score * 0.05)
            penalty = 5 + int(dominant_score * 0.03)
            free_kick = 6 + int(dominant_score * 0.04)
            own_goal = 1

            no_goal = 30 - int(dominant_score * 0.1)

            # LIMITS

            normal_shot = min(normal_shot, 80)
            header = min(header, 30)
            penalty = min(penalty, 20)
            free_kick = min(free_kick, 18)

            if no_goal < 2:
                no_goal = 2

            # MOMENTUM
            if dominant_score >= 120:
                momentum = "EXTREME PRESSURE"

            elif dominant_score >= 80:
                momentum = "HIGH ATTACKING MOMENTUM"

            elif dominant_score >= 50:
                momentum = "ACTIVE ATTACK FLOW"

            else:
                momentum = "LOW TEMPO"

            # MESSAGE

            message = f"""
🏟 {home} vs {away}

━━━━━━━━━━━━━━

📊 LIVE AI ANALYSIS

🏠 {home}

🎯 Shots: {home_shots}
🔥 Dangerous: {home_danger}
📈 Possession: {home_poss}%
🟥 Red Cards: {home_red}

━━━━━━━━━━━━━━

🛫 {away}

🎯 Shots: {away_shots}
🔥 Dangerous: {away_danger}
📈 Possession: {away_poss}%
🟥 Red Cards: {away_red}

━━━━━━━━━━━━━━

⚽ NEXT GOAL PREDICTION

🔢 Next Goal:
{next_goal}

🥅 Likely Scoring Team:
{scoring_team}

📈 AI Confidence:
{confidence}%

⚡ Momentum:
{momentum}

🧠 Expected Goal Value (xG):
{xg}

━━━━━━━━━━━━━━

🎯 Goal Type Chances

👟 Normal Shot → {normal_shot}%
🧠 Header → {header}%
🎯 Free Kick → {free_kick}%
✋ Penalty → {penalty}%
😬 Own Goal → {own_goal}%
❌ No Goal → {no_goal}%
"""

            print(message)

            # SEND TELEGRAM
            if message != last_message:

                await bot.send_message(
                    chat_id=CHAT_ID,
                    text=message
                )

                print("✅ Telegrama göndərildi.")

                last_message = message

            else:
                print("No changes.")

        except Exception as e:
            print("ERROR:", e)

        time.sleep(20)

asyncio.run(scan_match())