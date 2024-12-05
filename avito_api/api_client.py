# api_client.py
from .auth.authentication import Authentication
from .autoload.autoload_client import AutoloadClient
from .item.item_client import ItemClient
from .user.user_client import UserClient
from .default.default_client import DefaultClient

class AvitoAPIClient:
    def __init__(self, client_id, client_secret):
        # Инициализируем аутентификацию
        self.auth = Authentication(client_id, client_secret)
        # Инициализируем клиенты для каждого блока методов
        self.autoload = AutoloadClient(self.auth)
        self.item = ItemClient(self.auth)
        self.user = UserClient(self.auth)
        self.default = DefaultClient(self.auth)