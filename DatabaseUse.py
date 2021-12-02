import Database
import steamStore

database = Database


def update_steam_account_page(userID: str, steamID: int, auto: str, remove: str, limit: str, often: str):
    if remove == "on":
        database.delete_steam_account(userID, steamID)
        return 1
    else:
        toggle = database.get_auto_track(userID, steamID)
        time = database.get_playtime_limit(userID, steamID)
        duration = database.get_limit_duration(userID, steamID)
        if auto == "on":
            toggle = True
        if auto == "off":
            toggle = False
        if limit != "":
            time = float(limit)
        if often == '1':
            duration = 'day'
        if often == '2':
            duration = 'week'
        database.toggle_auto_track(userID, steamID, toggle)
        database.set_playtime_limit(userID, steamID, time)
        database.set_limit_duration(userID, steamID, duration)
        return 2


def add_steam_account(userID: str, steamID: int):
    return database.add_steam_account(userID, steamID)


def update_notifications_page(userID: str, often: int):
    try:
        if 5 > often > 0:
            database.update_notif_time(userID, often)
            return True
        else:
            return False
    except:
        return False


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


def add_to_watch_list(userID: str, steamID: int, gameURL: str, price: float):
    try:
        gameID = gameURL.split('/')[4]
        if gameID != '5':
            game_name = steamStore.SteamStore.get_app_details(gameID).get("name")
            database.add_watch_game(userID, steamID, game_name, gameID, price)
            return game_name + " added"
        else:
            return ""
    except:
        return "Please enter valid URL"


def update_watch_list_page(userID: str, steamID: int, game: str, new_price: float, remove: str):
    # remove game
    if remove == 'on':
        database.remove_watch_game(userID, steamID, game)
        return game + " removed from watch list"
    # change price
    else:
        try:
            price = float(new_price)
            database.update_watch_game(userID, steamID, game, price)
            return "Price for " + game + " updated to " + str(price)
        except:
            print("No value given")
            return ""


def update_tracked_games_page(userID: str, steamID: int, game: str, remove: str):
    # remove game
    if remove == "on":
        database.remove_tracked_game(game, userID, steamID)
