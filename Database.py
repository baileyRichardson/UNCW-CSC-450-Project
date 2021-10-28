from flask import Flask, request, jsonify
from firebase import firebase
import pyrebase

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


def get_user(userID: str):
    """
    This function returns a reference to the user object, good for checking for a user in the database
    :param userID: the unique ID number for the user in question. Should be an integer(?)
    :return: the dictionary with the user's data, raises exception if the path was not found
    """
    result = db.child("Users/"+userID).get()
    return result.val()


def create_user(userID: str, userEmail: str):
    """
    This function creates a new user with an ID and an email
    :param userID: string identification for the user - this is how they will be accessed by the application
    :param userEmail: string email address, will be associated with the user
    :return: True for success, False if a user with that ID already exists
    """
    if get_user(userID) is None:
        new_data = {"Email": userEmail}
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
        email = db.child("Users/"+userID).child("Email").get().val()
        return email
    else:
        return None


def add_steam_account(userID: str, steamID: int):
    """
    This function creates a new Steam account and associates it with a given user
    Initializes Auto Track, Limit Duration, Playtime Limit, Total Playtime, Playtimes, and Tracked Games fields
    :param userID: the user the steam account will be associated with
    :param steamID: an integer reference to the steam account
    :return: True for success, False for failure
    """
    if get_user(userID) is not None:
        new_data = {"On Report": True,"Auto Track": False,"Limit Duration": "week", "Playtime Limit": 0.0, "Total Playtime": 0.0, "Playtimes": {"Temp": 0}, "Tracked Games": {"Temp": 0}, "Watched Games": {"Temp": 0}}
        db.child("Users/"+userID+"/Steam Accounts").child(steamID).update(new_data)
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
        result = db.child("Users/"+userID+"/Steam Accounts").child(str(steamID)).get()
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
        db.child("Users/"+userID+"/Steam Accounts").child(steamID).remove()
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
        db.child("Users/"+userID+"/Steam Accounts").child(steamID).update({"Limit Duration": time})
        return True
    else:
        return False


def toggle_on_report(userID: str, steamID: int, tog: bool):
    if get_steam_account(userID, steamID) is not None:
        db.child("Users/"+userID+"/Steam Accounts/").child(steamID).update({"On Report": tog})
        print(db.child("Users/"+userID+"/Steam Accounts/"+str(steamID)).child("On Report").get().val())
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
        db.child("Users/"+userID+"/Steam Accounts/").child(steamID).update({"Auto Track": tog})
        print(db.child("Users/"+userID+"/Steam Accounts/"+str(steamID)).child("Auto Track").get().val())
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
        result = db.child("Users/"+userID+"/Steam Accounts/"+str(steamID)).child("Limit Duration").get().val()
        return result
    else:
        return "Account not found"


def set_playtime_limit(userID: str, steamID: int, limit: float):
    """
    This function sets how long a user can play in a given time period
    :param userID: the associated user
    :param steamID: the steam account
    :param limit: the time limit
    :return: True for success, False for failure
    """
    if get_steam_account(userID, steamID) is not None:
        db.child("Users/"+userID+"/Steam Accounts/").child(steamID).update({"Playtime Limit": limit})
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
        result = db.child("Users/"+userID+"/Steam Accounts/"+str(steamID)).child("Playtime Limit").get().val()
        return result
    else:
        return "Account not found"


def get_total_playtime(userID: str, steamID: int):
    """
    This function returns the total amount of time played on record
    :param userID: the associated user
    :param steamID: the steam account
    :return: the total time if success, Account not found for failure
    """
    if get_steam_account(userID, steamID) is not None:
        result = db.child("Users/"+userID+"/Steam Accounts/"+str(steamID)).child("Total Playtime").get().val()
        return result
    else:
        return "Account not found"


def update_total_playtime(userID: str, steamID: int, updatedTime: float):
    """
    This function updates the total playtime
    NOTE: it is called by updatePlayTime. There is no need to call the function separately
    :param userID: the associated user
    :param steamID: the steam account
    :param updatedTime: time to be added to the total
    :return: returns total playtime if success, Account not found if failure
    """
    if get_steam_account(userID, steamID) is not None:
        result = get_total_playtime(userID, steamID)
        result = result+updatedTime
        db.child("Users/"+userID+"/Steam Accounts/"+str(steamID)).update({"Total Playtime": result})
        return get_total_playtime(userID, steamID)
    else:
        return "Account not found"


