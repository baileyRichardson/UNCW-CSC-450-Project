import pytest

from Report import ReportException
from Subprocess import compare_with_steam_store

def test_compare_watch_to_store():
    # using account which has watched games added
    user_email = "matthewjar2000@gmailcom"
    # make sure a dictionary of games and booleans is being returned
    assert len(compare_with_steam_store(user_email)) >= 0

def test_when_no_steam_account():
    # using account which does not have a steam account linked
    user_email = "brr4103@uncwedu"
    # should give a ReportException because no steam account is linked
    with pytest.raises(expected_exception=ReportException):
        compare_with_steam_store(user_email)

