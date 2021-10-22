# Adan Narvaez Munguia
from Playtime import Playtime


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

    def list_steam_accounts(self) -> list:
        """
        Lists the display names of all of a user's steam accounts.
        :return: The display names as a list of strings.
        """
        if len(self.steam_accounts) == 0:
            print("No Steam Accounts are linked!")
            return []
        display_name_list = []
        for account in self.steam_accounts:
            display_name_list.append(account.get_display_name())
        return display_name_list
