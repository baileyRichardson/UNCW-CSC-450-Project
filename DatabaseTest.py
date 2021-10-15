import pyrebase
import Database


def test(username, steamName):
    # delete the old test user
    Database.delete_user(username)
    # creat the new test user
    Database.create_user(username, "test@gmail.com")
    # add steam accounts to the new user
    Database.add_steam_account(username, 1)
    Database.add_steam_account(username, steamName)
    # get reference to a steam account from the account ID
    print(Database.get_steam_account(username, steamName))
    # remove a steam account
    Database.delete_steam_account(username, 1)
    # toggle auto tracking
    Database.toggle_auto_track(username, steamName)
    Database.toggle_auto_track(username, steamName)
    # add games that are automatically added to the tracking
    Database.add_owned_game("GTA V", username, steamName, True)
    Database.add_owned_game("Portal 2", username, steamName, True)
    Database.add_owned_game("Minecraft", username, steamName, True)
    # add games that are not automatically added to the tracking
    Database.add_owned_game("Halo", username, steamName, False)
    Database.add_owned_game("Overwatch", username, steamName, False)
    # add a game to be tracked
    Database.add_tracked_game("Halo", username, steamName)
    # remove a game altogether
    Database.remove_owned_game("Minecraft", username, steamName)
    # remove a game from being tracked
    Database.remove_tracked_game("GTA V", username, steamName)
    # set how long a period of time you want to impose a limit over (week, month, day)
    Database.set_limit_duration(username, steamName, "month")
    # print how long a period of time you want to impose a limit over
    print(Database.get_limit_duration(username, steamName))
    # set how long you want to be allowed to play within a given time
    Database.set_playtime_limit(username, steamName, 10.2)
    # print how long you want to be allowed to play within a given time
    print(Database.get_playtime_limit(username, steamName))
    # check if a game is being tracked
    print(Database.check_for_tracked(username, steamName, "Portal 2"))
    print(Database.check_for_tracked(username, steamName, "GTA V"))
    # check if a game is owned
    Database.check_for_owned(username, steamName, "Portal 2")
    # update the play time on a game that's tracked, automatically updating the total time
    Database.update_playtime(username, steamName, "Portal 2", 2.4)
    # start watching a game
    Database.add_watch_game(username, steamName, "Cyberpunk 2077", 30.00)
    Database.add_watch_game(username, steamName, "Metroid Dread", 30.00)
    # remove game from watch list
    Database.remove_watch_game(username, steamName, "Metroid Dread")
    Database.update_watch_game(username, steamName, "Cyberpunk 2077", 40.00)
    # print the total playtime over all games
    print(Database.get_total_playtime(username, steamName))
    return username
