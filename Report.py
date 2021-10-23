# Adan Narvaez Munguia
from typing import List
from Playtime import Playtime
from User import User


class ReportException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Report():
    def __init__(self, user):
        """
        Constructor for the Report class.
        :param user:
        """
        self.user = user
        self.steam_accounts = []
        # Going to get steam accounts from database and store them in user_list
        user_list = []
        for account in user_list:
            self.steam_accounts.append(Playtime(account))

    def report_data(self) -> List[str]:
        """
        This method passes a report to the notification component.
        :return: A report as an array of JSON strings.
        """
        self.user = 0
        return ["report"]

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

    def get_games(self, account: Playtime) -> List[str]:
        try:
            return account.get_games()
        except SyntaxError:
            return ["No games Found on this account. It may be private."]

    def get_playtimes(self, account: Playtime) -> List[str]:
        try:
            return account.get_playtime()
        except SyntaxError:
            return ["0"]

    def generate_report_text(self):
        report_text = [self.list_steam_accounts()]
        steam_games = []
        steam_playtimes = []
        for account in self.steam_accounts:
            steam_games.append(self.get_games(account))
            steam_playtimes.append(self.get_playtimes(account))
        report_text.append(steam_games)
        report_text.append(steam_playtimes)
        return report_text
