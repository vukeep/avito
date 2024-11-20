# /item/item_client.py

from ..utils.request_handler import RequestHandler
from ..config.settings import API_BASE_URL

class ItemClient:
    def __init__(self, auth):
        self.auth = auth

    # def для core/v1/accounts/{userId}/vas/prices POST
    def get_vas_prices(self, user_id, item_ids):
        """
        Получение информации о стоимости услуг продвижения и доступных значках.
        :param user_id: Идентификатор пользователя
        :param item_ids: Список идентификаторов объявлений
        :return: Информация о стоимости услуг или None в случае ошибки
        """
        url = f"{API_BASE_URL}/core/v1/accounts/{user_id}/vas/prices"
        headers = self.auth.get_headers()
        data = {
            "itemIds": item_ids
        }
        return RequestHandler.send_request(url, method="POST", headers=headers, data=data)

    # def для core/v1/accounts/{user_id}/calls/stats/ POST
    def get_calls_stats(self, user_id, date_from, date_to, item_ids):
        """
        Получение агрегированной статистики звонков, полученных пользователем.
        :param user_id: Идентификатор пользователя
        :param date_from: Начальная дата периода
        :param date_to: Конечная дата периода
        :param item_ids: Список идентификаторов объявлений
        :return: Статистика звонков или None в случае ошибки
        """
        url = f"{API_BASE_URL}/core/v1/accounts/{user_id}/calls/stats/"
        headers = self.auth.get_headers()
        data = {
            "dateFrom": date_from,
            "dateTo": date_to,
            "itemIds": item_ids
        }
        return RequestHandler.send_request(url, method="POST", headers=headers, data=data)

    # def для core/v1/accounts/{user_id}/items/{item_id}/ GET
    def get_item_info(self, user_id, item_id):
        """
        Получение информации по объявлению (статус, примененные услуги).
        :param user_id: Идентификатор пользователя
        :param item_id: Идентификатор объявления
        :return: Информация об объявлении или None в случае ошибки
        """
        url = f"{API_BASE_URL}/core/v1/accounts/{user_id}/items/{item_id}/"
        headers = self.auth.get_headers()
        return RequestHandler.send_request(url, method="GET", headers=headers)

    # def для core/v1/items GET
    def get_items_info(self, per_page=25, page=1, status=None, updated_at_from=None, category=None):
        """
        Получение списка объявлений пользователя.
        :param per_page: Количество объявлений на странице
        :param page: Номер страницы
        :param status: Фильтр по статусу объявлений
        :param updated_at_from: Фильтр по дате обновления
        :param category: Фильтр по категории
        :return: Список объявлений или None в случае ошибки
        """
        url = f"{API_BASE_URL}/core/v1/items"
        headers = self.auth.get_headers()
        params = {
            "per_page": per_page,
            "page": page,
            "status": status,
            "updatedAtFrom": updated_at_from,
            "category": category
        }
        params = {k: v for k, v in params.items() if v is not None}
        return RequestHandler.send_request(url, method="GET", headers=headers, params=params)

    # def для core/v2/accounts/{user_id}/items/{item_id}/vas_packages PUT
    def apply_vas_package(self, user_id, item_id, package_id):
        """
        Применение пакета дополнительных услуг к объявлению.
        :param user_id: Идентификатор пользователя
        :param item_id: Идентификатор объявления
        :param package_id: Идентификатор пакета услуг
        :return: Информация о примененной услуге или None в случае ошибки
        """
        url = f"{API_BASE_URL}/core/v2/accounts/{user_id}/items/{item_id}/vas_packages"
        headers = self.auth.get_headers()
        data = {
            "package_id": package_id
        }
        return RequestHandler.send_request(url, method="PUT", headers=headers, data=data)

    # def для core/v2/items/{itemId}/vas/ PUT
    def apply_vas(self, item_id, slugs, stickers=None):
        """
        Применение услуг продвижения к объявлению.
        :param item_id: Идентификатор объявления
        :param slugs: Список идентификаторов услуг
        :param stickers: Список значков (необязательно)
        :return: Информация о примененных услугах или None в случае ошибки
        """
        url = f"{API_BASE_URL}/core/v2/items/{item_id}/vas/"
        headers = self.auth.get_headers()
        data = {
            "slugs": slugs,
            "stickers": stickers
        }
        data = {k: v for k, v in data.items() if v is not None}
        return RequestHandler.send_request(url, method="PUT", headers=headers, data=data)

    # def для stats/v1/accounts/{user_id}/items POST
    def get_items_stats(self, user_id, date_from, date_to, item_ids, period_grouping="day"):
        """
        Получение статистики по списку объявлений.
        :param user_id: Идентификатор пользователя
        :param date_from: Начальная дата периода
        :param date_to: Конечная дата периода
        :param item_ids: Список идентификаторов объявлений
        :param period_grouping: Период группировки (по умолчанию "day")
        :return: Статистика по объявлениям или None в случае ошибки
        """
        url = f"{API_BASE_URL}/stats/v1/accounts/{user_id}/items"
        headers = self.auth.get_headers()
        data = {
            "dateFrom": date_from,
            "dateTo": date_to,
            "itemIds": item_ids,
            "periodGrouping": period_grouping
        }
        return RequestHandler.send_request(url, method="POST", headers=headers, data=data)