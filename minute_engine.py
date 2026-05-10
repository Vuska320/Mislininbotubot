def get_minute_multiplier(minute):

    try:
        minute = int(minute)
    except:
        minute = 0

    # Early game
    if minute < 20:
        return 0

    # Normal pressure
    elif minute < 45:
        return 8

    # Second half pressure
    elif minute < 70:
        return 15

    # Late pressure
    elif minute < 80:
        return 25

    # Very late pressure
    elif minute < 90:
        return 40

    # Extra time chaos
    else:
        return 55