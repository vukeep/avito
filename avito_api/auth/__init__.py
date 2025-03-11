"""
Пакет Avito API - клиент для работы с API Avito
Оптимизирован для быстрой интеграции и высокой производительности
"""

from .api_client import AvitoAPIClient  # Было AvitoApiClient, меняем на AvitoAPIClient 
from . import utils
from . import user
from . import services_item
from . import messenger
from . import item
from . import auth

# Экспортируем основной класс для удобного импорта
__all__ = ['AvitoAPIClient']  # Также меняем здесь

# Версия пакета
__version__ = '1.0.0'