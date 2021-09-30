#steamSetting Component - Tan Ngo

def hello ():
    return "Hello from Component steamSetting"

def get_game_price(gameid: str) -> str:
    """
    This method returns the price of a game, raises an exception if the gameid is invalid.
    :param string: The id of the game in question.
    :return: The price of the game based on the id.
    """
    pass

def on_sale(gameid: str) -> bool:
    """
    This method checks if the game is on sale, raises an exception if the game is invalid.
    :param string: The id of the game in question.
    :return: True if the game is on sale, false otherwise.
    """
    pass

def sale_price(gameid: str) -> str:
    """
    This method checks the price of the game on sale.
    :param string: The id of the game in question.
    :return: The price of the game that is on sale.
    """
    pass

