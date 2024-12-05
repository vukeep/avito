import os
import dotenv
import requests
import json

dotenv.load_dotenv()

site_login = os.getenv("SITE_LOGIN")
site_password = os.getenv("SITE_PASSWORD")

class MobicomAPI:
    def __init__(self):
        self.base_url = "https://www.mobicom.ru/props"
        self.access_token = None
        self.refresh_token = None
        
    def login(self):
        '''
        Авторизация на сайте mobicom.ru
        '''
        try:
            response = requests.post(
                f"{self.base_url}/auth/login",
                json={
                    "username": site_login,
                    "password": site_password
                }
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "success":
                self.access_token = data["data"]["access_token"]
                self.refresh_token = data["data"]["refresh_token"]
                return True
            return False
        except Exception as e:
            return {"error": str(e)}

    def refresh_tokens(self):
        '''
        Обновление токенов
        '''
        try:
            response = requests.post(
                f"{self.base_url}/auth/refresh",
                json={"refresh_token": self.refresh_token}
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "success":
                self.access_token = data["data"]["access_token"]
                self.refresh_token = data["data"]["refresh_token"]
                return True
            return False
        except Exception as e:
            return {"error": str(e)}

    def get_product_by_article(self, article):
        '''
        Получение информации о товаре по артикулу
        '''
        if not self.access_token:
            login_result = self.login()
            if isinstance(login_result, dict) and "error" in login_result:
                return login_result

        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = requests.get(
                f"{self.base_url}/product-by-article",
                params={"article": article},
                headers=headers
            )

            if response.status_code == 401:
                # Try refreshing token
                refresh_result = self.refresh_tokens()
                if isinstance(refresh_result, dict) and "error" in refresh_result:
                    # If refresh failed, try logging in again
                    login_result = self.login()
                    if isinstance(login_result, dict) and "error" in login_result:
                        return login_result
                
                # Retry request with new token
                headers = {"Authorization": f"Bearer {self.access_token}"}
                response = requests.get(
                    f"{self.base_url}/product-by-article",
                    params={"article": article},
                    headers=headers
                )
            
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            return {"error": str(e)}

if __name__ == '__main__':
    mobicom = MobicomAPI()
    res = mobicom.get_product_by_article('MLP53RU-A')
    print(res)