def add_tracked_game(gameID: str, userID: str, steamID: int):
    """
    This function adds a game to be tracked.
    If the game has not been tracked before, it adds it to a global list of playtimes
    :param gameID: the game string to be added
    :param userID: the associated user
    :param steamID: the steam account
    :return: True for success, False if the game is already tracked
    """
    if not check_for_tracked(userID, steamID, gameID):
        db.child("Users/"+userID+"/Steam Accounts/"+str(steamID)+"/Tracked Games").update({gameID: 0.0})
        # if existing global data doesn't exist
        if not check_for_playtime(userID, steamID, gameID):
            add_global_playtime(gameID, userID, steamID)
        return True
    else:
        print(gameID+" is already tracked")
        return False


def remove_tracked_game(gameID: str, userID: str, steamID: int):
    """
    This function removes a game from being tracked
    :param gameID: the game string to be removed
    :param userID: the associated user
    :param steamID: the steam account
    :return: True for success, False for failure
    """
    if check_for_tracked(userID, steamID, gameID):
        db.child("Users/"+userID+"/Steam Accounts/"+str(steamID)+"/Tracked Games").child(gameID).remove()
    # print(db.child("Users/"+userID+"/Steam Accounts"+steamID+"/Playtimes").child(gameID))
        return True
    else:
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
        db.child("Users/"+userID+"/Steam Accounts/"+str(steamID)).child("Watched Games").update({gameID : price})
        return True
    else:
        return False


def get_watch_game_price(userID: str, steamID: int, gameID: str):
    if get_steam_account(userID, steamID) is not None:
        price = db.child("Users/"+userID+"/Steam Accounts/"+str(steamID)+"/Watched Games").child(gameID).get().val()
        return price
    else:
        return None


def add_watch_game(userID: str, steamID: int, gameID: str, price: float):
    """
    This function adds a game to be watched at a certain price
    :param userID: the associated user
    :param steamID: the steam account
    :param gameID: the game being watched
    :param price: the price being watched for
    :return: True for success, False for failure
    """
    if get_steam_account(userID, steamID) is not None:
        if check_for_watched(userID, steamID, gameID) is None:
            db.child("Users/"+userID+"/Steam Accounts/"+str(steamID)+"/Watched Games").update({gameID: price})
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
            db.child("Users/"+userID+"/Steam Accounts/"+str(steamID)+"/Watched Games").child(gameID).remove()
            return True
        else:
            return False
    else:
        return False


def add_global_playtime(gameID: str, userID: str, steamID: int):
    """
    This function adds a game to the list of global game playtimes, even games currently not tracked
    :param gameID: the game string to be added
    :param userID: the associated user
    :param steamID: the steam account
    :param auto: whether or not this game should be automatically tracked
    :return: True for success, False for failure
    """
    if get_steam_account(userID, steamID) is not None:
        db.child("Users/"+userID+"/Steam Accounts/"+str(steamID)+"/Playtimes").update({gameID: 0.0})
        return True
    else:
        return False


def get_playtime(userID: str, steamID: int, gameID: str):
    """
    This function returns the playtime for an individual game
    :param userID: the associated user
    :param steamID: the steam account
    :param gameID: the game string to be tracked
    :return: the playtime if success, None if failure
    """
    if get_steam_account(userID, steamID) is not None:
        playtime = db.child("Users/"+userID+"/Steam Accounts/"+str(steamID)+"/Playtimes").child(gameID).get().val()
        #print(playtime)
        return playtime
    else:
        return None


