import pytest
"""
Authors: William Ebright, Adan Narvaez Munguia
"""
from Playtime import Playtime
import Database


def test_get_game_info():
    user_email = "10000"
    steam_id = Database.list_of_steam_accounts(user_email)[0]
    playtime_test = Playtime(steam_id, user_email)
    playtime_games = playtime_test.get_game_info()
    assert len(playtime_games.get_game_names()) >= 1  # check if info is gathered; if so should be dic.


def test_get_display_name():
    user_email = "10000"
    steam_id = Database.list_of_steam_accounts(user_email)[0]
    playtime_test = Playtime(steam_id, user_email)
    assert len(playtime_test.get_display_name()) >= 1  # simple test to see if there is a display name.


def test_user_not_found():
    steam_id = 30013
    user_email = "10000"
    with pytest.raises(AttributeError):
        Playtime(steam_id, user_email).get_display_name()
