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



def getUser(userID: str):
    """
    This function returns a reference to the user object, good for checking for a user in the database
    :param userID: the unique ID number for the user in question. Should be an integer(?)
    :return: the dictionary with the user's data, raises exception if the path was not found
    """
    result = db.child("Users/"+userID).get()
    return result.val()


def createUser(userID: str, userEmail: str):
    """
    This function creates a new user with an ID and an email
    :param userID: string identification for the user - this is how they will be accessed by the application
    :param userEmail: string email address, will be associated with the user
    :return: True for success, False if a user with that ID already exists
    """
    if getUser(userID) is None:
        new_data = {"Email":userEmail}
        db.child('Users').child(userID).update(new_data)
        return True
    else:
        return False


def deleteUser(userID: str):
    """
    This function deletes a user and all associated information from the database
    NOTE: this does not delete an email/password from firebase, just the user and steam accounts from our database
    :param userID: string identification for the user
    :return: True for success, False for failure
    """
    if getUser(userID) is not None:
        db.child("Users").child(userID).remove()
        return True
    else:
        return False


def addSteamAccount(userID: str, steamID: int):
    '''
    This function creates a new Steam account and associates it with a given user
    Initializes Auto Track, Limit Duration, Playtime Limit, Total Playtime, Owned Games, Playtimes, and Tracked Games fields
    :param userID: the user the steam account will be associated with
    :param steamID: an integer reference to the steam account
    :return: True for success, False for failure
    '''
    if getUser(userID) is not None:
        new_data = {"Auto Track": False,"Limit Duration": "week", "Playtime Limit": 0.0, "Total Playtime": 0.0, "Owned Games": {"Temp": 0}, "Playtimes": {"Temp": 0}, "Tracked Games": {"Temp": 0}, "Watched Games": {"Temp": 0}}
        db.child("Users/"+userID+"/Steam Accounts").child(steamID).update(new_data)
        return True
    else:
        return False


def getSteamAccount(userID: str, steamID: int):
    '''
    This function gets a reference to a steam account, fails if given user cannot be found
    :param userID: the associated user
    :param steamID: the target steam account ID
    :return: returns a reference to the steam account if it's found, None if it's not, and User not found if the user is not found
    '''
    if getUser(userID) is not None:
        result = db.child("Users/"+userID+"/Steam Accounts").child(str(steamID)).get()
        return result
    else:
        return None


def deleteSteamAccount(userID: str, steamID: int):
    '''
    This function removes a steam account from the database
    :param userID: the associated user
    :param steamID: the steam account to be removed
    :return: returns True for success, False for failure
    '''
    if getSteamAccount(userID, steamID) is not None:
        db.child("Users/"+userID+"/Steam Accounts").child(steamID).remove()
        return True
    else:
        return False


def setLimitDuration(userID: str, steamID: int, time: str):
    '''
    This function sets the time period over which playtime will be tracked in an instance (day, week, month)
    :param userID: the associated user
    :param steamID: the steam account
    :param time: a string denoting either day, week, or month
    :return: True for success, False for failure
    '''
    if getSteamAccount(userID, steamID) is not None:
        db.child("Users/"+userID+"/Steam Accounts").child(steamID).update({"Limit Duration": time})
        return True
    else:
        return False


def toggleAutoTrack(userID: str, steamID: int):
    '''
    This function toggles whether games will be tracked automatically as they are installed
    :param userID: the associated user
    :param steamID: the steam account
    :return: True for success, False for failure
    '''
    if getSteamAccount(userID, steamID) is not None:
        toggle = db.child("Users/"+userID+"/Steam Accounts/"+str(steamID)).child("Auto Track").get().val()
        if toggle is False:
            toggle = True
        else:
            toggle = False
        db.child("Users/"+userID+"/Steam Accounts/").child(steamID).update({"Auto Track": toggle})
        print(toggle)
        return True
    else:
        return False


def getLimitDuration(userID: str, steamID: int):
    '''
    This function returns the time period being tracked
    :param userID: the associated user
    :param steamID: the steam account
    :return: the time period being tracked if success, Account not found for failure
    '''
    if getSteamAccount(userID, steamID) is not None:
        result = db.child("Users/"+userID+"/Steam Accounts/"+str(steamID)).child("Limit Duration").get().val()
        return result
    else:
        return "Account not found"


def setPlaytimeLimit(userID: str, steamID: int, limit: float):
    '''
    This function sets how long a user can play in a given time period
    :param userID: the associated user
    :param steamID: the steam account
    :param limit: the time limit
    :return: True for success, False for failure
    '''
    if getSteamAccount(userID, steamID) is not None:
        db.child("Users/"+userID+"/Steam Accounts/").child(steamID).update({"Playtime Limit": limit})
        return True
    else:
        return False


