from integrations_1C import Client_1c
from business_logic import update_property_table
from db import DatabaseHandler
from business_logic.new_avito_item import new_avito_item, add_new_avito_item
from data.stores import stores
from utils.logger import get_logger

logger = get_logger("Функция создания карточек")

client_1c = Client_1c()
db_handler = DatabaseHandler()

def card_creation(account):
    stores_id = []
    store_name = account.get('key')
    offline_stores_name = account.get('stores')
    for store in offline_stores_name:
        stores_id.append(stores.get(store).get('Ссылка'))
    df_stock = client_1c.get_stock(stores_id)
    update_property_table(db_handler, df_stock)

    df_new_items = new_avito_item(db_handler, store_name)
    # добавляем данные из df_stock Index(['Номенклатура', 'Цена', 'КоличествоОстаток', 'НоменклатураНаименование', 'Артикул', 'НоменклатураКод'], в df_new_items Index(['product_article', 'id'], dtype='object') по Артикул = product_article
    df_new_items = df_new_items.merge(df_stock, left_on='product_article', right_on='Артикул', how='left')
    # удаляем данные по которым нет стока
    df_new_items = df_new_items[df_new_items['НоменклатураНаименование'].notna()]

    result = add_new_avito_item(db_handler, account, df_new_items)

    # добавляем результат в таблицу базы данных
    for item in result:
        try:
            db_handler.insert_new_avito_item(item)
        except Exception as e:
            logger.error(f"Ошибка при добавлении нового элемента в базу данных: {e}")



