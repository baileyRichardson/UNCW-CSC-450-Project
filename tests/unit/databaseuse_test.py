import pytest

import DatabaseUse


def test_update_notifications_page():
    # not a valid time
    often = 6
    # a test account
    userID = "10000"
    assert (DatabaseUse.update_notifications_page(userID, often) is False)


def test_remove_steam_account():
    # a test account
    userID = "test@gmail"
    #an existing steam account
    steamID = 12345
    auto = "off"
    remove = "on"
    limit = "5"
    assert DatabaseUse.update_steam_account_page(userID, steamID, auto, remove, limit) == 1


def test_toggle_auto():
    # a test account
    userID = "test@gmail"
    #an existing steam account
    steamID = 12345
    auto = "on"
    remove = "off"
    limit = "5"
    assert DatabaseUse.update_steam_account_page(userID, steamID, auto, remove, limit) == 2


def test_add_steam_account():
    # a test account
    userID = "test@gmail"
    #an invalid steam account ID
    steamID = "asdfghj"
    assert DatabaseUse.add_steam_account(userID, steamID) is False


def test_add_to_watchlist():
    # a test account
    userID = "test@gmail"
    #an existing steamID
    steamID = 67890
    # an invalid URL
    gameURL = "asdfghjklpoiuytrewq"
    # a valid price
    price = 30.00
    assert DatabaseUse.add_to_watch_list(userID, steamID, gameURL, price) == "Please enter valid URL"


def run_all():
    test_update_notifications_page()
    test_toggle_auto()
    test_add_steam_account()
    test_remove_steam_account()
    test_add_to_watchlist()