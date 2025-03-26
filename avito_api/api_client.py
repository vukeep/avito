# api_client.py
from .auth.authentication import Authentication
from .autoload.autoload_client import AutoloadClient
from .item.item_client import ItemClient
from .user.user_client import UserClient
from .services_item.services_client import ServicesClient
from .messenger.messenger_client import MessengerClient
import logging

# Получаем логгер
logger = logging.getLogger('avito_api')

class AvitoAPIClient:
    def __init__(self, client_id=None, client_secret=None, access_token=None, token_expires_at=None):
        """
        Инициализация клиента API Avito
        
        Args:
            client_id (str): ID клиента для авторизации
            client_secret (str): Секретный ключ клиента
            access_token (str): Существующий токен доступа
            token_expires_at (int): Время истечения токена (timestamp)
        """
        # Инициализируем аутентификацию
        self.auth = Authentication(
            client_id=client_id, 
            client_secret=client_secret,
            access_token=access_token,
            token_expires_at=token_expires_at
        )
        
        # Если токен был обновлен при инициализации, логируем это
        if self.auth.token_refreshed:
            logger.info("Токен был обновлен при инициализации клиента")
        
        # Инициализируем клиенты для каждого блока методов
        self.autoload = AutoloadClient(self.auth)
        self.item = ItemClient(self.auth)
        self.user = UserClient(self.auth)
        self.services = ServicesClient(self.auth)
        self.messenger = MessengerClient(self.auth)
