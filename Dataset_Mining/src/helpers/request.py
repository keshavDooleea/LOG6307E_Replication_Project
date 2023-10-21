import requests
from helpers.env import get_github_token

class RequestHelper:

    @staticmethod
    def get_api_response(url: str):
        token = get_github_token()

        headers = {
            'Authorization': f'token {token}'
        }

        try:
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Request error exception: {e}")