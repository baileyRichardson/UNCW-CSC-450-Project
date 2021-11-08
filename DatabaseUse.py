import Database

database = Database


def update_steam_account_page(userID: str, steamID: int, auto: str, remove: str, limit: str):
    if remove == "on":
        database.delete_steam_account(userID, steamID)
        return 1
    else:
        toggle = database.get_auto_track(userID, steamID)
        time = database.get_playtime_limit(userID, steamID)
        if auto == "on":
            toggle = True
        if auto == "off":
            toggle = False
        if limit is not "":
            time = float(limit)
        database.toggle_auto_track(userID, steamID, toggle)
        database.set_playtime_limit(userID, steamID, time)
        return 2


def add_steam_account(userID: str, steamID: int):
    database.add_steam_account(userID, steamID)
    return 1


def update_notifications_page(userID: str, often: int):
    database.update_notif_time(userID, often)
    return 1


def interpret_notification_time(userID: str):
    often = database.get_notif_time(userID)
    if often == 1:
        return "Every day"
    elif often == 2:
        return "Once a week"
    elif often == 3:
        return "Every two weeks"
    elif often == 4:
        return "Once a month"
    else:
        return "Error - invalid time stored"

