# /auth/authentication.py

import requests
import time
import logging

# Получаем логгер
logger = logging.getLogger('avito_api')

class Authentication:
    def __init__(self, client_id=None, client_secret=None, access_token=None, token_expires_at=None):
        '''
        Инициализация класса Authentication
        
        Args:
            client_id (str): ID клиента для авторизации
            client_secret (str): Секретный ключ клиента
            access_token (str): Существующий токен доступа
            token_expires_at (int): Время истечения токена в формате timestamp
        '''
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.token_expires_at = token_expires_at
        
        # Флаг обновления токена
        self.token_refreshed = False
        
        # Проверяем токен при инициализации
        self._initialize_token()
    
    def _initialize_token(self):
        """
        Инициализирует или проверяет токен при создании объекта
        """
        # Если токен предоставлен, проверяем его валидность
        if self.access_token:
            if not self._validate_token():
                # Если токен невалиден и есть client_id/client_secret, получаем новый
                if self.client_id and self.client_secret:
                    self._create_token()
        # Если токен не предоставлен, но есть учетные данные
        elif self.client_id and self.client_secret:
            self._create_token()
    
    def _validate_token(self):
        """
        Проверяет валидность токена через тестовый запрос к API
        
        Returns:
            bool: True если токен валиден, False если нет
        """
        if not self.access_token:
            return False
            
        # URL для проверки валидности токена
        url = "https://api.avito.ru/core/v1/accounts/self"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            # Если токен валиден
            if response.status_code == 200:
                # Если не знаем время истечения, устанавливаем примерное (24 часа)
                if self.token_expires_at is None:
                    self.token_expires_at = int(time.time()) + 86400
                return True
            
            # Если ошибка авторизации
            elif response.status_code in [401, 403]:
                return False
            
            # Другие ошибки считаем не связанными с токеном
            else:
                return True
                
        except requests.exceptions.RequestException:
            # При ошибке сети считаем токен валидным
            return True

    def get_headers(self):
        """
        Возвращает заголовки для запросов с проверкой актуальности токена
        
        Returns:
            dict: Заголовки для запроса
        """
        # Проверяем срок действия токена
        self._ensure_valid_token()
        
        # Возвращаем заголовки
        return {"Authorization": f"Bearer {self.access_token}"}
    
    def _ensure_valid_token(self):
        """
        Проверяет срок действия токена и обновляет при необходимости
        """
        # Если нет токена, пытаемся получить новый
        if not self.access_token and self.client_id and self.client_secret:
            self._create_token()
            return
            
        # Проверяем срок действия токена (если он известен)
        current_time = int(time.time())
        if self.token_expires_at and current_time > self.token_expires_at - 300:
            # Если client_id и client_secret доступны, создаем новый токен
            if self.client_id and self.client_secret:
                self._create_token()
    
    def _create_token(self):
        """
        Создает новый токен доступа используя client credentials
        
        Returns:
            str: Новый токен доступа
        """
        if not (self.client_id and self.client_secret):
            raise ValueError("client_id и client_secret требуются для создания токена")
            
        url = "https://api.avito.ru/token/"
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

        response = requests.post(url, data=data)
        if response.status_code == 200:
            response_data = response.json()
            self.access_token = response_data.get("access_token")
            # Стандартное время жизни токена - 24 часа
            self.token_expires_at = int(time.time()) + 86400
            self.token_refreshed = True
            logger.info("Новый токен успешно получен")
            return self.access_token
        else:
            logger.error(f"Ошибка при получении токена: {response.status_code} - {response.text}")
            raise Exception(f"Ошибка при получении токена: {response.status_code} - {response.text}")
