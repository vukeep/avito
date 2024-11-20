# /utils/request_handler.py
import requests
from ..config.settings import TIMEOUT

class RequestHandler:
    @staticmethod
    def send_request(url, method="GET", headers=None, data=None, params=None):
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=data if method in ["POST", "PUT", "PATCH"] else None,
                params=params if method == "GET" else None,
                timeout=TIMEOUT
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")
            return None