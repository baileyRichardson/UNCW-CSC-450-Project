"""
For account settings.

Bailey Richardson
"""
from User import User

def get_account_preferences(user: User) -> List[accountInfo]:
    """
    This method returns the account preferences for a user.
    :param self: the User object for whom to retrieve the account preferences
    :return: a list of account preference objects or an empty list if the user has no account preferences
    """
    pass


def get_notification_preferences(user: User) -> List[accountInfo]:
    """
    This method returns the notification preferences for a user.
    :param user: the User object for whom you want to get notification preferences
    :return: a list of notification preference objects or an empty list if the user has no notification preferences
    """
    pass


def hello() -> str:
    return "Hello from component accountSettings"
