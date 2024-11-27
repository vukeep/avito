from requests.auth import HTTPBasicAuth
from requests import Session
from zeep import Client
from zeep.transports import Transport
from zeep.exceptions import Fault
from zeep import xsd
import json
from typing import Dict, List, Any
import os
import dotenv

dotenv.load_dotenv()

username_1c = os.getenv('username_1c')
password_1c = os.getenv('password_1c')
url_1c = os.getenv('url_1c')

class Data_1c:
    def __init__(self, username: str, password: str, url: str):
        try:
            session = Session()
            session.auth = HTTPBasicAuth(username.encode('utf-8'), password)
            self.client = Client(url, transport=Transport(session=session))
        except Exception as e:
            raise RuntimeError(f"Ошибка инициализации клиента SOAP: {e}")

    def stock(self, id_warehouse: str) -> List[Dict[str, Any]]:
        try:
            result = self.client.service.getPricesAndRests(id_warehouse)
            return json.loads(result)
        except Fault as e:
            raise ValueError(f"Ошибка запроса SOAP: {e}")
    

    def goods_stock(self, ar_product_1c: list) -> List[Dict[str, Any]]: # Получение остатков по id товара
        try:
            # Постройте список товаров с ожидаемым ключом
            goods_array = [{"Ссылка": pid} for pid in ar_product_1c]

            # Преобразуйте список в строку JSON с правильной кодировкой
            goods_array_json = json.dumps(goods_array, ensure_ascii=False)

            response = self.client.service.getQuantities(GoodsArray=goods_array_json)

            if not response:
                raise ValueError("Пустой ответ от сервера 1С.")

            return json.loads(response)
        except Fault as e:
            raise ValueError(f"Ошибка запроса SOAP: {e}")
        except json.JSONDecodeError:
            raise ValueError("Ответ от сервера 1С не является корректным JSON.")
        except Exception as e:
            raise ValueError(f"Неизвестная ошибка: {e}")



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
    #store_id = ['MME73RU-A']
    '''
    store_id = ["38661463-a478-11ea-8a9e-005056010801"] #,"38661463-a478-11ea-8a9e-005056010801","38661463-a478-11ea-8a9e-005056010801"]
    stocks = data.stock_store(store_id)
    for stock in stocks[0].get('Остатки'):
        print(stock)

    shops = data.shops()
    for shop in shops[0]['Подчиненные']:
        for sub_shop in shop['Подчиненные']:
            print(sub_shop['Наименование'], sub_shop['Ссылка'])
    '''

    store_id = '415894a0-952e-11e8-b502-005056010801'
    goods_stock = data.stock(store_id)
    for goods in goods_stock:
        print(goods.get('НоменклатураНаименование'), goods.get('НоменклатураКод'), goods.get('КоличествоОстаток'), goods.get('Цена'))
