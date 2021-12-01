from flask import Flask, request, jsonify
from firebase import firebase
import pyrebase
import Playtime
import SteamUser
from steamStore import SteamStore

firebaseConfig = {"apiKey": "AIzaSyB7UiA-ZyjEO-wO-9ofk9BzPId9wRe_ENs",
                  "authDomain": "csc-450-group-5-project.firebaseapp.com",
                  "databaseURL": "https://csc-450-group-5-project-default-rtdb.firebaseio.com",
                  "projectId": "csc-450-group-5-project",
                  "storageBucket": "csc-450-group-5-project.appspot.com",
                  "messagingSenderId": "248907054984",
                  "appId": "1:248907054984:web:3e56f6fefbb0ea8d67c43d",
                  "measurementId": "G-97CZL0FRJF"}
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()


# firebase = firebase.FirebaseApplication('https://csc-450-group-5-project-default-rtdb.firebaseio.com/',None)

class UserNotFoundException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def scrub_name(name: str):
    translation_table = dict.fromkeys(map(ord, '!@#$'), None)
    return name.translate(translation_table)


def get_user(userID: str):
    """
    This function returns a reference to the user object, good for checking for a user in the database
    :param userID: the unique ID number for the user in question. Should be an integer(?)
    :return: the dictionary with the user's data, raises exception if the path was not found
    """
    result = db.child("Users/" + userID).get()
    return result.val()


def create_user(userID: str, userEmail: str):
    """
    This function creates a new user with an ID and an email
    :param userID: string identification for the user - this is how they will be accessed by the application
    :param userEmail: string email address, will be associated with the user
    :return: True for success, False if a user with that ID already exists
    """
    if get_user(userID) is None:
        new_data = {"Email": userEmail, "Notification Time": 2}
        db.child('Users').child(userID).update(new_data)
        return True
    else:
        return False


def delete_user(userID: str):
    """
    This function deletes a user and all associated information from the database
    NOTE: this does not delete an email/password from firebase, just the user and steam accounts from our database
    :param userID: string identification for the user
    :return: True for success, False for failure
    """
    if get_user(userID) is not None:
        db.child("Users").child(userID).remove()
        return True
    else:
        return False


def get_email(userID: str):
    if get_user(userID) is not None:
        email = db.child("Users/" + userID).child("Email").get().val()
        return email
    else:
        return "Account not found"


def get_notif_time(userID: str):
    if get_user(userID) is not None:
        time = db.child("Users/" + userID).child("Notification Time").get().val()
        return time
    else:
        return "Account not found"


def update_notif_time(userID: str, often: int):
    if get_user(userID) is not None:
        if 0 < often < 5:
            db.child("Users/").child(userID).update({"Notification Time": often})
            print(db.child("Users/" + userID).child("Notification Time").get().val())
            return True
        else:
            return False
    else:
        return False


def add_steam_account(userID: str, steamID: int):
    """
    This function creates a new Steam account and associates it with a given user
    Initializes Auto Track, Limit Duration, Playtime Limit, Total Playtime, Playtimes, and Tracked Games fields
    :param userID: the user the steam account will be associated with
    :param steamID: an integer reference to the steam account
    :return: True for success, False for failure
    """
    if get_user(userID) is not None:
        steam_user = Playtime.Playtime(steamID, userID).get_game_info(new_user=True)
        display_name = steam_user.get_steam_name()
        game_dict = {}
        game_names = steam_user.get_game_names()
        playtimes = steam_user.get_playtimes()
        app_ids = steam_user.get_game_appids()
        img_icns = steam_user.get_game_icons()
        for i in range(len(game_names)):
            game_dict[scrub_name(game_names[i])] = {
                "Tracked": False,
                "Total Playtime": playtimes[i],
                "Weekly Playtime": -1,
                "Daily Playtime": -1,
                "App ID": app_ids[i],
                "Image Icon": img_icns[i]
            }
        new_data = {
            "Display Name": display_name,
            "On Report": True,
            "Auto Track": False,
            "Limit Duration": "week",
            "Playtime Limit": 0,
            "Exceeded": False,
            "Total Weekly Playtime": 0,
            "Total Daily Playtime": 0,
            "Watched Games": {
                "Temp": {
                    "ID": 0,
                    "Price": 0,
                    "Lower Than Threshold": False
                }
            },
            "Game Tracking": game_dict
        }
        db.child("Users/" + userID + "/Steam Accounts").child(steamID).update(new_data)
        return True
    else:
        return False


