
import Database
from steamStore import SteamStore
from SteamUser import SteamUser
from Report import Report

def compare_with_steam_store(user_email : str):
    """
    Compares the watch price of games on a users watchlist to the Steam Store prices and returns a dictionary
    of games as keys and a boolean of True or False as value. True and False corresponds to whether or
    not the watch price equals the Steam Store price.
    :param user_email: User email as a string.
    :return: A dictionary with watched games as keys and a boolean of either True or False as the value.
    """
    accounts = Report(user_email)
    account_list = accounts.get_report(reports_page=True)
    watched_by_steam_account = []
    account: SteamUser
    watched_equals_store = {}
    for account in account_list:
        user_watched_games = Database.list_of_watched_games(user_email, account.get_steam_id())
        watched_by_steam_account.append(user_watched_games)
        # print("Watched games and price for ", account, ": ", user_watched_games)

        for game in user_watched_games:
            watch_game_price = Database.get_watch_game_price(user_email, account.get_steam_id(), game[0])
            # print(game[0], " watch price --> ", watch_game_price)
            watched_game_ids = Database.get_watch_game_ID(user_email, account.get_steam_id(), game[0])
            steam_store_game = SteamStore.get_app_details(watched_game_ids)
            steam_store_price = float(steam_store_game.get('price'))
            steam_store_price /= 100
            steam_store_price = steam_store_price.__round__(1)
            # print(game[0], "store price --> ", steam_store_price)

            if watch_game_price >= steam_store_price:
                watched_equals_store[game[0]] = True
            else:
                watched_equals_store[game[0]] = False

    # print(watched_equals_store)
    return watched_equals_store


def watch_vs_store_price(user_email : str):
    accounts = Report(user_email)
    account_list = accounts.get_report(reports_page=True)
    watched_by_steam_account = []
    account: SteamUser
    watched_vs_store = {}
    for account in account_list:
        user_watched_games = Database.list_of_watched_games(user_email, account.get_steam_id())
        watched_by_steam_account.append(user_watched_games)
        # print("Watched games and price for ", account, ": ", user_watched_games)

        for game in user_watched_games:
            watch_game_price = Database.get_watch_game_price(user_email, account.get_steam_id(), game[0])
            # print(game[0], " watch price --> ", watch_game_price)
            watched_game_ids = Database.get_watch_game_ID(user_email, account.get_steam_id(), game[0])
            steam_store_game = SteamStore.get_app_details(watched_game_ids)
            steam_store_price = float(steam_store_game.get('price'))
            steam_store_price /= 100
            steam_store_price = steam_store_price.__round__(1)
            # print(game[0], "store price --> ", steam_store_price)

            watched_vs_store[game[0]] = [watch_game_price, steam_store_price]
            # watched_vs_store.append([game[0], watch_game_price, steam_store_price])
    # print(watched_vs_store)
    return watched_vs_store
