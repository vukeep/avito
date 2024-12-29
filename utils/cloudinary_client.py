import cloudinary.api as api_client
import cloudinary
import os
from dotenv import load_dotenv
from utils.logger import get_logger

logger = get_logger("Cloudinary")

# Load environment variables
load_dotenv()

class CloudinaryClient:
    def __init__(self):
        """
        Конфигурация Cloudinary.
        """
        cloudinary.config(
            cloud_name=os.getenv("cloud_name"),
            api_key=os.getenv("cloud_api_key"),
            api_secret=os.getenv("cloud_api_secret"),
            secure=True
        )

    def get_photo_urls(self, folder: str) -> list:
        """
        Получение всех URL фотографий из папки Cloudinary.
        """
        try:
            resources = api_client.resources(type="upload", prefix=folder, max_results=500)
            return [resource["url"] for resource in resources["resources"]]
        except Exception as e:
            logger.error(f"Ошибка получения фотографий из папки {folder}: {e}")
            return []

    def url_to_string(self, folder: str) -> str:
        """
        Преобразование URL фотографий в одну строку, разделенную ' | '.
        """
        photo_urls = self.get_photo_urls(folder)[:10]
        return ' | '.join(photo_urls) if photo_urls else ''