def get_steam_account(userID: str, steamID: int):
    """
    This function gets a reference to a steam account, fails if given user cannot be found
    :param userID: the associated user
    :param steamID: the target steam account ID
    :return: returns a reference to the steam account if it's found, None if it's not, and User not found if the user is not found
    """
    if get_user(userID) is not None:
        result = db.child("Users/" + userID + "/Steam Accounts").child(str(steamID)).get()
        return result
    else:
        return None


def delete_steam_account(userID: str, steamID: int):
    """
    This function removes a steam account from the database
    :param userID: the associated user
    :param steamID: the steam account to be removed
    :return: returns True for success, False for failure
    """
    if get_steam_account(userID, steamID) is not None:
        db.child("Users/" + userID + "/Steam Accounts").child(steamID).remove()
        return True
    else:
        return False


def set_limit_duration(userID: str, steamID: int, time: str):
    """
    This function sets the time period over which playtime will be tracked in an instance (day, week, month)
    :param userID: the associated user
    :param steamID: the steam account
    :param time: a string denoting either day, week, or month
    :return: True for success, False for failure
    """
    if get_steam_account(userID, steamID) is not None:
        db.child("Users/" + userID + "/Steam Accounts").child(steamID).update({"Limit Duration": time})
        return True
    else:
        return False


def toggle_on_report(userID: str, steamID: int, tog: bool):
    if get_steam_account(userID, steamID) is not None:
        db.child("Users/" + userID + "/Steam Accounts/").child(steamID).update({"On Report": tog})
        print(db.child("Users/" + userID + "/Steam Accounts/" + str(steamID)).child("On Report").get().val())
        return True
    else:
        return False


def toggle_exceeded(userID: str, steamID: int, tog: bool):
    if get_steam_account(userID, steamID) is not None:
        db.child("Users/" + userID + "/Steam Accounts/").child(steamID).update({"On Report": tog})
        print(db.child("Users/" + userID + "/Steam Accounts/" + str(steamID)).child("On Report").get().val())
        return True
    else:
        return False


def toggle_auto_track(userID: str, steamID: int, tog: bool):
    """
    This function toggles whether games will be tracked automatically as they are installed
    :param userID: the associated user
    :param steamID: the steam account
    :return: True for success, False for failure
    """
    if get_steam_account(userID, steamID) is not None:
        db.child("Users/" + userID + "/Steam Accounts/").child(steamID).update({"Auto Track": tog})
        print(db.child("Users/" + userID + "/Steam Accounts/" + str(steamID)).child("Auto Track").get().val())
        return True
    else:
        return False


def get_limit_duration(userID: str, steamID: int):
    """
    This function returns the time period being tracked
    :param userID: the associated user
    :param steamID: the steam account
    :return: the time period being tracked if success, Account not found for failure
    """
    if get_steam_account(userID, steamID) is not None:
        result = db.child("Users/" + userID + "/Steam Accounts/" + str(steamID)).child("Limit Duration").get().val()
        return result
    else:
        return "Account not found"


def set_playtime_limit(userID: str, steamID: int, limit: int):
    """
    This function sets how long a user can play in a given time period
    :param userID: the associated user
    :param steamID: the steam account
    :param limit: the time limit
    :return: True for success, False for failure
    """
    if get_steam_account(userID, steamID) is not None:
        db.child("Users/" + userID + "/Steam Accounts/").child(steamID).update({"Playtime Limit": limit})
        return True
    else:
        return False


def get_playtime_limit(userID: str, steamID: int):
    """
    This function returns the time limit
    :param userID: the associated user
    :param steamID: the steam account
    :return: the time limit for success, Account not found for failure
    """
    if get_steam_account(userID, steamID) is not None:
        result = db.child("Users/" + userID + "/Steam Accounts/" + str(steamID)).child("Playtime Limit").get().val()
        return result
    else:
        return "Account not found"


