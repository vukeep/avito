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
import pandas as pd
import time
from utils.logger import get_logger
import traceback
from requests.exceptions import ConnectTimeout
dotenv.load_dotenv()

class Data_1c:
    def __init__(self):
        self.username = os.getenv('username_1c')
        self.password = os.getenv('password_1c')
        self.url = os.getenv('url_1c')
        self.logger = get_logger('Data_1c')
        self.logger.debug("Stack trace during __init__:\n%s", ''.join(traceback.format_stack()))


        self.client = None
        self.max_retries = 3
        self.retry_delay = 5  # seconds

        self.initialize_client()

    def initialize_client(self):
        attempt = 0
        while attempt < self.max_retries:
            try:
                session = Session()
                session.auth = HTTPBasicAuth(self.username.encode('utf-8'), self.password)
                self.client = Client(self.url, transport=Transport(session=session))
                self.logger.info("Успешное подключение к SOAP клиенту.")
                break
            except ConnectTimeout as e:
                self.logger.error(f"Ошибка подключения: {e}. Попытка {attempt + 1} из {self.max_retries}.")
                attempt += 1
                time.sleep(self.retry_delay)
            except Exception as e:
                self.logger.error(f"Ошибка инициализации клиента SOAP: {e}")
                raise RuntimeError(f"Ошибка инициализации клиента SOAP: {e}")

        if self.client is None:
            raise RuntimeError("Не удалось подключиться к SOAP клиенту после нескольких попыток.")

    def ensure_connection(self):
        """
        Проверяет и восстанавливает соединение с сервером, если это необходимо.
        """
        if self.client is None:
            self.logger.info("Попытка восстановления соединения с сервером.")
            self.initialize_client()

    def stock(self, id_warehouse: str, SN_Level: bool = True) -> List[Dict[str, Any]]:
        '''
        Получение остатков и цен на товары
        :param id_warehouse: ID склада
        :param SN_Level: Флаг, указывающий, включен ли уровень SN
        :return: Список словарей с остатками и ценами на товары
        '''
        self.ensure_connection()  # Проверяем соединение перед запросом
        try:
            result = self.client.service.getPricesAndRests(GUID_Store=id_warehouse, AllGoods=True, SN_Level=SN_Level)
            return json.loads(result)
        except Fault as e:
            raise ValueError(f"Ошибка запроса SOAP: {e}")
    

    def goods_stock(self, ar_product_1c: list) -> List[Dict[str, Any]]: # Получение остатков по id товара
        try:
            self.ensure_connection()  # Проверяем соединение перед запросом
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



    def stores(self) -> List[Dict[str, Any]]:
        try:
            self.ensure_connection()  # Проверяем соединение перед запросом
            result = self.client.service.getStoresList()
            return json.loads(result)
        except Fault as e:
            raise ValueError(f"Ошибка запроса SOAP: {e}")

    def dict_shops(self, data: List[Dict[str, Any]], res_dict: Dict[str, str] = None) -> Dict[str, str]:
        if res_dict is None:
            res_dict = {}
        for shop in data:
            sub_shops = shop.get('Подчиненные')
            if sub_shops:
                self.dict_shops(sub_shops, res_dict)
            else:
                res_dict[shop['Наименование']] = shop['Ссылка']
        return res_dict
    
    def stock_to_df(self, data: List[Dict[str, Any]]) -> pd.DataFrame:
        df = pd.DataFrame(data)
        # удаляем все строки где остаток равен 0 и Артикул равен None
        df = df[(df['КоличествоОстаток'] != 0) & (df['Артикул'] != None)]
        # удаляем все строки где цена меньше 10000
        df = df[df['Цена'] > 10000]
        return df.head()

if __name__ == "__main__":
    data_1c = Data_1c()
    stock = data_1c.stock('ed20a1c7-8f55-11e6-8230-005056b4177e', SN_Level=False)
    for item in stock:
        if item.get('Цена') > 20000:
            print(item)
    # df = data_1c.stock_to_df(stock)

