# /default/default_client.py

from utils.request_handler import RequestHandler
from config.settings import API_BASE_URL

class DefaultClient:
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