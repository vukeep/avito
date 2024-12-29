import sqlite3
import os
import pandas as pd
from utils.logger import get_logger

logger = get_logger("База данных")

class DatabaseHandler:
    def __init__(self, db_folder='db', db_name='project_data.db'):
        """
        Инициализируйте обработчик базы данных. Убедитесь, что база данных существует.
        """
        # Убедитесь, что папка с базой данных существует
        os.makedirs(db_folder, exist_ok=True)

        # Полный путь к базе данных
        self.db_path = os.path.join(db_folder, db_name)

        # Инициализирует схему базы данных
        self._initialize_db()

    def _initialize_db(self):
        """
        Инициализирует базу данных и создает необходимые таблицы, если они не существуют.
        """
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        if not os.path.exists(schema_path):
            raise FileNotFoundError(f"Schema file not found: {schema_path}")
        
        with sqlite3.connect(self.db_path) as conn:
            with open(schema_path, 'r') as schema_file:
                conn.executescript(schema_file.read())

    def insert_product(self, product_code, product_article, brand, product_type, properties):
        """
        Вставляет продукт и его свойства в базу данных.

        :param product_code: Код продукта (строка).
        :param brand: Бренд продукта (строка).
        :param product_type: Тип продукта (строка).
        :param properties: Список словарей с именами и значениями свойств.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Вставляем продукт с брендом и типом
            cursor.execute(
                """
                INSERT OR IGNORE INTO products (product_code, product_article, brand, type)
                VALUES (?, ?, ?, ?)
                """,
                (product_code, product_article, brand, product_type)
            )
            product_id = cursor.execute(
                "SELECT id FROM products WHERE product_code = ?",
                (product_code,)
            ).fetchone()[0]

            # Вставляем свойства
            for prop in properties:
                cursor.execute(
                    "INSERT INTO product_properties (product_id, name, value) VALUES (?, ?, ?)",
                    (product_id, prop['name'], prop['values'][0])
                )

            conn.commit()

    def avito_query(self, query: str, params: tuple):
        with sqlite3.connect(self.db_path) as conn:
            df = pd.read_sql_query(query, conn, params=params)
            return df

    def get_article_by_type_brand(self, type, brand):
        query = """
        SELECT product_article, Id FROM products 
        WHERE type IN ({}) AND brand IN ({})
        """.format(','.join('?' * len(type)), ','.join('?' * len(brand)))
        with sqlite3.connect(self.db_path) as conn:
            df = pd.read_sql_query(query, conn, params=(*type, *brand))
            return df
        
    def get_avito_items(self, store: str) -> pd.DataFrame:
        """
        Получает список id из таблицы stores, где поле AvitoId не равно Null и возвращает их в виде DataFrame.
        """
        query = "SELECT Id FROM stores WHERE store = ?"
        with sqlite3.connect(self.db_path) as conn:
            df = pd.read_sql_query(query, conn, params=(store,))
            return df
        
    def insert_new_avito_item(self, item):
        """
        Вставляет новый элемент в таблицу stores.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                columns = ', '.join(item.keys())
                placeholders = ', '.join(['?'] * len(item))
                values = tuple(item.values())

                query = f"INSERT INTO stores ({columns}) VALUES ({placeholders})"
                cursor.execute(query, values)
                conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Error adding record: {e}")


    def update_record(self, store, record_dict):
        """
        Универсальная функция для обновления записи в таблице `stores`.
        
        :param store: Название магазина (используется для фильтрации записей).
        :param record_dict: Словарь с данными для обновления. Обязательный ключ `Id`.
                            Остальные ключи - это столбцы, которые нужно обновить.
        """
        if 'Id' not in record_dict:
            raise ValueError("Ключ 'Id' обязателен в словаре данных для обновления.")
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Извлекаем столбцы и значения для обновления
                columns = [f"{key} = ?" for key in record_dict if key != 'Id']
                values = [record_dict[key] for key in record_dict if key != 'Id']
                
                # Генерируем SQL-запрос
                query = f"""
                    UPDATE stores
                    SET {', '.join(columns)}
                    WHERE Id = ? AND store = ?
                """
                
                # Выполняем запрос
                cursor.execute(query, values + [record_dict['Id'], store])
                conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Error updating record: {e}")

    def get_all_stores(self, store):
        """
        Получает все записи из таблицы stores.
        """
        query = "SELECT * FROM stores WHERE store = ?"
        with sqlite3.connect(self.db_path) as conn:
            df = pd.read_sql_query(query, conn, params=(store,))
            return df

    def delete_stores(self):
        """
        Удаляет таблицу stores.
        """
        query = "DROP TABLE IF EXISTS stores"
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()









    def get_properties_by_product_id(self, product_id):
        query = "SELECT name, value FROM product_properties WHERE product_id = ?"
        with sqlite3.connect(self.db_path) as conn:
            df = pd.read_sql_query(query, conn, params=(product_id,))
            return df
        
    def get_all_product_articles(self) -> list:
        """
        Получает все product_article из таблицы products. 

        :return: Список всех product_article (list).
        """
        query = "SELECT product_article FROM products GROUP BY product_article"
        with sqlite3.connect(self.db_path) as conn:
            # Возвращаем результат в виде DataFrame
            df = pd.read_sql_query(query, conn)
            return df[df['product_article'].notna()]  # Исключаем None


    def add_record(self, record_dict):
        """
        Добавьте одну запись в таблицу `stores`.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                columns = ', '.join(record_dict.keys())
                placeholders = ', '.join(['?'] * len(record_dict))
                values = tuple(record_dict.values())

                query = f"INSERT INTO stores ({columns}) VALUES ({placeholders})"
                cursor.execute(query, values)
                conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Error adding record: {e}")

    def fetch_records_by_store(self, store):
        """
        Получение всех записей для определенного магазина.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                query = "SELECT * FROM stores WHERE store = ?"
                return pd.read_sql_query(query, conn, params=(store,))
        except sqlite3.Error as e:
            logger.error(f"Error fetching records: {e}")
            return pd.DataFrame()




    def delete_records_by_store(self, store):
        """
        Удаление всех записей для определенного магазина.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                query = "DELETE FROM stores WHERE store = ?"
                cursor.execute(query, (store,))
                conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Error deleting records: {e}")

    def fetch_avito_ids(self, store):
        """
        Получение AvitoId и Id для всех записей магазина.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                query = "SELECT AvitoId, Id FROM stores WHERE store = ?"
                return pd.read_sql_query(query, conn, params=(store,))
        except sqlite3.Error as e:
            logger.error(f"Error fetching Avito IDs: {e}")
            return pd.DataFrame()
        
    def get_id_mobicom(self, store): 
        """
        Функция возвращает список id из таблицы stores, где поле AvitoId равно Null
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''SELECT Id FROM stores WHERE AvitoId IS NULL AND store = ?''', (store,))
                return cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"Ошибка при получении id: {e}")

# Example usage
if __name__ == "__main__":
    db_handler = DatabaseHandler()

    db_handler.delete_stores()
