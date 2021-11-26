import pyrebase
import Database


def test(username="test@gmailcom", steamName=76561198079743061):
    # delete the old test user
    Database.delete_user(username)
    # creat the new test user
    Database.create_user(username, "test@gmail.com")
    # get the user
    print(Database.get_user(username))
    print(Database.get_email(username))
    # add steam accounts to the new user
    Database.add_steam_account(username, steamName)
    # get reference to a steam account from the account ID
    print(Database.get_steam_account(username, steamName))
    # remove a steam account
    Database.delete_steam_account(username, 1)
    # get a list of steam accounts
    print(Database.list_of_steam_accounts(username))
    # toggle auto tracking
    Database.toggle_auto_track(username, steamName, False)
    Database.toggle_auto_track(username, steamName, True)
    # toggle shown on Report
    Database.toggle_on_report(username, steamName, True)

    # add a game to be tracked
    Database.add_tracked_game("GTA V", username, steamName)
    Database.add_tracked_game("Portal 2", username, steamName)
    Database.add_tracked_game("Minecraft", username, steamName)
    Database.add_tracked_game("Halo", username, steamName)
    # remove a game from being tracked
    Database.remove_tracked_game("GTA V", username, steamName)
    # set how long a period of time you want to impose a limit over (week, month, day)
    Database.set_limit_duration(username, steamName, "month")
    # print how long a period of time you want to impose a limit over
    print(Database.get_limit_duration(username, steamName))
    # set how long you want to be allowed to play within a given time
    Database.set_playtime_limit(username, steamName, 100)
    # print how long you want to be allowed to play within a given time
    print(Database.get_playtime_limit(username, steamName))
    # check if a game is being tracked
    print(Database.game_tracked("Portal 2", username, steamName))
    print(Database.game_tracked("GTA V", username, steamName))
    # update the play time on a game that's tracked, automatically updating the total time
    Database.update_playtime("Portal 2", username, steamName, 120)
    # remove a game from being tracked
    Database.remove_tracked_game("Portal 2", username, steamName)
    # add a game to be tracked
    Database.add_tracked_game("Portal 2", username, steamName)
    print(Database.update_playtime("Portal 2", username, steamName, 180))
    Database.get_daily_playtime("Portal 2", username, steamName)
    # start watching a game
    Database.add_watch_game(username, steamName, "Cyberpunk 2077", 30.00)
    Database.add_watch_game(username, steamName, "Metroid Dread", 30.00)
    # remove game from watch list
    Database.remove_watch_game(username, steamName, "Metroid Dread")
    Database.update_watch_game(username, steamName, "Cyberpunk 2077", 40.00)
    # print list of watched games
    print("Watched games:", Database.list_of_watched_games(username, steamName))
    # print list of tracked games
    print(Database.list_of_tracked_games(username, steamName))
    # print list of playtimes
    print(Database.list_of_playtime_games(username, steamName))
    return username
