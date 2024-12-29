# /default/default_client.py

from ..utils.request_handler import RequestHandler
from ..config.settings import API_BASE_URL

class ServicesClient:
    def __init__(self, auth):
        self.auth = auth

    def update_price(self, item_id, price):
        """
        Обновление цены объявления по его идентификатору (item_id).

        :param item_id: Идентификатор объявления
        :param price: Новая цена
        :return: Результат обновления цены или None в случае ошибки
        """
        url = f"{API_BASE_URL}/core/v1/items/{item_id}/update_price"

        # Тело запроса
        data = {
            "price": price
        }

        # Выполнение запроса
        headers = self.auth.get_headers()
        return RequestHandler.send_request(url, method="POST", headers=headers, data=data)
    
    def update_quantity(self, avito_id, quantity):
        """
        Обновление количества товара по его идентификатору (external_id, item_id, quantity).
        [   
            {
                "external_id": "AB123456",
                "item_id": 123321,
                "quantity": 500
            }
        ]
        :param stock: Список с данными для обновления количества
        :return: Результат обновления количества или None в случае ошибки
        """
        url = f"{API_BASE_URL}/stock-management/1/stocks"

        # Тело запроса
        data = {
            "item_id": avito_id,
            "stocks": quantity
        }

        # Выполнение запроса
        headers = self.auth.get_headers()
        return RequestHandler.send_request(url, method="PUT", headers=headers, data=data)