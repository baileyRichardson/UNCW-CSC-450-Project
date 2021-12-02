import Database
import Mail
import Playtime
import SteamUser


def update_playtime(user_email: str):
    steam_accounts = Database.list_of_steam_accounts(user_email)
    for steam_acc in steam_accounts:
        account_data = Playtime.Playtime(steam_acc, user_email).get_game_info()
    return True


def compare_playtime(user_email: str):
    steam_accounts = Database.list_of_steam_accounts(user_email)
    for account in steam_accounts:
        limit = Database.get_playtime_limit(user_email, account)
        total = Database.get_playtime_sums(user_email, account)
        if total >= limit:
            Mail.send_limit_notification(limit, total, account, Database.get_email(user_email))