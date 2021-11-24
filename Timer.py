# this file will be used to send out notifications at set intervals
import Mail
import Subprocess
import Database


def scheduler_update_database():
    '''
    This is for keeping track of what games from the watch list should be included in email
    :return:
    '''
    for user in Database.list_of_users():
        try:
            print("User is",user)
            steam_accounts = Database.list_of_steam_accounts(user)
            print("Steam account that matters is",steam_accounts[0])
            games = Subprocess.compare_with_steam_store(user)
            # update whether a game has cross the threshold
            for game in games:
                print("Bool is",games[game])
                print("Game is",game)
                Database.update_watch_game_lower(user, steam_accounts[0], game, games[game])
        except:
            print('No steam accounts')


def scheduler_notification_day():
    # for each user, check their notification frequency
    Mail.send_email('matthewjar2000@gmailcom', 'matthewjar2000@gmail.com', 1)
    # Mail.send_email(user,Database.get_email(user),1)
    # for user in Database.list_of_users():
    #     try:
    #         # every day
    #         if Database.get_notif_time(user) is 1:
    #             Mail.send_email(Database.get_email(user), 1)
    #         # every week
    #         # every two weeks
    #         # every month
    #     except:
    #         print("fuck")
    # if once a day
    #   some code
    # if once a week
    #   some code
    # if every 2 weeks
    #   some code
    # if once a month
    #   some code