# /auth/authentication.py

import requests


class Authentication:
    def __init__(self, client_id, client_secret):
        '''
        Инициализация класса Authentication
        '''
        api_key = self.create_token(client_id, client_secret)

        self.api_key = api_key

    def get_headers(self):
        # Возвращает заголовки для каждого запроса
        return {"Authorization": f"Bearer {self.api_key}"}
    
    def create_token(self, client_id, client_secret):
        url = "https://api.avito.ru/token/"
        data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret
        }

        response = requests.post(url, data=data)
        if response.status_code == 200:
            return response.json().get("access_token")
        else:
            raise Exception(f"Ошибка при получении токена: {response.status_code} - {response.text}")