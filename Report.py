# Adan Narvaez Munguia
from Playtime import Playtime
from SteamUser import SteamUser
import Database


class ReportException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Report:
    def __init__(self, user: str):
        """
        Constructor for the Report class.
        :param user: User ID as a string.
        """
        self.user = user
        self.steam_accounts = []
        self.report = []

        try:
            user_list = Database.list_of_steam_accounts(user)
            steam_list = []
            for key in user_list:
                steam_list.append(key)
            for account in user_list:
                self.steam_accounts.append(Playtime(account))
        except TypeError:
            raise ReportException("User not found.")

    def list_steam_accounts(self) -> [str]:
        """
        Lists the display names of all of a user's steam accounts.
        :return: The display names as a list of strings.
        """
        if len(self.steam_accounts) == 0:
            raise ReportException("No Steam Accounts Found!")
        display_name_list = []
        for account in self.steam_accounts:
            display_name_list.append(account.get_display_name())
        return display_name_list

    # Pycharm is being whiny:
    # noinspection PyMethodMayBeStatic
    def __get_games(self, account: Playtime) -> []:
        """
        Retrieves games and their information for the report.
        :param account: The specified account.
        :return: List of Lists containing the name, appid, img hash, and total playtime for each game.
        """
        try:
            return account.get_game_info()
        except SyntaxError:
            raise ReportException("Steam ID is invalid.")

    def __generate_report_data(self):
        """
        Pulls the report data from the SteamAPI.
        :return: No return value, but the data is stored in self.report.
        """
        account_names = self.list_steam_accounts()
        account_index = 0
        steam_games = []
        for account in self.steam_accounts:
            account_data = self.__get_games(account)
            steam_data = SteamUser(account.steam_id, account_names[account_index], account_data[0], account_data[1],
                                   account_data[2], account_data[3])
            account_index = account_index + 1
            steam_games.append(steam_data)
        self.report = steam_games

    def __generate_email_html(self):
        """
        Generates HTML for the Mail module.
        :return: A string with formatted HTML.
        """
        email_text = (
            f'<!DOCTYPE html>\n'
            f'<html>\n'
            f'    <body>\n'
            f'        <p>The following is an email report:</p>\n'
            f'        <h1>Total Playtimes:</h1>\n'
        )
        steam_account: SteamUser
        for steam_account in self.report:
            game_names = steam_account.get_game_names()
            total_playtimes = steam_account.get_playtimes()
            email_text = email_text + (
                f'            <h2>Account: {steam_account.get_steam_name()}</h2>\n'
                f'                <table>\n'
                f'                    <tr>\n'
                f'                        <th>Game</th>\n'
                f'                        <th>Total Playtime</th>\n'
                f'                    </tr>\n'
            )
            for i in range(len(game_names)):
                email_text = email_text + (
                    f'                    <tr>\n'
                    f'                        <td>{game_names[i]}</th>\n'
                    f'                        <td>{total_playtimes[i]}</th>\n'
                    f'                    </tr>\n'
                )
            email_text = email_text + f'                </table>\n'
        email_text = email_text + (
            f'    </body>\n'
            f'</html>\n'
        )
        return email_text

    def get_report(self, reports_page=False, reports_email=False):
        if len(self.steam_accounts) == 0:
            raise ReportException("No Steam Accounts for this user!")
        if len(self.report) == 0:
            self.__generate_report_data()
        if reports_page:
            return self.report
        elif reports_email:
            return self.__generate_email_html()
        else:
            raise ReportException("Undefined report type.")
