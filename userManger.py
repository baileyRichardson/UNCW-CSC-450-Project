#userManager Component - Tan Ngo
import User

def create_mainAccount(email: str, password: str):

    pass

def hello ():
    return "Hello from Component userManager"

def get_user(username: str) -> User:
    """
    This function just returns the current user based on who is logged in.
    :return: The userid based on the username, raises exception if user does not exist.
    """
    pass

def get_email(user: User) -> str:
    """
    this function returns the email of the associated user.
    :param userid: The id of the user.
    :return: The email of the user associated.
    """
    pass
