import requests
import asyncio
import time
from telegram import Bot

from database import save_prediction

from momentum_engine import (
    update_momentum,
    calculate_momentum
)

from minute_engine import (
    get_minute_multiplier
)

from ranking_engine import (
    add_ranking,
    get_top_rankings,
    clear_rankings
)

from team_dna import (
    get_team_bonus
)

BOT_TOKEN = "8745289261:AAE_YFIAY13QomJtQ0rBqXRbNc1pXCmsrgQ"
CHAT_ID = "960585833"

SPORTMONKS_TOKEN = "ML7GtK2ECdFYVrkEXtkFqwtXz7rSrfCCzhjpgVlyEjPOrk16SYAc52azjaSu"

bot = Bot(token=BOT_TOKEN)

# Spam filter
sent_alerts = {}

# 15 dəqiqə cooldown
COOLDOWN = 900


async def scan_live_matches():

    print("🧠 SPECIAL GOAL AI STARTED...")

    while True:

        try:

            clear_rankings()

            url = f"https://api.sportmonks.com/v3/football/livescores?api_token={SPORTMONKS_TOKEN}&include=participants;statistics"

            response = requests.get(url)
            data = response.json()

            matches = data.get("data", [])

            print(f"⚽ Live matches: {len(matches)}")

            for match in matches:

                match_id = match.get("id")

                participants = match.get("participants", [])

                if len(participants) < 2:
                    continue

                home = participants[0].get("name", "Home")
                away = participants[1].get("name", "Away")

                # =========================
                # TEAM DNA
                # =========================

                home_bonus = get_team_bonus(home)
                away_bonus = get_team_bonus(away)

                minute = match.get("time", {}).get("minute", 0)

                stats = match.get("statistics", [])

                corners = 0
                dangerous = 0
                possession = 50

                for stat in stats:

                    stat_type = str(stat.get("type_id"))

                    value = stat.get("data", {}).get("value", 0)

                    try:
                        value = int(value)
                    except:
                        value = 0

                    # Corners
                    if stat_type == "34":
                        corners += value

                    # Dangerous attacks
                    if stat_type == "84":
                        dangerous += value

                    # Possession
                    if stat_type == "45":
                        possession = value

                # =========================
                # MOMENTUM ENGINE
                # =========================

                update_momentum(
                    match_id,
                    0,
                    dangerous,
                    corners
                )

                momentum = calculate_momentum(match_id)

                # =========================
                # MINUTE ENGINE
                # =========================

                minute_boost = get_minute_multiplier(minute)

                # =========================
                # HEADER AI
                # =========================

                header_score = (
                    corners * 5 +
                    dangerous * 2 +
                    possession +
                    momentum +
                    minute_boost +
                    home_bonus["header_bonus"] +
                    away_bonus["header_bonus"]
                )

                # =========================
                # PENALTY AI
                # =========================

                penalty_score = (
                    dangerous * 3 +
                    possession * 2 +
                    momentum +
                    minute_boost +
                    home_bonus["penalty_bonus"] +
                    away_bonus["penalty_bonus"]
                )

                # =========================
                # RANKING ENGINE
                # =========================

                total_risk = max(
                    header_score,
                    penalty_score
                )

                add_ranking(
                    home,
                    away,
                    total_risk
                )

                # =========================
                # HEADER ALERT
                # =========================

                if header_score > 120:

                    alert_key = f"header_{match_id}"

                    last_sent = sent_alerts.get(alert_key, 0)

                    if time.time() - last_sent > COOLDOWN:

                        percent = min(header_score // 2, 95)

                        confidence = min(
                            int(
                                (corners * 4) +
                                (dangerous * 2) +
                                (possession * 1.2) +
                                momentum +
                                minute_boost +
                                home_bonus["header_bonus"] +
                                away_bonus["header_bonus"]
                            ) // 3,
                            100
                        )

                        text = f"""
🧠 BAŞ ZƏRBƏSİ TƏHLÜKƏSİ

🏟 {home} vs {away}

⏱ Dəqiqə:
{minute}

📈 Ehtimal:
{percent}%

🎯 Confidence:
{confidence}%

🌊 Momentum:
{momentum}

🔥 Təzyiq Boost:
{minute_boost}

🧬 Team DNA:
+{home_bonus["header_bonus"] + away_bonus["header_bonus"]}

📊 Səbəb:
• yüksək künc sayı
• hava pressinqi
• dangerous attacks artımı
• late game pressure
"""

                        await bot.send_message(
                            chat_id=CHAT_ID,
                            text=text
                        )

                        sent_alerts[alert_key] = time.time()

                        save_prediction(
                            match_id,
                            home,
                            away,
                            "HEADER",
                            percent,
                            confidence
                        )

                        print(f"🧠 HEADER ALERT SENT: {home}")

                # =========================
                # PENALTY ALERT
                # =========================

                if penalty_score > 180:

                    alert_key = f"penalty_{match_id}"

                    last_sent = sent_alerts.get(alert_key, 0)

                    if time.time() - last_sent > COOLDOWN:

                        percent = min(penalty_score // 3, 90)

                        confidence = min(
                            int(
                                (dangerous * 3) +
                                (possession * 2) +
                                momentum +
                                minute_boost +
                                home_bonus["penalty_bonus"] +
                                away_bonus["penalty_bonus"]
                            ) // 4,
                            100
                        )

                        text = f"""
✋ PENALTI TƏHLÜKƏSİ

🏟 {home} vs {away}

⏱ Dəqiqə:
{minute}

📈 Ehtimal:
{percent}%

🎯 Confidence:
{confidence}%

🌊 Momentum:
{momentum}

🔥 Təzyiq Boost:
{minute_boost}

🧬 Team DNA:
+{home_bonus["penalty_bonus"] + away_bonus["penalty_bonus"]}

📊 Səbəb:
• yüksək dangerous attacks
• cərimə meydançası pressinqi
• possession dominance
• late game pressure
"""

                        await bot.send_message(
                            chat_id=CHAT_ID,
                            text=text
                        )

                        sent_alerts[alert_key] = time.time()

                        save_prediction(
                            match_id,
                            home,
                            away,
                            "PENALTY",
                            percent,
                            confidence
                        )

                        print(f"✋ PENALTY ALERT SENT: {home}")

            # =========================
            # TOP LIVE RISKS
            # =========================

            top_games = get_top_rankings()

            ranking_text = "\n🔥 TOP LIVE RISKS\n\n"

            position = 1

            for game in top_games:

                ranking_text += (
                    f"{position}. "
                    f"{game['home']} vs "
                    f"{game['away']} → "
                    f"{game['risk']}%\n"
                )

                position += 1

            print(ranking_text)

            await asyncio.sleep(60)

        except Exception as e:

            print("ERROR:", e)

            await asyncio.sleep(30)


asyncio.run(scan_live_matches())