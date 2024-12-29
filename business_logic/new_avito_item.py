import pandas as pd
from db.db_handler import DatabaseHandler
from utils.logger import get_logger
from business_logic.new_avito_card import new_avito_card
from utils import CloudinaryClient
from data import type, brand

logger = get_logger("Создание новых карточек")    

def new_avito_item(db_handler: DatabaseHandler, store: str) -> pd.DataFrame:
    """
    Получает артикулы продуктов по списку типов и брендов.
    Возвращает DataFrame с артикулами и id, которых нет в базе данных.
    """
    df_articles = db_handler.get_article_by_type_brand(type, brand) # получаем артикулы из products
    df_articles_avito = db_handler.get_avito_items(store) # получаем артикулы (id) из stores(таблица карточек avito)

    # полчаем все артикулы из df_articles, которых нет в df_articles_avito
    articles = df_articles[~df_articles['product_article'].isin(df_articles_avito['Id'])]

    return articles

def add_new_avito_item(db_handler: DatabaseHandler, account: dict, articles: pd.DataFrame):
    """
    Получает артикулы и id продуктов которые нет в базе данных.
    Добавляет новые карточки в базу данных товаров.
    """
    new_cards_list = []

    for index, row in articles.iterrows():
        id = row['id']
        if pd.isna(row['Артикул']):
            logger.error(f'Артикул - Nan для id {id}')
            continue
        properties = db_handler.get_properties_by_product_id(id)
        if properties is None:
            logger.error(f'Свойства - None для id {id}')
            continue
        # преобразуем properties в словарь с ключами name и value   
        properties_dict = properties.to_dict(orient='records')
        # преобразуем properties_dict в словарь с ключами name и value
        properties_dict = {item['name']: item['value'] for item in properties_dict}

        new_card = new_avito_card(account, row, properties_dict)
        if not new_card:
            continue

        cloudinary_client = CloudinaryClient()
        logger.info(f'Новая карточка: {new_card.get("Id")}')

        # Обновляем данные в базе

        try:
            article = new_card.get('Id')
        except:
            logger.error(f'{new_card} - не понятно что это')
            continue
        url = cloudinary_client.url_to_string(article)
        if "http://res.cloudinary.com/avitophoto/image" not in url: # проверяем есть ли в строке текст http://res.cloudinary.com/avitophoto/image
            logger.error(f'{new_card} - нет изображения')
            continue
        new_card['ImageUrls'] = url
        new_card['store'] = account.get('key')
        data_details = account.get('data_details')
        # Объединяем два словаря item и data_details
        new_card.update(data_details)
        # Сохраняем new_card в список словарей
        new_cards_list.append(new_card)

    return new_cards_list