def update_playtime(userID: str, steamID: int, gameID: str, time: float):
    """
    This function updates the playtime for an individual game
    :param userID: the associated user
    :param steamID: the steam account
    :param gameID: the game to be updated
    :param time: the amount of time in hours to be added
    :return: True for success, False for failure
    """
    if get_steam_account(userID, steamID) is not None:
        playtime = db.child("Users/"+userID+"/Steam Accounts/"+str(steamID)+"/Playtimes").child(gameID).get().val()
        update_total_playtime(userID, steamID, time)
        #print(playtime)
        playtime = playtime+time
        db.child("Users/"+userID+"/Steam Accounts/"+str(steamID)+"/Playtimes").update({gameID: playtime})
        #print(db.child("Users/"+userID+"/Steam Accounts/"+steamID+"/Playtimes").child(gameID).get().val())
        return True
    else:
        return False


def list_of_steam_accounts(userID: str):
    """
    This function returns a list of steam accounts
    :param userID: the associated user
    :return: a list containing the steam account identifiers, stored as dictionary keys
    """
    accountList = []
    if get_user(userID) is not None:
        result = db.child("Users/"+userID+"/Steam Accounts").child().get().val()
        for key in result.keys():
            accountList.append(key)
        print(accountList)
        return accountList
    else:
        return None


def list_of_watched_games(userID: str, steamID: int):
    """
    This function returns a list of price watched games
    :param userID: the associated user
    :param steamID: the steam account
    :return: a list containing the games being price watched, stored as dictionary keys
    """
    wgList = []
    if get_steam_account(userID, steamID) is not None:
        result = db.child("Users/"+userID+"/Steam Accounts/"+str(steamID)+"/Watched Games").child().get().val()
        for key in result.keys():
            subList = []
            subList.append(key)
            price = get_watch_game_price(userID, steamID, key)
            subList.append(price)
            wgList.append(subList)
        return wgList
    else:
        return None


def list_of_tracked_games(userID: str, steamID: int):
    """
    This function returns a list of currently tracked games
    :param userID: the associated user
    :param steamID: the steam account
    :return: a list containing the games being tracked, stored as dictionary keys
    """
    tgList = []
    if get_steam_account(userID, steamID) is not None:
        result = db.child("Users/"+userID+"/Steam Accounts/"+str(steamID)+"/Tracked Games").child().get().val()
        for key in result.keys():
            tgList.append(key)
        return tgList
    else:
        return None


def list_of_playtime_games(userID: str, steamID: int):
    """
    This function returns a list of global stored playtimes
    :param userID: the associated user
    :param steamID: the steam account
    :return: a list containing the playtimes for all games ever tracked, stored as dictionary keys
    """
    pList = []
    if get_steam_account(userID, steamID) is not None:
        result = db.child("Users/"+userID+"/Steam Accounts/"+str(steamID)+"/Playtimes").child().get().val()
        for key in result.keys():
            pList.append(key)
        return pList
    else:
        return None


def check_for_playtime(userID: str, steamID: int, gameID: str):
    """
    This function checks if a game's playtime has ever been recorded
    :param userID: the associated user
    :param steamID: the steam account
    :param gameID: the game being checked
    :return: True if the game has playtime information, False if it doesn't
    """
    if get_steam_account(userID, steamID) is not None:
        found = False
        if db.child("Users/"+userID+"/Steam Accounts/"+str(steamID)+"/Playtimes").child(gameID).get().val() is not None:
            found = True
            print(gameID + " has Playtime information")
        else:
            print(gameID + " has no Playtime information")
        return found
    else:
        return False


def check_for_watched(userID: str, steamID: int, gameID: str):
    if get_steam_account(userID, steamID) is not None:
        found = False
        if db.child("Users/"+userID+"/Steam Accounts/"+str(steamID)+"/Watched Games").child(gameID).get().val() is not None:
            found = True
            print(gameID + " is being watched!")
        else:
            print(gameID + " is not being watched")
        return found
    else:
        return False


def check_for_tracked(userID: str, steamID: int, gameID: str):
    """
    This function checks if a game is currently being tracked
    :param userID: the associated user
    :param steamID: the steam account
    :param gameID: the game being checked
    :return: True if the game is being tracked, False if it's not or invalid parameters
    """
    if get_steam_account(userID, steamID) is not None:
        found = False
        if db.child("Users/"+userID+"/Steam Accounts/"+str(steamID)+"/Tracked Games").child(gameID).get().val() is not None:
            found = True
            print(gameID + " is being tracked!")
        else:
            print(gameID + " is not being tracked")
        return found
    else:
        return False
