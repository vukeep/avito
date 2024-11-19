# /utils/request_handler.py
import requests
import json
class RequestHandler:
    @staticmethod
    def send_request(url, method="GET", headers=None, data=None, params=None):
        try:
            # Преобразование метода в верхний регистр для корректности
            method = method.upper()
            # GET-запросы используют параметры, остальные — тело запроса
            if method == "GET":
                response = requests.get(url, headers=headers, params=params, timeout=30)
            elif method in ["POST", "PUT"]:
                response = requests.request(method, url, headers=headers, json=data, params=params, timeout=30)
            else:
                raise ValueError(f"HTTP method {method} is not supported.")

            # Проверяем статус-код и возвращаем ответ
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as http_err:
            text = f"HTTP error occurred: {http_err}"
        except requests.exceptions.RequestException as req_err:
            text = f"Request error: {req_err}"
        except json.decoder.JSONDecodeError as json_err:
            text = f"Error decoding JSON: {json_err}"
            return response.text  # Можно вернуть текстовый ответ вместо JSON
        except ValueError as val_err:
            text = f"Value error: {val_err}"
        except Exception as e:
            text = f"Unexpected error: {e}"
        
        return text