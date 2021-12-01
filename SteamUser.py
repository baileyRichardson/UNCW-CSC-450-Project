class SteamUser:

    def __init__(self, steam_id: int, steam_name: str, app_ids: [int], names: [str], img_icons: [str],
                 playtimes: [int], weekly_playtimes: [int], daily_playtimes: [int]):
        self.__steam_id = steam_id
        self.__steam_name = steam_name
        self.__appid_array = app_ids
        self.__name_array = names
        self.__img_icon_array = img_icons
        self.__playtime_array = playtimes
        self.__weekly_playtimes_array = weekly_playtimes
        self.__daily_playtimes_array = daily_playtimes

    def get_steam_id(self) -> int:
        """
        Returns the SteamID.
        :return: Steam ID as an integer.
        """
        return self.__steam_id

    def get_steam_name(self) -> str:
        """
        Returns the User's Display Name.
        :return: Steam Display name as a string.
        """
        return self.__steam_name

    def get_game_appids(self) -> [int]:
        """
        Returns the array of appids.
        :return: Integer array of app ids.
        """
        return self.__appid_array

    def get_game_names(self) -> [str]:
        """
        Returns the array of game names.
        :return: String array of game names.
        """
        return self.__name_array

    def get_game_icons(self) -> [str]:
        """
        Returns the array of image hashes.
        :return: String array of image hashes.
        """
        return self.__img_icon_array

    def get_playtimes(self) -> [int]:
        """
        Returns array of total playtimes.
        :return: Integer array of total playtimes.
        """
        return self.__playtime_array

    def get_weekly_playtimes(self) -> [int]:
        """
        Returns array of monthly playtimes.
        :return: Integer array of monthly playtimes.
        """
        return self.__weekly_playtimes_array

    def get_daily_playtimes(self) -> [int]:
        """
        Returns array of daily playtimes.
        :return: Integer array of daily playtimes.
        """
        return self.__daily_playtimes_array
