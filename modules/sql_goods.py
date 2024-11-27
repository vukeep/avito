from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import time
import pandas as pd
import dotenv
import os

dotenv.load_dotenv()


# Настройки подключения
DB_CONFIG = {
    "username": os.getenv("DB_USERNAME"),  
    "password": os.getenv("DB_PASSWORD"),  
    "host": os.getenv("DB_SERVER"),        
    "database": os.getenv("DB_DATABASE"),
    "driver": os.getenv("DB_DRIVER")  
}


# Создание строки подключения
CONNECTION_STRING = (
    f"mssql+pyodbc://{DB_CONFIG['username']}:{DB_CONFIG['password']}"
    f"@{DB_CONFIG['host']}/{DB_CONFIG['database']}?driver={DB_CONFIG['driver']}"
)

# Создание движка SQLAlchemy
ENGINE = create_engine(CONNECTION_STRING)

def fetch_products(retries=2, delay=5) -> pd:
    """
    Получает список товаров из базы данных.
    При ошибке подключения делает несколько попыток, возвращает пустой список при неудаче.
    :param retries: Количество попыток восстановления соединения.
    :param delay: Задержка (в секундах) между попытками.
    :return: Список товаров (dict) или пустой список при ошибке.
    """
    query = """
        SELECT *
        FROM [PowerBImobi].[dbo].[all_mobicom]
        WHERE Артикул IS NOT NULL AND Артикул != ''
    """
    attempt = 0
    while attempt < retries:
        try:
            with ENGINE.connect() as connection:
                result = connection.execute(text(query))
                df = pd.DataFrame(result.fetchall(), columns=result.keys())
                print("Данные успешно получены.")
                return df  # Преобразуем в список словарей
        except SQLAlchemyError as e:
            print(f"Ошибка выполнения запроса: {e}. Попытка {attempt + 1} из {retries}.")
            attempt += 1
            time.sleep(delay)  # Задержка перед следующей попыткой
    print("Не удалось получить данные после нескольких попыток.")
    return pd.DataFrame()

def avito_models(data: dict, filter_keys: list):
    """
    Получает данные из базы данных с фильтрацией по указанным ключам.

    :param data: Словарь с данными для фильтрации.
    :param filter_keys: Список ключей для фильтрации.
    :return: DataFrame с результатами запроса.
    """
    # Словарь для сопоставления ключей с названиями столбцов в базе данных
    column_mapping = {
        'Объем встроенной памяти': 'MemorySize',
        'Объем оперативной памяти': 'RamSize',
        'Цвет_avito': 'Color',
        'Модель': 'Model'
    }

    # Формируем условия WHERE на основе переданных ключей
    conditions = []
    for key in filter_keys:
        if key in column_mapping and key in data:
            column_name = column_mapping[key]
            value = data[key]
            if key == 'Объем оперативной памяти':
                conditions.append(f"RamSize like '%{value}%'") # RamSize like '%8 ГБ%'
            else:
                conditions.append(f"{column_name} = '{value}'")

    # Объединяем условия в строку
    where_clause = f"vendor = '{data['Бренд']}' AND " + " AND ".join(conditions)

    # Формируем SQL-запрос
    query = f"""
        SELECT *
        FROM [PowerBImobi].[dbo].[avito_phones]
        WHERE {where_clause}
    """

    # Выполняем запрос и возвращаем результат
    with ENGINE.connect() as connection:
        result = connection.execute(text(query))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
        return df



if __name__ == '__main__':
    df = fetch_products()
    print(df)
