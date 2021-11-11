"""
Authors: William Ebright
##Run simply by Running main()##
"""
import pytest
from Playtime import Playtime


def test_get_game_info(userID):
    assert len(Playtime.get_game_info(Playtime(userID))) >= 1  # check if info is gathered; if so should be dic.


def test_get_display_name(userID):
    assert len(Playtime.get_display_name(Playtime(userID))) >= 1  # simple test to see if there is a display name.


def main():
    userID = 76561198023715682
    try:
        test_get_game_info(userID)
        test_get_display_name(userID)
    except:
        print("One or more tests caused an error")


if __name__ == '__main__':
    main()
