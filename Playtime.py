"""
Author: William Ebright
"""


class Playtime:

    def __init__(self, steamuser: str):
        self.steamuser = steamuser

    def get_steam_user(username: str) -> id:
        """
        This function returns the current user's steam ID.
        :param username: user object for whom we want to get steam id.
        :return: The steam ID of user, raises exception if user does not exist.
        """
        pass

    def get_Playtime(steamID: id, game) -> int:
        """
        This function returns a steam users playtime
        :param game: game for which we are getting the playtime of.
        :param steamID: user object for whom we want to get playtime for.
        :return: The steam playtime of user on given game, raises exception if user does not exist.
        """
        pass


def hello():
    return "Hello from Component Playtime"


def main():
    pass


if __name__ == '__main__':
    main()