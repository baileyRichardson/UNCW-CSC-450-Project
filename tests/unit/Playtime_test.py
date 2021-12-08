"""
Authors: William Ebright
"""
import pytest
import playwright
from Playtime import Playtime


class testPlaytime:
    def __init__(self):
        self.userID = 12345678912345678

    def test_get_display_name(self):
        assert Playtime.get_display_name()

    def test_get_display_name2(self):
        with pytest.raises(SyntaxError):
            Playtime.get_display_name()
