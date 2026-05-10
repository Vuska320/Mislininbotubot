live_rankings = []


def add_ranking(
    home,
    away,
    risk
):

    global live_rankings

    live_rankings.append({
        "home": home,
        "away": away,
        "risk": risk
    })


def get_top_rankings():

    global live_rankings

    sorted_games = sorted(
        live_rankings,
        key=lambda x: x["risk"],
        reverse=True
    )

    return sorted_games[:5]


def clear_rankings():

    global live_rankings

    live_rankings = []