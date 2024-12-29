import cloudinary.api as api_client
import cloudinary
import os
from dotenv import load_dotenv
from utils.logger import get_logger

logger = get_logger("Cloudinary")

# Загрузка переменных окружения
load_dotenv()

class CloudinaryClient:
    def __init__(self):
        # Конфигурация Cloudinary
        cloudinary.config(
            cloud_name=os.getenv("cloud_name"),
            api_key=os.getenv("cloud_api_key"),
            api_secret=os.getenv("cloud_api_secret"),
            secure=True
        )

    # Получение всех URL фотографий из папки
    def get_photo_urls(self, folder):
        try:
            resources = api_client.resources(type="upload", prefix=folder, max_results=500)
            photo_urls = [resource["url"] for resource in resources["resources"]]
            photo_urls.sort()
            return photo_urls
        except Exception as e:
            logger.error(f"Ошибка при получении фото из папки {folder}: {e}")
            return []
        
    def url_to_string(self, folder):
        photo_urls = self.get_photo_urls(folder)[:10] # Получаем список URL фотографий и ограничиваем первыми 10 значениями
        if photo_urls:
            return ' | '.join(photo_urls) # Преобразуем список URL в строку
        else:
            return ''


if __name__ == "__main__":
    folder = "210839759"
    # Вывод URL фотографий
    photo_urls = CloudinaryClient().get_photo_urls(folder)
    print("URL фотографий:")
    for url in photo_urls:
        print(url)