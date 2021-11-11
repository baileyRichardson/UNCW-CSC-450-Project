import requests
from flask import json
import steamspypi


class SteamStore:


    def get_app_details(app_id: str) -> dict:
        """
        This function returns details for an application's ID
        :return: dictionary of info about a game.
        """
        try:
            data_request = dict()
            data_request['request'] = 'appdetails'
            appID = str(app_id)
            data_request['appid'] = appID
            data = steamspypi.download(data_request)  # steamspypi's download function is already checking if the
            return data  # request is valid, and also attempts to repair it.
        except:
            raise SyntaxError("App_id is invalid")
