from requests.auth import HTTPBasicAuth, AuthBase
from requests import Session
from zeep import Client
from zeep.transports import Transport
from zeep.exceptions import Fault
import json
from typing import Dict, List, Any
import os
import base64
import dotenv

dotenv.load_dotenv()

username_1c = os.getenv('username_1c')
password_1c = os.getenv('password_1c')
url_1c = os.getenv('url_1c')


class UTF8HTTPBasicAuth(AuthBase):
    """HTTP Basic Auth, поддерживающий UTF-8 логин и пароль"""
    def __init__(self, username, password):
        self.auth_str = f"{username}:{password}"
        self.encoded_auth = base64.b64encode(self.auth_str.encode("utf-8")).decode("utf-8")

    def __call__(self, r):
        r.headers["Authorization"] = f"Basic {self.encoded_auth}"
        return r

class Data_1c:
    def __init__(self, username: str, password: str, url: str):
        try:
            session = Session()
            session.auth = UTF8HTTPBasicAuth(username, password)
            self.client = Client(url, transport=Transport(session=session))
        except Exception as e:
            raise RuntimeError(f"Ошибка инициализации клиента SOAP: {e}")

    def stock(self, id_warehouse: str) -> List[Dict[str, Any]]:
        try:
            result = self.client.service.getPricesAndRests(id_warehouse)
            return json.loads(result)
        except Fault as e:
            raise ValueError(f"Ошибка запроса SOAP: {e}")

    def shops(self) -> List[Dict[str, Any]]:
        try:
            result = self.client.service.getStoresList()
            return json.loads(result)
        except Fault as e:
            raise ValueError(f"Ошибка запроса SOAP: {e}")

def dict_shops(data: List[Dict[str, Any]], res_dict: Dict[str, str] = None) -> Dict[str, str]:
    if res_dict is None:
        res_dict = {}
    for shop in data:
        sub_shops = shop.get('Подчиненные')
        if sub_shops:
            dict_shops(sub_shops, res_dict)
        else:
            res_dict[shop['Наименование']] = shop['Ссылка']
    return res_dict

if __name__ == '__main__':
    data = Data_1c(username_1c, password_1c, url_1c)

    try:
        shops = data.shops()
        shop_dict = dict_shops(shops)
        print(f"Количество складов: {len(shop_dict)}")
    except Exception as e:
        print(f"Ошибка: {e}")