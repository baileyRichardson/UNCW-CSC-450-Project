import pyrebase
import Database


def test(username, steamName):
    # delete the old test user
    Database.deleteUser(username)
    # creat the new test user
    Database.createUser(username, "test@gmail.com")
    # add steam accounts to the new user
    Database.addSteamAccount(username, 1)
    Database.addSteamAccount(username, steamName)
    # get reference to a steam account from the account ID
    print(Database.getSteamAccount(username, steamName))
    # remove a steam account
    Database.deleteSteamAccount(username, 1)
    # toggle auto tracking
    Database.toggleAutoTrack(username, steamName)
    Database.toggleAutoTrack(username, steamName)
    # add games that are automatically added to the tracking
    Database.addOwnedGame("GTA V", username, steamName, True)
    Database.addOwnedGame("Portal 2", username, steamName, True)
    Database.addOwnedGame("Minecraft", username, steamName, True)
    # add games that are not automatically added to the tracking
    Database.addOwnedGame("Halo", username, steamName, False)
    Database.addOwnedGame("Overwatch", username, steamName, False)
    # add a game to be tracked
    Database.addTrackedGame("Halo", username, steamName)
    # remove a game altogether
    Database.removeOwnedGame("Minecraft", username, steamName)
    # remove a game from being tracked
    Database.removeTrackedGame("GTA V", username, steamName)
    # set how long a period of time you want to impose a limit over (week, month, day)
    Database.setLimitDuration(username, steamName, "month")
    # print how long a period of time you want to impose a limit over
    print(Database.getLimitDuration(username, steamName))
    # set how long you want to be allowed to play within a given time
    Database.setPlaytimeLimit(username, steamName, 10.2)
    # print how long you want to be allowed to play within a given time
    print(Database.getPlaytimeLimit(username, steamName))
    # check if a game is being tracked
    print(Database.checkforTracked(username, steamName, "Portal 2"))
    print(Database.checkforTracked(username, steamName, "GTA V"))
    # check if a game is owned
    Database.checkforOwned(username, steamName, "Portal 2")
    # update the play time on a game that's tracked, automatically updating the total time
    Database.updatePlayTime(username, steamName, "Portal 2", 2.4)
    # print the total playtime over all games
    print(Database.getTotalPlaytime(username, steamName))
    return username
