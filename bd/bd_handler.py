import sqlite3
import pandas as pd
import os

class DatabaseHandler:
    def __init__(self, db_folder='bd', db_name='project_data.db'):
        # Убедимся, что папка для базы данных существует
        os.makedirs(db_folder, exist_ok=True)

        # Полный путь к базе данных
        self.db_path = os.path.join(db_folder, db_name)

        # Инициализация базы данных (создание таблицы, если нужно)
        self._initialize_db()

    def _initialize_db(self):
        """Инициализация базы данных и создание таблицы, если она не существует."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS stores (
                    key INTEGER PRIMARY KEY AUTOINCREMENT,
                    store TEXT,
                    AvitoId TEXT, 
                    Id TEXT, 
                    Title TEXT, 
                    Vendor TEXT, 
                    ImageUrls TEXT,
                    VideoURL TEXT,
                    Price TEXT, 
                    GoodsType TEXT, 
                    Color TEXT, 
                    Description TEXT, 
                    Condition TEXT, 
                    ContactPhone TEXT, 
                    AdType TEXT, 
                    Model TEXT, 
                    Category TEXT, 
                    Address TEXT, 
                    RamSize TEXT, 
                    MemorySize TEXT, 
                    ManagerName TEXT, 
                    Box_Sealed TEXT, 
                    IMEI TEXT 
                )
            ''')
            conn.commit()

    def add_record(self, record_dict):
        """Добавляет запись в таблицу, используя словарь с данными."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                # Получаем ключи и значения из словаря
                columns = ', '.join(record_dict.keys())
                placeholders = ', '.join(['?'] * len(record_dict))
                values = tuple(record_dict.values())
                
                # Выполняем SQL-запрос на вставку данных
                cursor.execute(f'''
                    INSERT INTO stores ({columns})
                    VALUES ({placeholders})
                ''', values)
                conn.commit()
        except sqlite3.Error as e:
            print(f"Ошибка при добавлении записи: {e}")

    def get_records_by_store(self, store):
        """
        Извлекает записи из таблицы, фильтруя для аккаунта Avito store.

        Эта функция подключается к базе данных SQLite, выполняет SQL-запрос для извлечения всех записей из таблицы 'stores', 
        где значение столбца 'store' совпадает с переданным параметром. 
        Результаты запроса возвращаются в виде DataFrame с использованием библиотеки pandas.

        Параметры:
        store (str): Название магазина, по которому будет выполняться фильтрация записей.

        Возвращает:
        DataFrame: DataFrame, содержащий все записи, соответствующие указанному магазину.
        В случае ошибки возвращает None и выводит сообщение об ошибке.
        """

        try:
            with sqlite3.connect(self.db_path) as conn:
                # Используем pandas для выполнения SQL-запроса и получения данных в виде DataFrame
                query = "SELECT * FROM stores WHERE store = ?"
                df = pd.read_sql_query(query, conn, params=(store,))
                return df
        except sqlite3.Error as e:
            print(f"Ошибка при извлечении записей: {e}")
            return None
    
    def delete_data(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''DELETE FROM stores''')
                conn.commit()
        except sqlite3.Error as e:
            print(f"Ошибка при удалении данных: {e}")

    def update_avito_id(self, record_list: list, store: str):
        """
        Обновляет значение AvitoId в базе данных по ключу Id.

        Параметры:
        record_list (list): Список словарей, содержащий ключи 'Id' и 'AvitoId' для обновления записи.
        store (str): Название магазина, по которому будет выполняться обновление записей.

        Возвращает:
        None
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                # Используем параметризованный запрос для повышения безопасности и производительности
                for record in record_list:
                    cursor.execute('''UPDATE stores SET AvitoId = ? WHERE Id = ? AND store = ?''', (record['AvitoId'], record['Id'], store))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Ошибка при обновлении данных: {e}")

    def get_id_mobicom(self, store): 
        # Функция возвращает список id из таблицы stores, где поле AvitoId равно Null
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''SELECT Id FROM stores WHERE AvitoId IS NULL AND store = ?''', (store,))
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Ошибка при получении id: {e}")

    def update_price(self, article_id, new_price, store):
        if article_id == 'MU0D3AH-A':
            print(article_id, new_price, store)
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''UPDATE stores SET Price = ? WHERE Id = ? AND store = ?''', (new_price, article_id, store))
                conn.commit()

        except sqlite3.Error as e:
            print(f"Ошибка при обновлении цены: {e}")

    def get_avito_id_by_article(self, store: str) -> list:
        # функция возвращает список avito_id и id из таблицы stores, где поле store равно переданному параметру
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''SELECT AvitoId, Id FROM stores WHERE store = ?''', (store,))
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Ошибка при получении avito_id: {e}")

# Пример использования
if __name__ == "__main__":
    db_handler = DatabaseHandler()

    # Добавление записей
    # db_handler.add_record('Store 1', '123', 'AVITO12345', 'IMEI67890')
    # db_handler.add_record('Store 2', '124', 'AVITO67890', 'IMEI12345')

    # # Извлечение записей по store
    # store_name = 'Store 1'
    # records = db_handler.get_records_by_store(store_name)
    # print(f"Записи для {store_name}: {records}")
    db_handler.delete_data()
