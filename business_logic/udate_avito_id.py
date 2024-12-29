from db.db_handler import DatabaseHandler
from avito_api import AvitoAPIClient
from data import accounts


def update_avito_ids(account: dict):
    account_name = account.get('key')
    client_id = account.get('client_id')
    client_secret = account.get('client_secret')
    # Инициализация обработчика базы данных и клиента Avito API
    db_handler = DatabaseHandler()
    client = AvitoAPIClient(client_id, client_secret)

    # Получаем все ID из базы данных
    df_id = db_handler.get_avito_items(account_name)

    # Список для хранения ID
    id_list = [id['Id'] for index, id in df_id.iterrows()]

    # Разбиваем список ID на чанки по 100 элементов
    chunks = [id_list[i:i + 100] for i in range(0, len(id_list), 100)]

    # Проходим по каждому чанку и делаем запрос к API
    for chunk in chunks:
        ids_str = '|'.join(chunk)
        report_items = client.autoload.get_report_items_idMobicom(ids_str)
        
        # Обрабатываем каждый элемент из полученного отчета
        for item in report_items.get("items", []):
            ad_id = item.get("ad_id")
            avito_id = item.get("avito_id") if item.get("avito_status") == "active" else None
            
            # Обновляем запись в базе данных
            db_handler.update_record(account_name, {'Id': ad_id, 'AvitoId': avito_id})

if __name__ == "__main__":
    account = accounts[0]
    update_avito_ids(account)