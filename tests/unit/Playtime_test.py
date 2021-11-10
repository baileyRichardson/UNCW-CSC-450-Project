"""
Authors: William Ebright
"""
import pytest
import playwright
from Playtime import Playtime


class testPlaytime:
    def __init__(self):
        self.userID = 12345678912345678
        self.steam_api_key = '25F01C7C51803E91E331CBAD669F542C'

    def test_get_display_name(self):
        assert Playtime.get_display_name(self.steam_api_key, self.userID)

    def test_get_display_name2(self):
        with pytest.raises(SyntaxError):
            Playtime.get_display_name()
