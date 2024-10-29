# /auth/authentication.py
class Authentication:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_headers(self):
        # Возвращает заголовки для каждого запроса
        return {"Authorization": f"Bearer {self.api_key}"}