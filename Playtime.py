"""
Author: William Ebright
"""
# import Report  #for later
from steamwebapi import profiles
from steamwebapi.api import ISteamUser, IPlayerService


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

    """ This function is unneeded but I don't want to delete it in case it isn't.
    def get_player_id(profile_name: str, steam_api_key: str) -> int:
        \"""
        This function returns the current user's steam ID using their profile name.
        :param profile_name: user object for whom we want to get steam id.
        :param steam_api_key: Developer key to access API.
        :return: The steam ID of user based on user's username.
        \"""
        try:
            user_info = ISteamUser(steam_api_key=steam_api_key)
            steamid = user_info.resolve_vanity_url(profile_name)['response']['steamid']
            return steamid
        except:
            print("Steam id is invalid")
            return 0
            # raise SyntaxError("Steam id is invalid")
    """

    def get_display_name(self) -> str:
        """
        Get the display name for this Steam Account.
        :return: The display name as a string.
        """
        try:
            player_service = ISteamUser(steam_api_key=self.steam_api_key)
            display_name = player_service.get_player_summaries(self.steam_id)['response']['personaname']
            return display_name
        except:
            print("Steam ID is invalid")
            return "Unknown Steam ID"
            # raise SyntaxError("Steam id is invalid")

    def get_game_info(self) -> list:
        """
        This function returns a steam users owned games as well as extra information.
        :return: List of a user's games with related info.
        """

        try:
            player_service = IPlayerService(steam_api_key=self.steam_api_key)
            games = player_service.get_owned_games(self.steam_id)['response']['games']
            return games
        except:
            print("Steam ID is invalid")
            return []
            # raise SyntaxError("Steam id is invalid")

    def get_games(self) -> list:
        """
        This function returns a steam users owned games.
        :return: List of a user's games.
        """
        try:
            player_service = IPlayerService(steam_api_key=self.steam_api_key)
            games = player_service.get_owned_games(self.steam_id)['response']['games']
            return list((i['name'] for i in games))
        except:
            print("Steam id is invalid")
            return []
            # raise SyntaxError("Steam id is invalid")

    def get_playtime(self) -> list:
        """
        This function returns a steam users playtime
        :param game_name: game for which we are getting the playtime of.  #future
        :return: The steam playtime, raises exception if user does not exist.
        """
        steam_api_key = self.steam_api_key
        try:
            player_service = IPlayerService(steam_api_key=steam_api_key)
            games = player_service.get_owned_games(self.steam_id)['response']['games']
            return list((i['playtime_forever'] for i in games))
        except:
            print("Steam id is invalid")
            return []

    def get_total_playtime(self, steam_id: int, steam_api_key: str) -> list:
        """
        This function returns a steam users playtime
        :param steam_api_key: Developer key to access API.
        :param game_name: game for which we are getting the playtime of.  #future
        :param steam_id: user ID for whom we want to get playtime for.
        :return: The steam playtime, raises exception if user does not exist.
        """
        try:
            player_service = IPlayerService(steam_api_key=steam_api_key)
            games = player_service.get_owned_games(steam_id)['response']['games']
            total_list = list((i['playtime_forever'] for i in games))
            return total_list
        except:
            print("Steam id is invalid")
            return []

        # for i in (x for x in games if x['name'] == game_name):  # game is owned
        #     return True

    """
    Notes:
    In order to track games, games tracked would have to be stored in a txt file (in database?) <-- for later
    * Tracking specific games should be in next sprint?

    Sprint 1 for Playtime then = user shown list of games on steam account with total playtime with each + total overall

    main currently set up to show off steamAPI calls for Sprint 1!
    
    Notes from Adan:
    Games being tracked are being called into a list. We can use this to store JSON into the database.
    """
