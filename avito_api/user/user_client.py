# /user/user_client.py

from utils.request_handler import RequestHandler
from config.settings import API_BASE_URL

class UserClient:
    def __init__(self, auth):
        self.auth = auth

    # def для core/v1/accounts/operations_history/ POST
    def get_operations_history(self, date_from, date_to):
        """
        Получение истории операций пользователя (списания/пополнения кошелька).
        :param date_from: Время выборки от (не более одного года в прошлое)
        :param date_to: Время выборки до (диапазон не более недели)
        :return: История операций или None в случае ошибки
        """
        url = f"{API_BASE_URL}/core/v1/accounts/operations_history/"
        headers = self.auth.get_headers()
        data = {
            "dateTimeFrom": date_from,
            "dateTimeTo": date_to
        }
        return RequestHandler.send_request(url, method="POST", headers=headers, data=data)

    # def для core/v1/accounts/self GET
    def get_user_info(self):
        """
        Получение информации об авторизованном пользователе.
        :return: Информация о пользователе или None в случае ошибки
        """
        url = f"{API_BASE_URL}/core/v1/accounts/self"
        headers = self.auth.get_headers()
        return RequestHandler.send_request(url, method="GET", headers=headers)

    # def для core/v1/accounts/{user_id}/balance/ GET
    def get_user_balance(self, user_id):
        """
        Получение баланса кошелька пользователя (реальные деньги и бонусы).
        :param user_id: Идентификатор пользователя
        :return: Баланс пользователя или None в случае ошибки
        """
        url = f"{API_BASE_URL}/core/v1/accounts/{user_id}/balance/"
        headers = self.auth.get_headers()
        return RequestHandler.send_request(url, method="GET", headers=headers)