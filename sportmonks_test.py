import requests

API_TOKEN = "ML7GtK2ECdFYVrkEXtkFqwtXz7rSrfCCzhjpgVlyEjPOrk16SYAc52azjaSu"

fixture_id = 19135006

url = f"https://api.sportmonks.com/v3/football/fixtures/{fixture_id}?api_token={API_TOKEN}&include=participants;statistics"

response = requests.get(url)

print("STATUS:", response.status_code)

data = response.json()

participants = data["data"]["participants"]

home_team = participants[1]["name"]
away_team = participants[0]["name"]

print("\nMATCH:")
print(home_team, "vs", away_team)

stats = data["data"]["statistics"]

home_stats = {}
away_stats = {}

STAT_TYPES = {
    45: "Possession",
    41: "Shots On Target",
    42: "Shots Off Target",
    34: "Corners",
    51: "Goals",
    58: "Yellow Cards",
    57: "Red Cards"
}

for stat in stats:
    stat_name = STAT_TYPES.get(stat["type_id"])

    if not stat_name:
        continue

    value = stat["data"]["value"]

    if stat["location"] == "home":
        home_stats[stat_name] = value
    else:
        away_stats[stat_name] = value

print("\nMATCH STATS:\n")

for key in STAT_TYPES.values():
    home = home_stats.get(key, 0)
    away = away_stats.get(key, 0)

    print(f"{key}: {home} - {away}")