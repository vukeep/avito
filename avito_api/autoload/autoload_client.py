# /autoload/autoload_client.py

from utils.request_handler import RequestHandler
from config.settings import API_BASE_URL

class AutoloadClient:
    def __init__(self, auth):
        self.auth = auth

    # def для autoload/v2/reports/{report_id}/items GET
    def get_report_items(self, report_id, per_page=50, page=0, query=None, sections=None):
        """
        Получение списка объявлений по идентификатору отчёта (report_id).

        :param report_id: ID отчёта
        :param per_page: Количество объявлений на странице (по умолчанию 50)
        :param page: Номер страницы (по умолчанию 0)
        :param query: Фильтр по ID объявления
        :param sections: Фильтр по разделам
        :return: Список объявлений или None в случае ошибки
        """
        url = f"{API_BASE_URL}/autoload/v2/reports/{report_id}/items"

        # Параметры запроса
        params = {
            "per_page": per_page,
            "page": page,
            "query": query,
            "sections": sections
        }

        # Очищаем параметры с None значениями
        params = {k: v for k, v in params.items() if v is not None}

        # Выполнение запроса
        headers = self.auth.get_headers()
        return RequestHandler.send_request(url, method="GET", headers=headers, params=params)

    # def для autoload/v1/profile GET
    def get_profile(self):
        """
        Получение профиля автозагрузки.
        :return: Профиль или None в случае ошибки
        """
        url = f"{API_BASE_URL}/autoload/v1/profile"
        headers = self.auth.get_headers()
        return RequestHandler.send_request(url, method="GET", headers=headers)

    # def для autoload/v1/profile POST
    def create_or_update_profile(self, profile_data):
        """
        Создание/редактирование профиля автозагрузки.
        :param profile_data: Данные профиля для создания или обновления
        :return: Результат операции или None в случае ошибки
        """
        url = f"{API_BASE_URL}/autoload/v1/profile"
        headers = self.auth.get_headers()
        return RequestHandler.send_request(url, method="POST", headers=headers, data=profile_data)

    # def для autoload/v1/upload POST
    def upload_file(self):
        """
        Запуск загрузки файла по ссылке, указанной в профиле.
        :return: Результат операции или None в случае ошибки
        """
        url = f"{API_BASE_URL}/autoload/v1/upload"
        headers = self.auth.get_headers()
        return RequestHandler.send_request(url, method="POST", headers=headers)

    # def для autoload/v2/items/ad_ids GET
    def get_ad_ids_by_avito_ids(self, query):
        """
        Получение ID объявлений из файла по ID объявлений на Авито.
        :param query: Идентификаторы объявлений на Авито, разделённые запятой или через "|"
        :return: Список объявлений или None в случае ошибки
        """
        url = f"{API_BASE_URL}/autoload/v2/items/ad_ids"
        headers = self.auth.get_headers()
        params = {"query": query}
        return RequestHandler.send_request(url, method="GET", headers=headers, params=params)

    # def для autoload/v2/items/avito_ids GET
    def get_avito_ids_by_ad_ids(self, query):
        """
        Получение ID объявлений на Авито по ID объявлений из файла.
        :param query: Идентификаторы объявлений из файла, разделённые запятой или через "|"
        :return: Список объявлений или None в случае ошибки
        """
        url = f"{API_BASE_URL}/autoload/v2/items/avito_ids"
        headers = self.auth.get_headers()
        params = {"query": query}
        return RequestHandler.send_request(url, method="GET", headers=headers, params=params)

    # def для autoload/v2/reports GET
    def get_reports(self, per_page=50, page=0, date_from=None, date_to=None):
        """
        Получение списка отчетов автозагрузки.
        :param per_page: Количество отчетов на странице
        :param page: Номер страницы
        :param date_from: Фильтр по дате создания "от"
        :param date_to: Фильтр по дате создания "до"
        :return: Список отчетов или None в случае ошибки
        """
        url = f"{API_BASE_URL}/autoload/v2/reports"
        headers = self.auth.get_headers()
        params = {
            "per_page": per_page,
            "page": page,
            "date_from": date_from,
            "date_to": date_to,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return RequestHandler.send_request(url, method="GET", headers=headers, params=params)

    # def для autoload/v2/reports/items GET
    def get_report_items(self, report_id, per_page=50, page=0, query=None, sections=None):
        """
        Получение списка объявлений по идентификатору отчёта.
        :param report_id: ID отчёта
        :param per_page: Количество объявлений на странице
        :param page: Номер страницы
        :param query: Фильтр по ID объявления
        :param sections: Фильтр по разделам
        :return: Список объявлений или None в случае ошибки
        """
        url = f"{API_BASE_URL}/autoload/v2/reports/{report_id}/items"
        headers = self.auth.get_headers()
        params = {
            "per_page": per_page,
            "page": page,
            "query": query,
            "sections": sections,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return RequestHandler.send_request(url, method="GET", headers=headers, params=params)

    # def для autoload/v2/reports/last_completed_report GET
    def get_last_completed_report(self):
        """
        Получение статистики по последней завершённой выгрузке.
        :return: Статистика или None в случае ошибки
        """
        url = f"{API_BASE_URL}/autoload/v2/reports/last_completed_report"
        headers = self.auth.get_headers()
        return RequestHandler.send_request(url, method="GET", headers=headers)

    # def для autoload/v2/reports/{report_id} GET
    def get_report_by_id(self, report_id):
        """
        Получение статистики по конкретной выгрузке.
        :param report_id: ID отчёта
        :return: Статистика или None в случае ошибки
        """
        url = f"{API_BASE_URL}/autoload/v2/reports/{report_id}"
        headers = self.auth.get_headers()
        return RequestHandler.send_request(url, method="GET", headers=headers)

    # def для autoload/v2/reports/{report_id}/items/fees GET
    def get_report_items_fees(self, report_id, per_page=100, page=0):
        """
        Получение информации о списаниях за размещение каждого объявления в конкретной выгрузке.
        :param report_id: ID отчёта
        :param per_page: Количество объявлений на странице
        :param page: Номер страницы
        :return: Информация о списаниях или None в случае ошибки
        """
        url = f"{API_BASE_URL}/autoload/v2/reports/{report_id}/items/fees"
        headers = self.auth.get_headers()
        params = {
            "per_page": per_page,
            "page": page,
        }
        return RequestHandler.send_request(url, method="GET", headers=headers, params=params)