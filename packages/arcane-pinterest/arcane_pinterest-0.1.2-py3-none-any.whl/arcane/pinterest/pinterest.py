import requests
import backoff
import base64
import json

from typing import Dict, List

from .const import PINTEREST_SERVER_URL
from .exceptions import PinterestAccountLostAccessException
from arcane.core import Campaign

class PinterestClient:
    def __init__(self, pinterest_credentials: str) -> None:
        with open(pinterest_credentials) as credentials:
            pinterest_credentials = json.load(credentials)
        self._app_id = pinterest_credentials.get('app_id'),
        self._app_secret = pinterest_credentials.get('app_secret'),
        self._token = pinterest_credentials.get('access_token')


    @backoff.on_exception(backoff.expo, requests.exceptions.HTTPError, max_tries=5)
    def _make_request(self, endpoint: str, method: str, headers: Dict = None, **kwargs) -> requests.models.Response:
        """Send a request to Pinterest API"""
        if headers == None:
            headers={'Authorization': f'Bearer {self._token}'}
        response = requests.request(method=method, url=f"{PINTEREST_SERVER_URL}{endpoint}", headers=headers, **kwargs)
        response.raise_for_status()
        return response

    def get_advertiser_campaigns(self, advertiser_id: str) -> List[Campaign]:
        """Get advertiser campaigns given its ID."""
        try:
            response = self._make_request(
                f'/ads/v3/advertisers/{advertiser_id}/campaigns/',
                'GET'
                )
        except requests.exceptions.HTTPError as e:
            error_code = e.response.status_code
            if error_code in [401, 403]:
                raise PinterestAccountLostAccessException(f"We cannot access your pinterest account with the id: {advertiser_id}. Are you sure you granted access?")
            if error_code == 404:
                raise PinterestAccountLostAccessException(f"We cannot find this account with the id: {advertiser_id}. Are you sure you entered the correct id?")

        return [Campaign(
            campaign_id= campaign.get('id'),
            campaign_name= campaign.get('name'),
            campaign_status= campaign.get('status')
        ) for campaign in response.json()['data']]





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

