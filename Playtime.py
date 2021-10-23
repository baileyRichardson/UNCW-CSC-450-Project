"""
Authors: William Ebright, Adan Narvaez Munguia
Things that must be done:
- Retrieving Tracked Games
- Comparing playtime to last known playtime
- Reflecting playtime comparisons that for the purposes of (pardon my français) day/week/month bs
- Replacing the generic exceptions with more helpful ones
"""
# import Report  #for later
import requests
from steamwebapi import profiles
from steamwebapi.api import ISteamUser, IPlayerService
from flask import json

class Playtime:
    def __init__(self, user_id: int):
        """
        This is the constructor for the class.
        It retrieves the user's profile and sets it as a class attribute.
        :param user_id: The desired user's Steam User ID.
        """
        self.steam_api_key = '25F01C7C51803E91E331CBAD669F542C'
        self.steam_id = user_id
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
        This function returns a Steam User's Owned Games.
        :return: Dictionary of the user's games. The name of the game is the key. The item is a List containing the game's total playtime, app id, and icon image URL.
        """
        try:
            player_service = IPlayerService(steam_api_key=self.steam_api_key)
            games = player_service.get_owned_games(self.steam_id, include_appinfo=True, include_played_free_games=True)['response']['games']
            playtimes = {}
            for i in games:
                playtimes[i['name']] = [i['playtime_forever'], i['appid'], i['img_icon_url']]
            return playtimes
        except:
            raise SyntaxError("Steam id is invalid")
