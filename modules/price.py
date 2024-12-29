from modules import Data_1c
import pandas as pd
from bd import DatabaseHandler
from avito_api import AvitoAPIClient


def price_stores(stores: list) -> pd.DataFrame:
    '''
    Функция для получения цен из 1с
    :param stores: Список ID магазинов
    :return: DataFrame с уникальными Артикулами и максимальными ценами, 'Артикул' и 'Цена'
    '''
    data = Data_1c()
    goods = []
    for store in stores:
        goods.extend(data.stock(store))
    df = pd.DataFrame(goods)
    # Создаем DataFrame с уникальными Артикул и максимальной ценой
    # Фильтруем DataFrame, чтобы исключить строки, где 'Артикул' равен null или ''
    df_filtered = df[df['Артикул'].notnull() & (df['Артикул'] != '')]
    # Создаем DataFrame с уникальными Артикул и максимальной ценой
    df_unique = df_filtered.groupby('Артикул', as_index=False)['Цена'].max()
    return df_unique

def update_price_avito(data: list, account: dict):
    '''
    Функция для обновления цен в avito
    :param data: Список кортежей (артикул, цена)
    :param account: Словарь с данными аккаунта
    :return: None
    '''
    
    # получение avito_ids из bd по артикулам
    db_handler = DatabaseHandler()
    account_key = list(account.keys())[0]
    avito_ids = db_handler.get_avito_id_by_article(account_key)

    # Проверяем, что avito_ids не None и является список    
    if avito_ids is None or not isinstance(avito_ids, list):
        print(f"avito_ids должен быть список, но получен None или неверный тип {avito_ids}")
        return None

    # обновление списка кортежей
    updated_data = []
    for article, price in data:
        # avito_ids список кортежей где первое значение avito_id, второе артикул
        avito_id = next((avito_id for avito_id, article_id in avito_ids if article_id == article), None)
        updated_data.append((article, price, avito_id))  # добавляем avito_id в кортеж

    # удаление кортежей где avito_id равно None, и уведомляем пользователя об артикулах которые не найдены 
    not_found_articles = [article for article, price, avito_id in updated_data if avito_id is None]

    updated_data = [(article, price, avito_id) for article, price, avito_id in updated_data if avito_id is not None]
    
    client = AvitoAPIClient(account[account_key]['client_id'], account[account_key]['client_secret'])

    for article, price, avito_id in updated_data:
        client.services.update_price(avito_id, price)