def get_auto_track(user_email: str, steam_id: int):
    """
    This function returns the user's auto track status.
    :param user_email: The associated user.
    :param steam_id: The associated Steam account.
    :return: True if the user is automatically tracking games, False otherwise.
    """
    if get_steam_account(user_email, steam_id) is not None:
        result = db.child("Users/" + user_email + "/Steam Accounts/" + str(steam_id)).child("Auto Track").get().val()
        return result
    else:
        return "Account not found"


def game_exists(game_name: str, user_email: str, steam_id: int):
    """
    This function checks if a game exists in the user's directory of games.
    :param game_name: The game to be checked.
    :param user_email: The associated user.
    :param steam_id: The steam ID associated with the user.
    :return: True if the game is present, False if it is not.
    """
    game_name = scrub_name(game_name)
    if get_steam_account(user_email, steam_id) is not None:
        found = False
        if db.child("Users/" + user_email + "/Steam Accounts/" + str(steam_id) + "/Game Tracking").child(
                game_name).get().val() is not None:
            found = True
        return found
    else:
        raise UserNotFoundException


def add_game(game_name: str, user_email: str, steam_id: int, total_playtime=0):
    """
    This function adds a game to the user's directory of games.
    :param game_name: The game's name, as a string.
    :param user_email: The associated user's email.
    :param steam_id: The associated user's SteamID.
    :param total_playtime: The game's total playtime.
    :return: True for success, False otherwise.
    """
    game_name = scrub_name(game_name)
    if game_exists(game_name, user_email, steam_id):
        RuntimeWarning("System attempting to add a game that already exists.")
    else:
        new_game = {
            "Tracked": get_auto_track(user_email, steam_id),
            "Total Playtime": total_playtime,
            "Weekly Playtime": 0,
            "Daily Playtime": 0
        }
        db.child("Users/" + user_email + "/Steam Accounts/" + str(steam_id) + "/Game Tracking").update(new_game)


def game_tracked(game_name: str, user_email: str, steam_id: int):
    """
    This function checks if a game is currently being tracked
    :param game_name: The game to be checked.
    :param user_email: The associated user's email.
    :param steam_id: The steam ID.
    :return: True if the game is being tracked, False if it's not.
    """
    game_name = scrub_name(game_name)
    if get_steam_account(user_email, steam_id) is not None:
        return db.child(
            "Users/" + user_email + "/Steam Accounts/" + str(steam_id) + "/Game Tracking/" + game_name +
            "/Tracked").get().val()
    else:
        raise UserNotFoundException(
            "User: " + user_email + " with Steam ID:" + str(
                steam_id) + "was not found when attempting to check if " + game_name + "was tracked.")


def add_tracked_game(game_name: str, user_email: str, steam_id: int):
    """
    This function adds a game to be tracked.
    If the game has not been added to the directory, it is added.
    :param game_name: the game string to be added
    :param user_email: the associated user
    :param steam_id: the steam account
    :return: True for success, False if the game is already tracked
    """
    game_name = scrub_name(game_name)
    if not game_tracked(game_name, user_email, steam_id):
        db.child("Users/" + user_email + "/Steam Accounts/" + str(steam_id) +
                 "/Game Tracking").child(game_name).update({"Tracked": True,
                                                            "Weekly Playtime": 0,
                                                            "Daily Playtime": 0
                                                            })
        return True
    else:
        RuntimeWarning("System attempting to track an already tracked game.")
        return False


def remove_tracked_game(game_name: str, user_email: str, steam_id: int):
    """
    This function adds a game to be tracked.
    If the game has not been added to the directory, it is added.
    :param game_name: the game string to be added
    :param user_email: the associated user
    :param steam_id: the steam account
    :return: True for success, False if the game is already not tracked
    """
    game_name = scrub_name(game_name)
    if game_tracked(game_name, user_email, steam_id):
        db.child("Users/" + user_email + "/Steam Accounts/" + str(steam_id) +
                 "/Game Tracking").child(game_name).update({"Tracked": False,
                                                            "Weekly Playtime": -1,
                                                            "Daily Playtime": -1
                                                            })
        return True
    else:
        RuntimeWarning("System attempting to un-track an already untracked game.")
        return False


