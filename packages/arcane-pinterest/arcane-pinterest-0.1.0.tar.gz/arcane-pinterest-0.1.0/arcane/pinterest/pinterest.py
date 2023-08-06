import requests
import backoff
import base64

from typing import Dict

from .const import PINTEREST_SERVER_URL



class PinterestClient:
    def __init__(self, app_id: str, app_secret: str, token: str) -> None:
        self._app_id = app_id
        self._app_secret = app_secret
        self._token = token
        pass

    @backoff.on_exception(backoff.expo, requests.exceptions.HTTPError, max_tries=5)
    def _make_request(self, endpoint: str, method: str, headers: Dict = None, **kwargs) -> requests.models.Response:
        """Send a request to Pinterest API"""
        if headers == None:
            headers={'Authorization': f'Bearer {self._token}'}
        response = requests.request(method=method, url=f"{PINTEREST_SERVER_URL}{endpoint}", headers=headers, **kwargs)
        response.raise_for_status()
        return response

    def get_advertiser_details(self, advertiser_id: str) -> Dict:
        """Get advertiser campaigns given its ID."""
        reponse = self._make_request(
            f'/ads/v3/advertisers/{advertiser_id}/campaigns/',
            'GET'
            )
        return reponse.json()

    def get_campaign(self, campaign_id: str) -> Dict:
        """Gets a campaign object given its ID."""
        reponse = self._make_request(
            f'/ads/v3/campaigns/{campaign_id}/',
            'GET'
            )
        return reponse.json()



    def get_new_access_token(self, code: str) -> str:
        """Get the acccess token for Pinterest API

        This function is composed of two step:

        #1: Get the pinterest APP_ID (Directly from pinterest website or from pinterest credentials)
            Manually visit https://www.pinterest.com/oauth/?client_id=<APP_ID>&redirect_uri=https://app.arcane.run/&response_type=code.
            You will be redirect to a pinterest dialog where you should login and then authorize the app.
            Once the app is authorized, you will be redirect to AMS with a params named code in the url. Get the value, it will be the arg needed in this function.

        #2: Initiate the pinterest client. Then call this function with the code and you will get in response the new access token.
            With this new access token, you can update the credentials.

        For more information, please refers to: https://developers.pinterest.com/docs/redoc/combined_reporting/#section/User-Authorization

        Args:
            code (str): This is the code you must use to get the access token.

        Returns:
            str: The new access token
        """


        # Second step:
        client_information_encoded = base64.b64encode(f'{self._app_id}:{self._app_secret}'.encode()).decode('utf-8')
        reponse = self._make_request(
            '/v3/oauth/access_token/',
            'PUT',
            data={'code': code, 'redirect_uri': 'https://app.arcane.run/', 'grant_type': 'authorization_code'},
            headers={'Authorization': f"Basic {client_information_encoded}"}
            )
        return reponse.json()['data']['access_token']

