from modules.starter.starter import const


def get_day_or_night(now):
    if now.hour in range(8, 23) or now.hour == 0 or now.hour == 1:
        const["day_or_night"] = 'day'
    elif now.hour in range(2, 7):
        const["day_or_night"] = 'night'


def is_prof_time(now):
    if now.minute in range(1, 6) or now.minute in range(21, 26) or now.minute in range(41, 46):
        const["fish_timer"] = True
    else:
        const["fish_timer"] = False
