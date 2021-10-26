# Adan Narvaez Munguia
from Playtime import Playtime
import Database


class ReportException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Report:
    def __init__(self, user=str):
        """
        Constructor for the Report class.
        :param user: User ID as a string.
        """
        self.user = user
        self.steam_accounts = []
        user_list = Database.list_of_steam_accounts(user)
        steam_list = []
        for key in user_list:
            steam_list.append(key)
        for account in user_list:
            self.steam_accounts.append(Playtime(account))

    def list_steam_accounts(self) -> list:
        """
        Lists the display names of all of a user's steam accounts.
        :return: The display names as a list of strings.
        """
        if len(self.steam_accounts) == 0:
            raise ReportException(message="No Steam Accounts Found!")
        display_name_list = []
        for account in self.steam_accounts:
            display_name_list.append(account.get_display_name())
        return display_name_list

    def get_games(self, account: Playtime) -> dict[str]:
        """
        Retrieves games and their information for the report.
        :param account: The specified account.
        :return: Dictionary of the user's games. The name of the game is the key. The item is a List containing the game's total playtime, app id, and icon image URL.
        """
        try:
            return account.get_game_info()
        except SyntaxError:
            return {"Error": "No games Found on this account. It may be private."}

    def generate_report_text(self):
        report_text = []
        account_names = [self.list_steam_accounts()]
        account_index = 0
        steam_games = []
        for account in self.steam_accounts:
            steam_games.append(account_names[account_index][0])
            account_index += 1
            steam_games.append(self.get_games(account))
            report_text.append(steam_games)
        return report_text


def test():
    user_id = "10000"
    # steam_id = 76561198065124435
    # Database.create_user(user_id, "test@fakemail.edu")
    # Database.add_steam_account(user_id, steam_id)
    user_report = Report(user_id)
    print(user_report.generate_report_text())