def update_watch_game(userID: str, steamID: int, gameID: str, price: float):
    """
    This function changes the price on a watched game
    :param userID: the associated user
    :param steamID: the steam account
    :param gameID: the game being watched
    :param price: the updated price
    :return: True for success, False for failure
    """
    if get_steam_account(userID, steamID) is not None:
        db.child("Users/" + userID + "/Steam Accounts/" + str(steamID)).child("Watched Games/" + gameID).update({"Price": price})
        return True
    else:
        return False


def update_watch_game_lower(userID: str, steamID: int, gameID: str, lower_than_threshold: bool):
    if get_steam_account(userID, steamID) is not None:
        db.child("Users/" + userID + "/Steam Accounts/" + str(steamID)).child("Watched Games/" + gameID).update({"Lower Than Threshold": lower_than_threshold})
        return True
    else:
        return False


def get_watch_game_price(userID: str, steamID: int, gameID: str):
    if get_steam_account(userID, steamID) is not None:
        price = db.child("Users/" + userID + "/Steam Accounts/" + str(steamID) + "/Watched Games").child(
            gameID + "/Price").get().val()
        return price
    else:
        return "Account not found"

def get_watch_game_ID(userID: str, steamID: int, gameID: str):
    if get_steam_account(userID, steamID) is not None:
        appID = db.child("Users/" + userID + "/Steam Accounts/" + str(steamID) + "/Watched Games").child(gameID + "/ID").get().val()
        return appID
    else:
        return "Account not found"


def get_watch_game_lower(userID: str, steamID: int, gameID: str):
    if get_steam_account(userID, steamID) is not None:
        lower_than_threshold = db.child("Users/" + userID + "/Steam Accounts/" + str(steamID) + "/Watched Games").child(gameID + "/Lower Than Threshold").get().val()
        return lower_than_threshold
    else:
        return False


def add_watch_game(userID: str, steamID: int, gameID: str, appID: str, price: float):
    """
    This function adds a game to be watched at a certain price
    :param userID: the associated user
    :param steamID: the steam account
    :param gameID: the game being watched
    :param price: the price being watched for
    :return: True for success, False for failure
    """
    if get_steam_account(userID, steamID) is not None:
        if check_for_watched(userID, steamID, gameID) is False:
            db.child("Users/" + userID + "/Steam Accounts/" + str(steamID) + "/Watched Games").update({gameID:{"ID": appID, "Price": price, "Lower Than Threshold": False}})
            return True
        else:
            return False
    else:
        return False


def remove_watch_game(userID: str, steamID: int, gameID: str):
    """
    This function removes a game from the watch list
    :param userID: the associated user
    :param steamID: the steam account
    :param gameID: the game being removed
    :return: True for success, False for failure
    """
    if get_steam_account(userID, steamID) is not None:
        if check_for_watched(userID, steamID, gameID):
            db.child("Users/" + userID + "/Steam Accounts/" + str(steamID) + "/Watched Games").child(gameID).remove()
            return True
        else:
            return False
    else:
        return False


def get_playtime(game_name: str, user_email: str, steam_id: int) -> int:
    """
    This function returns the playtime for an individual game
    :param user_email: the associated user
    :param steam_id: the steam account
    :param game_name: the game to be retrieved
    :return: The playtime if success.
    """
    game_name = scrub_name(game_name)
    if get_steam_account(user_email, steam_id) is not None:
        playtime = db.child("Users/" + user_email + "/Steam Accounts/" + str(
            steam_id) + "/Game Tracking/" + game_name).child("Total Playtime").get().val()
        return playtime
    else:
        raise UserNotFoundException("User: " + user_email + " with Steam ID:" + str(
            steam_id) + "was not found when attempting to get the total playtime of: " + game_name)


def get_weekly_playtime(game_name: str, user_email: str, steam_id: int) -> int:
    """
    This function returns the weekly playtime for an individual game
    :param user_email: the associated user
    :param steam_id: the steam account
    :param game_name: the game to be retrieved
    :return: The playtime if success.
    """
    game_name = scrub_name(game_name)
    if get_steam_account(user_email, steam_id) is not None:
        playtime = db.child("Users/" + user_email + "/Steam Accounts/" + str(
            steam_id) + "/Game Tracking/" + game_name).child("Weekly Playtime").get().val()
        return playtime
    else:
        raise UserNotFoundException("User: " + user_email + " with Steam ID:" + str(
            steam_id) + "was not found when attempting to get the weekly playtime of: " + game_name)


