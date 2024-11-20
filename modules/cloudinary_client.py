import cloudinary.api as api_client
import cloudinary
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Конфигурация Cloudinary
cloudinary.config(
    cloud_name=os.getenv("cloud_name"),
    api_key=os.getenv("cloud_api_key"),
    api_secret=os.getenv("cloud_api_secret"),
    secure=True
)

# Получение всех URL фотографий из папки
def get_photo_urls(folder):
    try:
        resources = api_client.resources(type="upload", prefix=folder, max_results=500)
        photo_urls = [resource["url"] for resource in resources["resources"]]
        photo_urls.sort()
        return photo_urls
    except Exception as e:
        print(f"Ошибка при получении фото из папки {folder}: {e}")
        return []

if __name__ == "__main__":
    folder = "210839759"
    # Вывод URL фотографий
    photo_urls = get_photo_urls(folder)
    print("URL фотографий:")
    for url in photo_urls:
        print(url)