def getPlaytimeLimit(userID: str, steamID: int):
    '''
    This function returns the time limit
    :param userID: the associated user
    :param steamID: the steam account
    :return: the time limit for success, Account not found for failure
    '''
    if getSteamAccount(userID, steamID) is not None:
        result = db.child("Users/"+userID+"/Steam Accounts/"+str(steamID)).child("Playtime Limit").get().val()
        return result
    else:
        return "Account not found"


def getTotalPlaytime(userID: str, steamID: int):
    '''
    This function returns the total amount of time played on record
    :param userID: the associated user
    :param steamID: the steam account
    :return: the total time if success, Account not found for failure
    '''
    if getSteamAccount(userID, steamID) is not None:
        result = db.child("Users/"+userID+"/Steam Accounts/"+str(steamID)).child("Total Playtime").get().val()
        return result
    else:
        return "Account not found"


def updateTotalPlaytime(userID: str, steamID: int, updatedTime: float):
    '''
    This function updates the total playtime
    NOTE: it is called by updatePlayTime. There is no need to call the function separately
    :param userID: the associated user
    :param steamID: the steam account
    :param updatedTime: time to be added to the total
    :return: returns total playtime if success, Account not found if failure
    '''
    if getSteamAccount(userID, steamID) is not None:
        result = getTotalPlaytime(userID, steamID)
        result = result+updatedTime
        db.child("Users/"+userID+"/Steam Accounts/"+str(steamID)).update({"Total Playtime": result})
        return getTotalPlaytime(userID, steamID)
    else:
        return "Account not found"


def addTrackedGame(gameID: str, userID: str, steamID: int):
    '''
    This function adds a game that is currently owned to be tracked
    :param gameID: the game string to be added
    :param userID: the associated user
    :param steamID: the steam account
    :return: True for success, False if the game is not owned
    '''
    if checkforOwned(userID, steamID, gameID):
        db.child("Users/"+userID+"/Steam Accounts/"+str(steamID)+"/Tracked Games").update({gameID: 0.0})
        return True
    else:
        print(gameID+" is not owned")
        return False


def removeTrackedGame(gameID: str, userID: str, steamID: int):
    '''
    This function removes a game that is currently owned from being tracked
    :param gameID: the game string to be removed
    :param userID: the associated user
    :param steamID: the steam account
    :return: True for success, False for failure
    '''
    if checkforTracked(userID, steamID, gameID):
        db.child("Users/"+userID+"/Steam Accounts/"+str(steamID)+"/Tracked Games").child(gameID).remove()
    # print(db.child("Users/"+userID+"/Steam Accounts"+steamID+"/Playtimes").child(gameID))
        return True
    else:
        return False


def updateWatchGame(userID: str, steamID: int, gameID: str, price: float):
    '''
    This function changes the price on a watched game
    :param userID: the associated user
    :param steamID: the steam account
    :param gameID: the game being watched
    :param price: the updated price
    :return: True for success, False for failure
    '''
    if getSteamAccount(userID, steamID) is not None:
        db.child("Users/"+userID+"/Steam Accounts/"+str(steamID)).child("Watched Games").update({gameID : price})
        return True
    else:
        return False


def addWatchGame(userID: str, steamID: int, gameID: str, price: float):
    '''
    This function adds a game to be watched at a certain price
    :param userID: the associated user
    :param steamID: the steam account
    :param gameID: the game being watched
    :param price: the price being watched for
    :return: True for success, False for failure
    '''
    if getSteamAccount(userID, steamID) is not None:
        if checkforWatched(userID, steamID, gameID) is None:
            db.child("Users/"+userID+"/Steam Accounts/"+str(steamID)+"/Watched Games").update({gameID: price})
            return True
        else:
            return False
    else:
        return False


def removeWatchGame(userID: str, steamID: int, gameID: str):
    '''
    This function removes a game from the watch list
    :param userID: the associated user
    :param steamID: the steam account
    :param gameID: the game being removed
    :return: True for success, False for failure
    '''
    if getSteamAccount(userID, steamID) is not None:
        if checkforWatched(userID, steamID, gameID):
            db.child("Users/"+userID+"/Steam Accounts/"+str(steamID)+"/Watched Games").child(gameID).remove()
            return True
        else:
            return False
    else:
        return False


