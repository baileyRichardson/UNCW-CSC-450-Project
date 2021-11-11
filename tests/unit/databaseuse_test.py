import pytest

import DatabaseUse


def test_update_notifications_page():
    often = 6
    userID = "10000"
    assert (DatabaseUse.update_notifications_page(userID, often) is False)
