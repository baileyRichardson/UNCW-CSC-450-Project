import pytest

import Report

# def get_user_id(user : User) -> int:
#     """
#     This method returns the userid for a specified user.
#     :param user: the User you want to get the ID for.
#     :return: The user's ID number or 0 if the user does not exist.
#     """
#     user = 0
#     return 0
from User import User


def test_get_user_id():
    user = User("jimbob")
    assert Report.get_user_id(user) == 0

def test_get_user_id_not_found():
    user = User("KASDJLKASDLJKDJQD")
    with pytest.raises(Report.ReportException):
        Report.get_user_id(user)

