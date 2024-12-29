from data.stores import stores
from integrations_1C import Client_1c
import business_logic
from db.db_handler import DatabaseHandler
from data import accounts

client_1c = Client_1c()
db_handler = DatabaseHandler()

def price_update():
    for account in accounts:
        stores_id = []
        offline_stores_name = account.get('stores')
        for store in offline_stores_name:
            stores_id.append(stores.get(store).get('Ссылка'))
        df_stock = client_1c.get_stock(stores_id)
        
        # обновление цен в таблице stores
        business_logic.update_prices_in_stores(db_handler, account, df_stock)

        # обновление цен на сайте avito
        business_logic.update_prices_on_avito(db_handler, account, df_stock)

        # обновление количества на сайте avito, товар отсутствует в df_stock, то предаем остаток 0
        business_logic.update_quantity_on_avito(db_handler, account, df_stock)
