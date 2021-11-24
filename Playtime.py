"""
Authors: William Ebright, Adan Narvaez Munguia
"""
import requests
from flask import json
from steamwebapi import profiles
from steamwebapi.api import ISteamUser, IPlayerService, ISteamUserStats, ISteamWebAPIUtil, SteamCommunityXML
import steamspypi


# from steam.steamid import SteamID  # Possibly useful later; Ignore for now.
import Database
from SteamUser import SteamUser


class Playtime:
    def __init__(self, steam_user_id: int, user_email: str):
        """
        This is the constructor for the class.
        It retrieves the user's profile and sets it as a class attribute.
        :param steam_user_id: The desired user's Steam User ID.
        :param user_email: The desired user's email.
        """
        self.steam_api_key = '25F01C7C51803E91E331CBAD669F542C'
        self.steam_id = steam_user_id
        self.user_email = user_email
        self.playtimes = Database.list_of_tracked_games(self.user_email, self.steam_id)
        try:
            self.user_profile = profiles.get_user_profile(steam_user_id)
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
            raise SyntaxError("Unable to grab profile.")

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

    def get_game_info(self) -> SteamUser:
        """
        This function returns a Steam User's Owned Games as well as the games playtime, appID, and image icon URL.
        :return: A SteamUser object.
        """
        try:
            player_service = IPlayerService(steam_api_key=self.steam_api_key)
            games = player_service.get_owned_games(self.steam_id, include_appinfo=True, include_played_free_games=True)[
                'response']['games']
            #print(games)
            appids_array = []
            names_array = []
            img_array = []
            playtimes_array = []
            daily_playtimes_array = []
            monthly_playtimes_array = []
            for i in games:
                appids_array.append(int(i['appid']))
                names_array.append(i['name'])
                img_array.append(i['img_icon_url'])
                playtimes_array.append(int(i['playtime_forever']))
                """
                if i['name'] in self.playtimes:
                    daily_playtime = i['playtime_forever'] - int(Database.get_playtime(self.user_email, self.steam_id, i['name']))
                    monthly_playtime = i['playtime_forever'] - int(Database.get_playtime(self.user_email, self.steam_id, i['name']))
                    Database.update_playtime(self.user_email, self.steam_id, i['name'], i['playtime_forever'])
                    daily_playtimes_array.append(daily_playtime)
                    monthly_playtimes_array.append(monthly_playtime)
                else:
                    daily_playtimes_array.append(-1)
                """
            steam_info = SteamUser(self.steam_id, self.get_display_name(), appids_array, names_array, img_array, playtimes_array, monthly_playtimes_array, daily_playtimes_array)
            #print(steam_info)
            return steam_info
        except SyntaxError:
            print("Error from Steam!")
        except:
            raise SyntaxError("Steam id is invalid")
