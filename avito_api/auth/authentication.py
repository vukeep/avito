# /auth/authentication.py

import requests
import os
import dotenv

dotenv.load_dotenv()

client_id = os.getenv("Client_id_iSmartChita")
client_secret = os.getenv("Client_secret_iSmartChita")

def create_token():
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

class Authentication:
    def __init__(self):
        '''
        Инициализация класса Authentication
        '''
        api_key = create_token()

        self.api_key = api_key

    def get_headers(self):
        # Возвращает заголовки для каждого запроса
        return {"Authorization": f"Bearer {self.api_key}"}