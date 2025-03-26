# /utils/request_handler.py
import requests
import json
import logging
from ..config.settings import TIMEOUT

# Настройка логирования
logger = logging.getLogger('avito_api')

class RequestHandler:
    @staticmethod
    def send_request(url, method="GET", headers=None, data=None, params=None, files=None):
        """
        Отправляет HTTP запрос и обрабатывает ответ
        
        Args:
            url (str): URL для отправки запроса
            method (str): HTTP метод (GET, POST, PUT, DELETE)
            headers (dict): Заголовки запроса
            data (dict): Данные для отправки в теле запроса
            params (dict): Параметры запроса для URL
            files (dict): Файлы для загрузки
            
        Returns:
            dict: Данные ответа в формате JSON или None в случае ошибки
        """
        try:
            # Добавляем информацию о запросе в лог для отладки
            logger.debug(f"Sending {method} request to {url}")
            if params:
                logger.debug(f"Params: {json.dumps(params, ensure_ascii=False)}")
            if data:
                logger.debug(f"Data: {json.dumps(data, ensure_ascii=False)}")
            
            # Выполняем запрос
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=data if method in ["POST", "PUT", "PATCH"] and not files else None,
                params=params if method == "GET" or params else None,
                files=files,
                timeout=TIMEOUT
            )
            
            # Проверяем статус ответа
            response.raise_for_status()
            
            # Возвращаем данные в формате JSON
            if response.content:
                return response.json()
            else:
                return {"status": "success"}
                
        except requests.exceptions.HTTPError as e:
            # Ошибки HTTP (4xx, 5xx)
            error_msg = f"HTTP Error: {e.response.status_code} - {e.response.reason}"
            logger.error(error_msg)
            
            # Пытаемся получить детали ошибки из тела ответа
            try:
                error_details = e.response.json()
                logger.error(f"Error details: {json.dumps(error_details, ensure_ascii=False)}")
                return {"error": error_msg, "details": error_details, "status_code": e.response.status_code}
            except:
                return {"error": error_msg, "status_code": e.response.status_code}
                
        except requests.exceptions.ConnectionError as e:
            # Ошибки соединения
            error_msg = f"Connection Error: {str(e)}"
            logger.error(error_msg)
            return {"error": error_msg}
            
        except requests.exceptions.Timeout as e:
            # Таймаут запроса
            error_msg = f"Timeout Error: {str(e)}"
            logger.error(error_msg)
            return {"error": error_msg}
            
        except requests.exceptions.RequestException as e:
            # Другие ошибки запросов
            error_msg = f"Request Error: {str(e)}"
            logger.error(error_msg)
            return {"error": error_msg}
            
        except Exception as e:
            # Непредвиденные ошибки
            error_msg = f"Unexpected Error: {str(e)}"
            logger.error(error_msg)
            return {"error": error_msg}