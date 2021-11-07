import pytest

from Report import Report, ReportException

# def get_user_id(user : User) -> int:
#     """
#     This method returns the userid for a specified user.
#     :param user: the User you want to get the ID for.
#     :return: The user's ID number or 0 if the user does not exist.
#     """
#     user = 0
#     return 0
from User import User


def test_instantiate_report():
    # "10000" corresponds to a test user. user_id is usually an email.
    user_id = "10000"
    # Instantiating a report object
    test_report = Report(user_id)
    # This specific test account should have a steam account in it.
    assert len(test_report.list_steam_accounts()) >= 1


def test_instantiate_report_id_not_found():
    user_id = "KASDJLKASDLJKDJQD"
    with pytest.raises(ReportException):
        test_report = Report(user_id)
