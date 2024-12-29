import time
import requests
from typing import Callable
from utils.logger import get_logger

logger = get_logger("API Helpers")

def retry_request(func: Callable, retries: int = 3, delay: int = 5, *args, **kwargs):
    """
    Повторное выполнение функции запроса при неудаче.
    """
    for attempt in range(retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Попытка {attempt + 1} не удалась: {e}")
            time.sleep(delay)
    raise Exception("Превышено максимальное количество попыток")

def handle_api_response(response: requests.Response) -> dict:
    """
    Обрабатывает ответ API, выдавая ошибки при неуспешном статусе.
    """
    if response.status_code == 200:
        return response.json()
    response.raise_for_status()
