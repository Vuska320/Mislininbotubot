team_profiles = {

    "Arsenal": {
        "header_bonus": 20,
        "penalty_bonus": 5,
        "late_pressure": 15
    },

    "Real Madrid": {
        "header_bonus": 10,
        "penalty_bonus": 12,
        "late_pressure": 25
    },

    "Manchester City": {
        "header_bonus": 8,
        "penalty_bonus": 7,
        "late_pressure": 18
    },

    "Barcelona": {
        "header_bonus": 5,
        "penalty_bonus": 6,
        "late_pressure": 20
    },

    "Liverpool": {
        "header_bonus": 16,
        "penalty_bonus": 8,
        "late_pressure": 22
    }

}


def get_team_bonus(team_name):

    profile = team_profiles.get(team_name)

    if not profile:

        return {
            "header_bonus": 0,
            "penalty_bonus": 0,
            "late_pressure": 0
        }

    return profile