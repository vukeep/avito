# /messenger/messenger_client.py

from ..utils.request_handler import RequestHandler
from ..config.settings import API_BASE_URL

class MessengerClient:
    def __init__(self, auth):
        self.auth = auth

    def get_chats(self, user_id, item_ids=None, unread_only=False, chat_types="u2i", limit=100, offset=0):
        """
        Получение списка чатов пользователя.
        
        Args:
            user_id (int): ID пользователя
            item_ids (list, optional): Список ID объявлений для фильтрации
            unread_only (bool): Только непрочитанные чаты
            chat_types (str): Тип чатов (u2i - по объявлениям, u2u - между пользователями)
            limit (int): Количество чатов на странице (макс. 100)
            offset (int): Смещение от начала списка
        
        Returns:
            dict: Информация о чатах
        """
        url = f"{API_BASE_URL}/messenger/v2/accounts/{user_id}/chats"
        params = {
            "item_ids": ','.join(map(str, item_ids)) if item_ids else None,
            "unread_only": str(unread_only).lower(),  # Преобразуем в 'true' или 'false'
            "chat_types": chat_types,
            "limit": limit,
            "offset": offset
        }
        # Удаляем None значения
        params = {k: v for k, v in params.items() if v is not None}
        
        headers = self.auth.get_headers()
        return RequestHandler.send_request(url, method="GET", headers=headers, params=params)

    def get_chat(self, user_id, chat_id):
        """
        Получение информации по конкретному чату.
        
        Args:
            user_id (int): ID пользователя
            chat_id (str): ID чата
            
        Returns:
            dict: Информация о чате
        """
        url = f"{API_BASE_URL}/messenger/v2/accounts/{user_id}/chats/{chat_id}"
        headers = self.auth.get_headers()
        return RequestHandler.send_request(url, method="GET", headers=headers)

    def get_messages(self, user_id, chat_id, limit=100, offset=0):
        """
        Получение списка сообщений в чате.
        
        Args:
            user_id (int): ID пользователя
            chat_id (str): ID чата
            limit (int): Количество сообщений (макс. 100)
            offset (int): Смещение от начала списка
            
        Returns:
            list: Список сообщений
        """
        url = f"{API_BASE_URL}/messenger/v3/accounts/{user_id}/chats/{chat_id}/messages/"
        params = {
            "limit": limit,
            "offset": offset
        }
        headers = self.auth.get_headers()
        return RequestHandler.send_request(url, method="GET", headers=headers, params=params)

    def send_message(self, user_id, chat_id, data):
        """
        Отправка текстового сообщения в чат.
        
        Args:
            user_id (int): ID пользователя
            chat_id (str): ID чата
            text (str): Текст сообщения
            data = {
                "message": {"text": text},
                "type": "text"
            }
            
        Returns:
            dict: Информация об отправленном сообщении
        """
        url = f"{API_BASE_URL}/messenger/v1/accounts/{user_id}/chats/{chat_id}/messages"

        headers = self.auth.get_headers()
        return RequestHandler.send_request(url, method="POST", headers=headers, data=data)

    def send_image_message(self, user_id, chat_id, image_id):
        """
        Отправка сообщения с изображением.
        
        Args:
            user_id (int): ID пользователя
            chat_id (str): ID чата
            image_id (str): ID загруженного изображения
            
        Returns:
            dict: Информация об отправленном сообщении
        """
        url = f"{API_BASE_URL}/messenger/v1/accounts/{user_id}/chats/{chat_id}/messages/image"
        data = {
            "image_id": image_id
        }
        headers = self.auth.get_headers()
        return RequestHandler.send_request(url, method="POST", headers=headers, data=data)

    def upload_image(self, user_id, image_file):
        """
        Загрузка изображения для отправки в чат.
        
        Args:
            user_id (int): ID пользователя
            image_file (file): Файл изображения
            
        Returns:
            dict: Информация о загруженном изображении
        """
        url = f"{API_BASE_URL}/messenger/v1/accounts/{user_id}/uploadImages"
        files = {
            'uploadfile[]': image_file
        }
        headers = self.auth.get_headers()
        return RequestHandler.send_request(url, method="POST", headers=headers, files=files)

    def mark_chat_as_read(self, user_id, chat_id):
        """
        Пометить чат как прочитанный.
        
        Args:
            user_id (int): ID пользователя
            chat_id (str): ID чата
            
        Returns:
            dict: Результат операции
        """
        url = f"{API_BASE_URL}/messenger/v1/accounts/{user_id}/chats/{chat_id}/read"
        headers = self.auth.get_headers()
        return RequestHandler.send_request(url, method="POST", headers=headers)

    def delete_message(self, user_id, chat_id, message_id):
        """
        Удаление сообщения из чата.
        
        Args:
            user_id (int): ID пользователя
            chat_id (str): ID чата
            message_id (str): ID сообщения
            
        Returns:
            dict: Результат операции
        """
        url = f"{API_BASE_URL}/messenger/v1/accounts/{user_id}/chats/{chat_id}/messages/{message_id}"
        headers = self.auth.get_headers()
        return RequestHandler.send_request(url, method="POST", headers=headers)

    def get_voice_files(self, user_id, voice_ids):
        """
        Получение ссылок на голосовые сообщения.
        
        Args:
            user_id (int): ID пользователя
            voice_ids (list): Список ID голосовых сообщений
            
        Returns:
            dict: Словарь с ссылками на голосовые сообщения
        """
        url = f"{API_BASE_URL}/messenger/v1/accounts/{user_id}/getVoiceFiles"
        params = {
            "voice_ids": ','.join(voice_ids)
        }
        headers = self.auth.get_headers()
        return RequestHandler.send_request(url, method="GET", headers=headers, params=params)
    
    def get_subscriptions(self):
        """
        Получение списка подписок на webhook-уведомления.
        
        Returns:
            dict: Список активных подписок на уведомления
        """
        url = f"{API_BASE_URL}/messenger/v1/subscriptions"
        headers = self.auth.get_headers()
        return RequestHandler.send_request(url, method="POST", headers=headers)
