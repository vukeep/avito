import pandas as pd
from db.db_handler import DatabaseHandler
from integrations_Mobicom import MobicomAPI
from utils.logger import get_logger

logger = get_logger("Обновление таблицы свойств")

def update_property_table(db_handler: DatabaseHandler, df_stock: pd.DataFrame):
    """
    Обновляет таблицу свойств на основе данных из 1С
    
    Args:
        db_handler: экземпляр DatabaseHandler
        df_stock: DataFrame с данными из 1С
    """
    client_mobicom = MobicomAPI()

    # Проверяем наличие необходимой колонки
    if 'Артикул' not in df_stock.columns:
        logger.error("В данных отсутствует колонка 'Артикул'")
        logger.debug(f"Доступные колонки: {df_stock.columns.tolist()}")
        return
    
    # Получаем существующие артикулы из БД
    existing_articles = db_handler.get_all_product_articles() # список артикулов которые есть в базе данных
    existing_articles_set = set(existing_articles['product_article'].tolist())
    
    # Находим новые артикулы
    new_articles = df_stock[~df_stock['Артикул'].isin(existing_articles_set)]

    # Удаляем дубли из new_articles
    new_articles = new_articles.drop_duplicates(subset=['Артикул'])

    # Обработка новых артикулов
    for _, article in new_articles.iterrows():  
        article = article['Артикул']

        
        logger.info(f"Артикул: {article}")
        # Получаем строку из df_stock по 'Артикул'
        product_row = df_stock[df_stock['Артикул'] == article].iloc[0]
        code = product_row['НоменклатураКод']
        brand = None
        type = None

        properties = client_mobicom.get_product_by_article(article)
        if properties['status'] == 'success':
            product = properties['data']
            for item in product:
                if item['name'] == 'Тип':
                    type = item['values'][0]
                elif item['name'] == 'Бренд':
                    brand = item['values'][0]
                elif item['name'] == 'Код':
                    code = item['values'][0]
            if all([code, brand, type]):
                logger.info(f"Обновление таблицы свойств для кода: {code}, бренда: {brand}, типа: {type}, продукт {product_row['НоменклатураКод']}")
                db_handler.insert_product(code, article, brand, type, product)
                properties = None
            else:
                logger.error(f"Не найдены свойства для Артикула: {article}")
             


if __name__ == "__main__":
    pass
