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
        self.steam_accounts = []
        # Going to get steam accounts from database and store them in user_list
        user_list = []
        for account in user_list:
            self.steam_accounts.append(Playtime(account))


    def report_data(user) -> List[str]:
        """
        This method passes a report to the notification component.
        :param user: the User the report is for.
        :return: A report as an array of JSON strings.
        """
        user = 0
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
