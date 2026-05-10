import requests

API_TOKEN = "ML7GtK2ECdFYVrkEXtkFqwtXz7rSrfCCzhjpgVlyEjPOrk16SYAc52azjaSu"

url = f"https://api.sportmonks.com/v3/football/fixtures/date/2026-05-10?api_token={API_TOKEN}&include=participants"

response = requests.get(url)

print("STATUS:", response.status_code)

data = response.json()

matches = data["data"]

print("\nTODAY MATCHES:\n")

for match in matches:

    participants = match["participants"]

    if len(participants) < 2:
        continue

    home_team = participants[0]["name"]
    away_team = participants[1]["name"]

    match_id = match["id"]

    print(f"{match_id} | {home_team} vs {away_team}")