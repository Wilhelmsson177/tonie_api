"""The module of the Toniecloud session."""
import requests
from requests.exceptions import RequestException, Timeout

class TonieCloudSession(requests.Session):
    """A regular restss session to the TonieCloud REST API."""

    def __init__(self):
        """Initialize the session."""
        super().__init__()
        self.token: None | str = None

    def acquire_token(self, openid_connect: str, username: str, password: str, user_agent: str, timeout: int = 30) -> None:
        """Acquire a token from the ToniCloud SSO login using username and password.

        Args:
            username (str): The username
            password (str): The password_
            user_agent (str): A string with a representation as agent for request
            timeout (int): The request timeout. Try to increase this value if you receive a timeout error
        """

        data = {
            "grant_type": "password",
            "client_id": "my-tonies",
            "scope": "openid",
            "username": username,
            "password": password,
        }

        headers = {
            "User-Agent": user_agent,
        }

        # in any case clear the token before requests
        self.token = None

        try:
            response = requests.post(openid_connect, data=data, headers=headers, timeout=timeout)
            response.raise_for_status()
            self.token = response.json().get("access_token")
        except Timeout:
            raise ConnectionError("Request to acquire a token timed out.")
        except RequestException as e:
            raise PermissionError(f"An error occurred while acquiring a token: {e}")

    def validate_token(self, validate_url: str, token: str, user_agent: str, timeout: int = 30) -> None:
        """Validate a token for access to the ToniCloud SSO.

        Args:
            token (str): A valid token
            user_agent (str): A string with a representation as agent for request
            timeout (int): The request timeout. Try to increase this value if you receive a timeout error
        """

        data = {
        }

        headers = {
            "Authorization": f"Bearer {token}",
            "User-Agent": user_agent,
        }

        # in any case clear the token before requests
        self.token = None

        try:
            response = self.request('GET', validate_url, headers=headers, timeout=timeout)
            response.raise_for_status()
            self.token = token
        except Timeout:
            raise ConnectionError("Request to acquire a token timed out.")
        except RequestException as e:
            raise PermissionError(f"An error occurred while acquiring a token: {e}")
