# this file will be used to send out notifications at set intervals
import Mail
import Subprocess
import Database
import SubprocessPlaytime


def scheduler_update_database():
    '''
    This is for keeping track of what games from the watch list should be included in email
    :return:
    '''
    userList = Database.list_of_users()
    if len(userList) > 0:
        for user in userList:
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

                SubprocessPlaytime.update_playtime(user)
            except:
                print('No steam accounts')
        return True
    else:
        return False


def scheduler_notification_day():
    print("Daily notification triggered")
    # Mail.send_email(user,Database.get_email(user),1)
    for user in Database.list_of_users():
        try:
            # every day
            if Database.get_notif_time(user) == 1:
                Mail.send_email('matthewjar2000@gmailcom', Database.get_email('matthewjar2000@gmailcom'), 1)
            steam_accounts = Database.list_of_steam_accounts(user)
            for steam_acc in steam_accounts:
                Database.clear_daily_playtimes(user, steam_acc)
                Mail.send_email(user, Database.get_email(user), 1)
        except:
            print("User does not receive daily notifications")


def scheduler_notification_week():
    for user in Database.list_of_users():
        try:
            # every week
            if Database.get_notif_time(user) == 2:
                Mail.send_email('matthewjar2000@gmailcom', Database.get_email('matthewjar2000@gmailcom'), 1)
            steam_accounts = Database.list_of_steam_accounts(user)
            for steam_acc in steam_accounts:
                Database.clear_weekly_playtimes(user, steam_acc)
                Mail.send_email(user, Database.get_email(user), 1)
        except:
            print("User does not receive weekly notifications")


def scheduler_notification_month():
    for user in Database.list_of_users():
        try:
            # every month
            if Database.get_notif_time(user) == 4:
                Mail.send_email(user, Database.get_email(user), 1)
        except:
            print("User does not receive monthly notifications")


def scheduler_notification_biweekly():
    for user in Database.list_of_users():
        try:
            # every 2 weeks
            if Database.get_notif_time(user) == 3:
                Mail.send_email(user, Database.get_email(user), 1)
        except:
            print("User does not receive biweekly notifications")