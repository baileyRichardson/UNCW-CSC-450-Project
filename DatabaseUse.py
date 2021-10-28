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