def get_daily_playtime(game_name: str, user_email: str, steam_id: int) -> int:
    """
    This function returns the daily playtime for an individual game
    :param user_email: the associated user
    This function returns the daily playtime for an individual game
    :param user_email: the associated user
    :param steam_id: the steam account
    :param game_name: the game to be retrieved
    :return: The playtime if success.
    """
    game_name = scrub_name(game_name)
    if get_steam_account(user_email, steam_id) is not None:
        playtime = db.child("Users/" + user_email + "/Steam Accounts/" + str(
            steam_id) + "/Game Tracking/" + game_name).child("Daily Playtime").get().val()
        return playtime
    else:
        raise UserNotFoundException("User: " + user_email + " with Steam ID:" + str(
            steam_id) + "was not found when attempting to get the daily playtime of: " + game_name)


def update_playtime(game_name: str, user_email: str, steam_id: int, new_time: int):
    """
    This function updates the playtime for an individual game
    :param user_email: the associated user
    :param steam_id: the steam account
    :param game_name: the game to be updated
    :param new_time: the new playtime
    :return: True for success, False for failure
    """
    game_name = scrub_name(game_name)
    if get_steam_account(user_email, steam_id) is not None:
        if game_tracked(game_name, user_email, steam_id):
            last_known_time = get_playtime(game_name, user_email, steam_id)
            elapsed_time = new_time - last_known_time
            new_weekly_playtime = get_weekly_playtime(game_name, user_email, steam_id) + elapsed_time
            new_daily_playtime = get_daily_playtime(game_name, user_email, steam_id) + elapsed_time
        else:
            new_weekly_playtime = -1
            new_daily_playtime = -1
        db.child("Users/" + user_email + "/Steam Accounts/" + str(steam_id) + "/Game Tracking/" +
                 game_name).update({"Total Playtime": new_time,
                                    "Weekly Playtime": new_weekly_playtime,
                                    "Daily Playtime": new_daily_playtime})
        # print(db.child("Users/"+user_email+"/Steam Accounts/"+__steam_id+"/Playtimes").child(game_name).get().val())
        return True
    else:
        raise UserNotFoundException("User: " + user_email + " with Steam ID:" + str(
            steam_id) + "was not found when attempting to update the playtime of: " + game_name)


def get_playtime_sums(user_email: str, steam_id: int):
    """
    This function returns the total playtimes for the user's steam account.
    :param user_email: User's email.
    :param steam_id: User's steam ID.
    :return: An array with total, weekly, and daily playtimes.
    """
    tracked_games = db.child("Users/" + user_email + "/Steam Accounts/" + str(steam_id) +
                             "/Game Tracking").order_by_child("Tracking").equal_to(True).get()
    total_playtime = 0
    weekly_playtime = 0
    daily_playtime = 0
    for game in tracked_games:
        total_playtime = total_playtime + game["Total Playtime"]
        weekly_playtime = weekly_playtime + game["Weekly Playtime"]
        daily_playtime = daily_playtime + game["Daily Playtime"]
    return total_playtime, weekly_playtime, daily_playtime


def retrieve_report_data(user_email: str):
    """
    This function grabs all the data necessary for a report, and returns it as a list of SteamUser objects.
    :param user_email: The desired user's email.
    :return: A list of SteamUser objects.
    """
    all_steam_accounts = list_of_steam_accounts(user_email)
    data = []
    for account in all_steam_accounts:
        steam_id = account
        steam_name = db.child("Users/" + user_email + "/Steam Accounts/" + str(steam_id) + "/Display Name").get().val()
        game_names = []
        app_ids = []
        img_icons = []
        total_playtime = []
        weekly_playtime = []
        daily_playtime = []
        games = db.child("Users/" + user_email + "/Steam Accounts/" + str(steam_id) + "/Game Tracking").get()
        for game in games:
            game_data = game.val()
            game_names.append(game.key())
            app_ids.append(game_data["App ID"])
            img_icons.append(game_data["Image Icon"])
            total_playtime.append(game_data["Total Playtime"])
            weekly_playtime.append(game_data["Weekly Playtime"])
            daily_playtime.append(game_data["Daily Playtime"])
        account_data = SteamUser.SteamUser(steam_id, steam_name, app_ids, game_names, img_icons,
                                           total_playtime, weekly_playtime, daily_playtime)
        data.append(account_data)
    return data


