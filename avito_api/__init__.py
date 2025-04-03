"""
Пакет Avito API - клиент для работы с API Avito
Оптимизирован для быстрой интеграции и высокой производительности
"""

from .api_client import AvitoAPIClient

# Экспортируем основной класс для удобного импорта
__all__ = ['AvitoAPIClient']  # Также меняем здесь

# Версия пакета
__version__ = '1.1.0'

# Настройка логирования
import logging

# Создаем логгер
logger = logging.getLogger('avito_api')
logger.setLevel(logging.INFO)

# Если обработчики еще не настроены, добавляем базовый обработчик
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)