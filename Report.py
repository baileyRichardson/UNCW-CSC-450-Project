# Adan Narvaez Munguia
from typing import List

from User import User


class ReportException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def get_user_id(user: User) -> int:
    """
    This method returns the userid for a specified user.
    :param user: the User you want to get the ID for.
    :return: The user's ID number or 0 if the user does not exist.
    """
    if user.username == "jimbob":
        return 0
    raise ReportException(message="User not found")


def report_data(user) -> List[str]:
    """
    This method passes a report to the notification component.
    :param user: the User the report is for.
    :return: A report as an array of JSON strings.
    """
    user = 0
    return ["report"]


def hello() -> str:
    """
    This method says hello :)
    :return: hi
    """
    return "Hello from Component Report"
