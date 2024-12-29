# api_client.py
from .auth.authentication import Authentication
from .autoload.autoload_client import AutoloadClient
from .item.item_client import ItemClient
from .user.user_client import UserClient
from .services_item.services_client import ServicesClient
from .messenger.messenger_client import MessengerClient

class AvitoAPIClient:
    def __init__(self, client_id, client_secret):
        # Инициализируем аутентификацию
        self.auth = Authentication(client_id, client_secret)
        # Инициализируем клиенты для каждого блока методов
        self.autoload = AutoloadClient(self.auth)
        self.item = ItemClient(self.auth)
        self.user = UserClient(self.auth)
        self.services = ServicesClient(self.auth)
        self.messenger = MessengerClient(self.auth)