def clear_weekly_playtimes(user_email: str, steam_id: int):
    tracked_games = list_of_tracked_games(user_email, steam_id)
    for game in tracked_games:
        db.child("Users/" + user_email + "/Steam Accounts/" + str(steam_id) + "/Game Tracking/" +
                 game).update({"Weekly Playtime": 0})


def clear_daily_playtimes(user_email: str, steam_id: int):
    tracked_games = list_of_tracked_games(user_email, steam_id)
    for game in tracked_games:
        db.child("Users/" + user_email + "/Steam Accounts/" + str(steam_id) + "/Game Tracking/" +
                 game).update({"Daily Playtime": 0})

def list_of_steam_accounts(userID: str):
    """
    This function returns a list of steam accounts
    :param userID: the associated user
    :return: a list containing the steam account identifiers, stored as dictionary keys
    """
    accountList = []
    if get_user(userID) is not None:
        result = db.child("Users/" + userID + "/Steam Accounts").child().shallow().get().val()
        if result is not None:
            for key in result:
                accountList.append(key)
            print(accountList)
        return accountList
    else:
        return []


def list_of_watched_games(userID: str, steamID: int):
    """
    This function returns a list of price watched games
    :param userID: the associated user
    :param steamID: the steam account
    :return: a list containing the games being price watched, stored as dictionary keys
    """
    wgList = []
    if get_steam_account(userID, steamID) is not None:
        result = db.child("Users/" + userID + "/Steam Accounts/" + str(steamID) + "/Watched Games").child().get().val()
        for key in result.keys():
            # print("Key is" + key)
            if key != 'Temp':
                subList = []
                subList.append(key)
                price = get_watch_game_price(userID, steamID, key)
                sale = get_watch_game_lower(userID, steamID, key)
                subList.append(price)
                subList.append(sale)
                wgList.append(subList)
        return wgList
    else:
        return []


def list_of_sale_games(userID: str, steamID: int):
    #print("beans")
    sgList = []
    if list_of_watched_games(userID, steamID) is not []:
        for game in list_of_watched_games(userID, steamID):
            #print(game)
            if game[2] is True:
                subList = []
                subList.append(game[0])
                steam_store_game = SteamStore.get_app_details(get_watch_game_ID(userID, steamID, game[0]))
                steam_store_price = float(steam_store_game.get('price'))
                steam_store_price /= 100
                steam_store_price = steam_store_price.__round__(1)
                print(steam_store_price)
                subList.append(steam_store_price)
                sgList.append(subList)
        return sgList
    else:
        return []


def list_of_tracked_games(userID: str, steamID: int):
    """
    This function returns a list of currently tracked games
    :param userID: the associated user
    :param steamID: the steam account
    :return: a list containing the games being tracked, stored as dictionary keys
    """
    tgList = []
    if get_steam_account(userID, steamID) is not None:
        result = db.child("Users/" + userID + "/Steam Accounts/" + str(steamID) + "/Game Tracking").get()
        for game in result.each():
            if game.val()["Tracked"]:
                tgList.append(game.key())
        return tgList
    else:
        return []


def list_of_playtime_games(userID: str, steamID: int):
    """
    This function returns a list of global stored playtimes
    :param userID: the associated user
    :param steamID: the steam account
    :return: a list containing the playtimes for all games ever tracked, stored as dictionary keys
    """
    pList = []
    if get_steam_account(userID, steamID) is not None:
        result = db.child("Users/" + userID + "/Steam Accounts/" + str(steamID) + "/Game Tracking").child().shallow().get().val()
        for game in result:
            pList.append(game)
        return pList
    else:
        return []


def list_of_users():
    userList = []
    result = db.child("Users").child().get().val()
    for key in result.keys():
        #print(key)
        userList.append(key)
    return userList


def check_for_watched(userID: str, steamID: int, gameID: str):
    if get_steam_account(userID, steamID) is not None:
        found = False
        watched_games = list_of_watched_games(userID, steamID)
        for game in watched_games:
            print(game[0])
            if game[0] == gameID:
                print(gameID + " is being watched!")
                found = True
        if not found:
            print(gameID + " is not being watched")
        return found
    else:
        return False
