from db.db_handler import DatabaseHandler
from utils.logger import get_logger
from avito_api import AvitoAPIClient
import pandas as pd

logger = get_logger("Обновления цен")


def update_prices_in_stores(db_handler: DatabaseHandler, account: dict, price_df: pd.DataFrame):
    
    """
    Обновляет цены в таблице stores для всех совпадений по артикулу.

    :param db_handler: Экземпляр DatabaseHandler для взаимодействия с базой данных.
    :param price_df: DataFrame с новыми ценами, содержащий столбцы 'Артикул' и 'Цена'.
    """
    store_name = account.get('key')
    # Получаем все артикулы и AvitoId из таблицы stores
    stores_df = db_handler.fetch_avito_ids(store=store_name)  # получаем все id и AvitoId из таблицы stores

    # Объединяем DataFrame по артикулу, оставляя только совпадения
    merged_df = pd.merge(stores_df, price_df, left_on='Id', right_on='Артикул', how='inner')

    # Проверяем, что в merged_df остались только записи с совпадениями
    if merged_df.empty:
        logger.info(f"Нет совпадений для обновления цен. Салон {store_name}")
        return

    # Обновляем цены в таблице stores
    for _, row in merged_df.iterrows():
        update_data = {
            'Id': row['Id'],
            'Price': row['Цена']  # Предполагается, что столбец с новой ценой называется 'Цена'
        }
        db_handler.update_record(store=store_name, record_dict=update_data)
    logger.info(f"Цены в таблице stores для {store_name} обновлены {merged_df.shape[0]} строк")

def update_prices_on_avito(db_handler: DatabaseHandler, account: dict, stock_df: pd.DataFrame):
    """
    Обновляет цены на сайте Avito для всех совпадений по артикулу.

    :param db_handler: Экземпляр DatabaseHandler для взаимодействия с базой данных.
    :param store_name: Название магазина.
    :param stock_df: DataFrame с новыми данными, содержащий столбцы 'Артикул' и 'КоличествоОстаток'.
    """
    # Получаем все артикулы и AvitoId из таблицы stores
    stores_df = db_handler.fetch_avito_ids(store=account.get('key'))

    # Объединяем DataFrame по артикулу, оставляя только совпадения
    merged_df = pd.merge(stores_df, stock_df, left_on='Id', right_on='Артикул', how='inner')

    # Фильтруем записи, у которых AvitoId не пустой
    valid_entries = merged_df[merged_df['AvitoId'].notna()]

    # Подготовка данных для API Avito
    avito_data = valid_entries[['AvitoId', 'Цена']].to_dict('records')

    # Обновление цен на Avito через API
    avito_client = AvitoAPIClient(account.get('client_id'), account.get('client_secret'))
    for item in avito_data:
        avito_id = item['AvitoId']
        price = item['Цена']
        if price is None:
            continue
        try:
            # avito_client.services.update_price(avito_id, price)
            logger.info(f"Цена для AvitoId {avito_id} успешно обновлена {price}. Салон {account.get('key')}")
        except Exception as e:
            logger.error(f"Ошибка обновления цены для AvitoId {avito_id}. Салон {account.get('key')}: {e}")

def update_quantity_on_avito(db_handler: DatabaseHandler, account: dict, stock_df: pd.DataFrame):
    """
    Обновляет количество на сайте Avito для всех совпадений по артикулу.

    :param db_handler: Экземпляр DatabaseHandler для взаимодействия с базой данных.
    :param store_name: Название магазина.
    :param stock_df: DataFrame с новыми данными, содержащий столбцы 'Артикул' и 'КоличествоОстаток'.
    """
    # Получаем все артикулы и AvitoId из таблицы stores
    stores_df = db_handler.fetch_avito_ids(store=account.get('key'))

    # Объединяем DataFrame по артикулу, оставляя все записи из stores_df
    merged_df = pd.merge(stores_df, stock_df, left_on='Id', right_on='Артикул', how='left')

    # Заполняем NaN в 'КоличествоОстаток' нулями для записей без совпадений
    merged_df['КоличествоОстаток'] = merged_df['КоличествоОстаток'].fillna(0)

    # Фильтруем записи, у которых AvitoId не пустой
    valid_entries = merged_df[merged_df['AvitoId'].notna()]

    # Подготовка данных для API Avito
    avito_data = valid_entries[['AvitoId', 'КоличествоОстаток']].to_dict('records')

    # Обновление количества на Avito через API
    avito_client = AvitoAPIClient(account.get('client_id'), account.get('client_secret'))
    for item in avito_data:
        avito_id = item['AvitoId']
        quantity = item['КоличествоОстаток']
        try:
            # avito_client.services.update_quantity(avito_id, quantity)
            logger.info(f"Количество для AvitoId {avito_id} успешно обновлено. Салон {account.get('key')}")
        except Exception as e:
            logger.error(f"Ошибка обновления количества для AvitoId {avito_id}. Салон {account.get('key')}: {e}")


