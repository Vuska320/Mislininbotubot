import requests
import time

# TELEGRAM BOT TOKEN
BOT_TOKEN = "8745289261:AAE_YFIAY13QomJtQ0rBqXRbNc1pXCmsrgQ"

# TELEGRAM CHAT ID
CHAT_ID = "960585833"

# SPORTMONKS API TOKEN
API_TOKEN = "ML7GtK2ECdFYVrkEXtkFqwtXz7rSrfCCzhjpgVlyEjPOrk16SYAc52azjaSu"

# Telegram API URL
telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# Store previous scores
previous_scores = {}

print("⚽ NEW GOALS Bot Started...")

# Send startup message
requests.post(telegram_url, data={
    "chat_id": CHAT_ID,
    "text": "✅ Goal Alert Bot is running..."
})

while True:

    print("Checking live matches...")

    url = (
        f"https://api.sportmonks.com/v3/football/livescores"
        f"?api_token={API_TOKEN}&include=participants;scores"
    )

    response = requests.get(url)

    print("STATUS:", response.status_code)

    data = response.json()

    if "data" in data:

        matches = data["data"]

        for match in matches:

            try:

                participants = match["participants"]

                home_team = participants[0]["name"]
                away_team = participants[1]["name"]

                scores = match["scores"]

                home_score = scores[0]["score"]["goals"]
                away_score = scores[1]["score"]["goals"]

                match_id = match["id"]

                current_score = f"{home_score}-{away_score}"

                # First time seeing match
                if match_id not in previous_scores:

                    previous_scores[match_id] = current_score
                    continue

                old_score = previous_scores[match_id]

                # ONLY send if score changed
                if current_score != old_score:

                    message = (
                        f"⚽ NEW GOAL!\n\n"
                        f"{home_team} {current_score} {away_team}"
                    )

                    requests.post(telegram_url, data={
                        "chat_id": CHAT_ID,
                        "text": message
                    })

                    print(message)

                    # Update stored score
                    previous_scores[match_id] = current_score

            except Exception as e:
                print("ERROR:", e)

    time.sleep(10)