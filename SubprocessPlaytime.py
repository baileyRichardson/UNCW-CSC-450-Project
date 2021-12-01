import Database
import Playtime
import SteamUser


def update_playtime(user_email: str):
    steam_accounts = Database.list_of_steam_accounts(user_email)
    for steam_acc in steam_accounts:
        account_data = Playtime.Playtime(steam_acc, user_email).get_game_info()
    return True
