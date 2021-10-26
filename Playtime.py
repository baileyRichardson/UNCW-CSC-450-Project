"""
Authors: William Ebright, Adan Narvaez Munguia
Things that must be done:
- Retrieving Tracked Games - must be done though database (probably)
- Comparing playtime to last known playtime - must be done though database (probably)
- Reflecting playtime comparisons that for the purposes of (pardon my français) day/week/month bs
- Replacing the generic exceptions with more helpful ones  - Do during testing in Lab?
"""
import requests
from flask import json
from steamwebapi import profiles
from steamwebapi.api import ISteamUser, IPlayerService, ISteamUserStats, ISteamWebAPIUtil, SteamCommunityXML
import steamspypi

# from steam.steamid import SteamID  # Possibly useful later; Ignore for now.


class Playtime:
    def __init__(self, user_id: int, app_id: int):
        """
        This is the constructor for the class.
        It retrieves the user's profile and sets it as a class attribute.
        :param user_id: The desired user's Steam User ID.
        """
        self.steam_api_key = '25F01C7C51803E91E331CBAD669F542C'
        self.steam_id = user_id
        self.app_id = app_id
        try:
            self.user_profile = profiles.get_user_profile(user_id)
            if self.user_profile.primaryclanid:
                # Group ID '103582791429521408' is often encountered.
                # In hex, that ID is '0x170000000000000' which has 0 in the
                # lower 32bits. There is no actual group ID, just the universe,
                # account type identifiers, and the instance.
                # https://developer.valvesoftware.com/wiki/SteamID
                if (int(self.user_profile.primaryclanid) & 0x00000000FFFFFFFF) != 0:
                    self.primary_group_profile = profiles.get_group_profile(self.user_profile.primaryclanid)
                else:
                    self.primary_group_profile = None
            else:
                self.primary_group_profile = None
        except:
            self.profileGrabStatus = False

    def get_display_name(self) -> str:
        """
        Get the display name for this Steam Account.
        :return: The display name as a string.
        """
        try:
            player_service = ISteamUser(steam_api_key=self.steam_api_key)
            display_name = player_service.get_player_summaries(self.steam_id)['response']['players'][0]['personaname']
            return display_name
        except:
            raise SyntaxError("Steam id is invalid")

    def get_game_info(self) -> dict:
        """
        This function returns a Steam User's Owned Games as well as the games playtime, appID, and image icon URL.
        :return: Dictionary of the user's games. The name of the game is the key. The item is a List containing the
                 game's total playtime, app id, and icon image URL.
        """
        try:
            player_service = IPlayerService(steam_api_key=self.steam_api_key)
            games = player_service.get_owned_games(self.steam_id, include_appinfo=True, include_played_free_games=True)[
                'response']['games']
            playtimes = {}
            for i in games:
                playtimes[i['name']] = [i['playtime_forever'], i['appid'], i['img_icon_url']]
            return playtimes
        except:
            raise SyntaxError("Steam id is invalid")

    def get_app_details(self, app_id: str) -> dict:
        """
        This function returns details for an application's ID
        :return: dictonary of info about a game.
        """
        try:
            data_request = dict()
            data_request['request'] = 'appdetails'
            appID = str(self.app_id)
            data_request['appid'] = appID
            data = steamspypi.download(data_request)  # steamspypi's download function is already checking if the
            return data  # request is valid, and also attempts to repair it.
        except:
            raise SyntaxError("App_id is invalid")

    """
    def get_game_stats(self, appID: int, count: int, names: list, steam_api_key: str) -> list:
        \"""
        THIS IS A BACKUP METHOD; should work if steamspypy is no longer an option
        Get the global stats for a given game.
        :return: Stats for a given game
        \"""
        try:
            service_stats = ISteamUserStats(steam_api_key=self.steam_api_key)
            game_stats = service_stats.get_global_stats_for_game(appID, count, names, )['response']['games']
            return game_stats
        except:
            print("Steam ID is invalid")
            return []
            # raise SyntaxError("Steam id is invalid")

    def get_app_details_brute(app_id: int) -> dict:
        \"""
        THIS IS ALSO BACKUP METHOD; is another method that should function identically to get_app_details
        Get the global stats for a given game.
        :return: Stats for a given game
        \"""
        response = get(f'{config.STEAMSPY_URL}/api.php?request=appdetails&appid={game_id}')
        response.raise_for_status()
        return json.loads(response.text)

    """
