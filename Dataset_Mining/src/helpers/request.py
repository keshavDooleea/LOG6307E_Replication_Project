import requests
from helpers.env import get_github_token

class RequestHelper:

    @staticmethod
    def get_rate_limit():
        return RequestHelper.get_api_response("https://api.github.com/rate_limit")["rate"]

    @staticmethod
    def get_api_response(url: str, add_token = True):
        token = get_github_token()

        if add_token:
            headers = { 'Authorization': f'token {token}' }
        else:
            headers = {}

        try:
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Request error exception: {e}")