class SteamUser:
    def __init__(self, steam_id, steam_name, app_ids, names, img_icons, playtimes):
        self.__steam_id = steam_id
        self.__steam_name = steam_name
        self.__appid_array = app_ids
        self.__name_array = names
        self.__img_icon_array = img_icons
        self.__playtime_array = playtimes

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
        :return:
        """
        return self.__name_array

    def get_game_icons(self) -> [str]:
        return self.__img_icon_array

    def get_playtimes(self) -> [int]:
        return self.__playtime_array