def addOwnedGame(gameID: str, userID: str, steamID: int, auto: bool):
    '''
    This function adds a game to the list of owned games
    :param gameID: the game string to be added
    :param userID: the associated user
    :param steamID: the steam account
    :param auto: whether or not this game should be automatically tracked
    :return: True for success, False for failure
    '''
    if getSteamAccount(userID, steamID) is not None:
        db.child("Users/"+userID+"/Steam Accounts/"+str(steamID)+"/Owned Games").update({gameID: gameID})
        db.child("Users/"+userID+"/Steam Accounts/"+str(steamID)+"/Playtimes").update({gameID: 0.0})
        if auto:
            addTrackedGame(gameID, userID, steamID)
        return True
    else:
        return False


def removeOwnedGame(gameID: str, userID: str, steamID: int):
    '''
    This function removes a game from the list of owned games, and by default from the list of tracked games
    NOTE: this does not remove a game from the list of playtimes. This is so playtimes can be viewed for
    games that are no longer tracked or owned
    :param gameID: the game string to be removed
    :param userID: the associated user
    :param steamID: the steam account
    :return: True for success, False for failure
    '''
    if getSteamAccount(userID, steamID) is not None:
        removeTrackedGame(gameID, userID, steamID)
        db.child("Users/"+userID+"/Steam Accounts/"+str(steamID)+"/Owned Games").child(gameID).remove()
        return True
    else:
        return False


def getPlayTime(userID: str, steamID: int, gameID: str):
    '''
    This function returns the playtime for an individual game
    :param userID: the associated user
    :param steamID: the steam account
    :param gameID: the game string to be tracked
    :return: the playtime if success, None if failure
    '''
    if getSteamAccount(userID, steamID) is not None:
        playtime = db.child("Users/"+userID+"/Steam Accounts/"+str(steamID)+"/Playtimes").child(gameID).get().val()
        #print(playtime)
        return playtime
    else:
        return None


def updatePlayTime(userID: str, steamID: int, gameID: str, time: float):
    '''
    This function updates the playtime for an individual game
    :param userID: the associated user
    :param steamID: the steam account
    :param gameID: the game to be updated
    :param time: the amount of time in hours to be added
    :return: True for success, False for failure
    '''
    if getSteamAccount(userID, steamID) is not None:
        playtime = db.child("Users/"+userID+"/Steam Accounts/"+str(steamID)+"/Playtimes").child(gameID).get().val()
        updateTotalPlaytime(userID, steamID, time)
        #print(playtime)
        playtime = playtime+time
        db.child("Users/"+userID+"/Steam Accounts/"+str(steamID)+"/Playtimes").update({gameID: playtime})
        #print(db.child("Users/"+userID+"/Steam Accounts/"+steamID+"/Playtimes").child(gameID).get().val())
        return True
    else:
        return False


def checkforOwned(userID: str, steamID: int, gameID: str):
    '''
    This function checks if a game is listed as owned
    :param userID: the associated user
    :param steamID: the steam account
    :param gameID: the game being checked
    :return: True if the game is found, False if it is not or invalid parameters
    '''
    if getSteamAccount(userID, steamID) is not None:
        found = False
        games = db.child("Users/"+userID+"/Steam Accounts/"+str(steamID)).child("Owned Games").get()
        for game in games.each():
            #print(game.val())
            if game.val() == gameID:
                found = True
        return found
    else:
        return False


def checkforPlaytime(userID: str, steamID: int, gameID: str):
    '''
    This function checks if a game's playtime has ever been recorded
    :param userID: the associated user
    :param steamID: the steam account
    :param gameID: the game being checked
    :return: True if the game has playtime information, False if it doesn't
    '''
    if getSteamAccount(userID, steamID) is not None:
        found = False
        if(db.child("Users/"+userID+"/Steam Accounts/"+str(steamID)+"/Playtimes").child(gameID).get().val() != None):
            found = True
            print(gameID + " has Playtime information")
        else:
            print(gameID + " has no Playtime information")
        return found
    else:
        return False


def checkforWatched(userID: str, steamID: int, gameID: str):
    if getSteamAccount(userID, steamID) is not None:
        found = False
        if(db.child("Users/"+userID+"/Steam Accounts/"+str(steamID)+"/Watched Games").child(gameID).get().val() != None):
            found = True
            print(gameID + " is being watched!")
        else:
            print(gameID + " is not being watched")
        return found
    else:
        return False


def checkforTracked(userID: str, steamID: int, gameID: str):
    '''
    This function checks if a game is currently being tracked
    :param userID: the associated user
    :param steamID: the steam account
    :param gameID: the game being checked
    :return: True if the game is being tracked, False if it's not or invalid parameters
    '''
    if getSteamAccount(userID, steamID) is not None:
        found = False
        if(db.child("Users/"+userID+"/Steam Accounts/"+str(steamID)+"/Tracked Games").child(gameID).get().val() != None):
            found = True
            print(gameID + " is being tracked!")
        else:
            print(gameID + " is not being tracked")
        return found
    else:
        return False
