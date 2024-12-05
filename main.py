# Пример тестирования метода
from avito_api.api_client import AvitoAPIClient
from modules.cloudinary_client import get_photo_urls
from modules.article_properties import MobicomAPI
#from modules.sql_goods import fetch_products

import requests
import pandas as pd

import os
import dotenv

dotenv.load_dotenv()

client_id = os.getenv("Client_id_iSmartChita")
client_secret = os.getenv("Client_secret_iSmartChita")

def save_report_to_excel(client, report_id):
    """
    Сохраняет все позиции отчета в Excel файл
    
    Args:
        client: экземпляр AvitoAPIClient
        report_id: ID отчета для выгрузки
    
    Returns:
        str: Путь к сохраненному файлу
    """
    # Получаем первую страницу для определения общего количества элементов
    initial_response = client.autoload.get_report_items(
        report_id=report_id,
        page=0,
        sections=None
    )

    total_items = initial_response.get('meta', {}).get('total')
    total_pages = initial_response.get('meta', {}).get('pages')

    print(f"Всего элементов: {total_items}, страниц: {total_pages}")

    # Собираем все items со всех страниц
    all_items = []
    all_items.extend(initial_response.get('items', []))

    # Проходим по остальным страницам
    for page in range(1, total_pages):
        response = client.autoload.get_report_items(
            report_id=report_id,
            page=page,
            sections=None
        )
        items = response.get('items', [])
        all_items.extend(items)
        print(f"Обработана страница {page + 1} из {total_pages}")

    # Создаем DataFrame из собранных данных
    df = pd.DataFrame(all_items)

    # Сохраняем в Excel
    output_file = f'report_{report_id}.xlsx'
    df.to_excel(output_file, index=False)
    print(f"Данные сохранены в файл: {output_file}")
    
    return output_file

# Пример использования:
if __name__ == "__main__":
    client = AvitoAPIClient(client_id, client_secret)
    report_id = 296747312
    saved_file = save_report_to_excel(client, report_id)
    #user_info = client.user.get_user_info()

    #user_balance = client.user.get_user_balance(user_id=251411026)

    # Получение истории операций
    '''operations_history = client.user.get_operations_history(
        date_from="2024-09-01T00:00:00",
        date_to="2024-10-07T00:00:00"
    )

    last_completed = client.autoload.get_last_completed_report()

    # Печатаем результат
    print(last_completed)'''



