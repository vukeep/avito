import pandas as pd
from db.db_handler import DatabaseHandler
from fuzzywuzzy import fuzz
from utils import get_logger
from llm import ai_agent

logger = get_logger("Функция поиска моделей")

def avito_models(data: dict, filter_keys: list) -> pd.DataFrame:
    """
    Получает данные из базы данных с фильтрацией по указанным ключам.

    :param data: Словарь с данными для фильтрации
    :param filter_keys: Список ключей для фильтрации
    :return: DataFrame с результатами запроса
    """
    # Словарь для сопоставления ключей с названиями столбцов в базе данных
    column_mapping = {
        'Объем встроенной памяти': 'MemorySize',
        'Объем оперативной памяти': 'RamSize',
        'Цвет_avito': 'Color',
        'Модель': 'Model'
    }

    # Создаем подключение к базе данных
    db_handler = DatabaseHandler()

    # Формируем условия WHERE
    conditions = []
    params = []
    
    # Добавляем условие для бренда
    conditions.append("Vendor = ?")
    params.append(data['Бренд'])

    # Добавляем остальные условия
    for key in filter_keys:
        if key in column_mapping and key in data:
            column_name = column_mapping[key]
            value = data[key]
            if key == 'Объем оперативной памяти':
                conditions.append(f"RamSize LIKE ?")
                params.append(f"%{value.upper()}%")
            elif key == 'Объем встроенной памяти':
                conditions.append(f"MemorySize = ?")
                params.append(value.upper())
            else:
                conditions.append(f"{column_name} = ?")
                params.append(value)

    # Формируем SQL-запрос, не чувствительный к регистру значений
    query = f"""
        SELECT *
        FROM avito_phones
        WHERE {' AND '.join([f"LOWER({condition.split('=')[0].strip()}) = LOWER(?)" if '=' in condition else condition for condition in conditions])}
    """
    # Выполняем запрос
    df = db_handler.avito_query(query, params)
    return df

def model_search(df: pd.DataFrame, filter_keys: str, name: str) -> str:
    """
    Функция для поиска наиболее вероятного совпадения модели в DataFrame.

    :param df: DataFrame, содержащий столбец с моделями
    :param filter_keys: Имя столбца для поиска
    :param name: Строка, представляющая модель, для которой нужно найти совпадение
    :return: Наиболее вероятное значение модели из DataFrame
    """
    # Проверяем, что DataFrame содержит нужный столбец
    if filter_keys not in df.columns:
        raise ValueError(f"DataFrame должен содержать столбец '{filter_keys}'")

    # Инициализируем переменные для хранения наилучшего совпадения
    best_match = None
    highest_probability = 0.0

    # Оставляем только нужную колонку и группируем ее
    df_grouped = df[[filter_keys]].groupby(filter_keys).size().reset_index(name='counts')

    # Проходим по каждой строке DataFrame
    for index, row in df_grouped.iterrows():
        value = row[filter_keys]
        
        # Вычисляем вероятность совпадения
        probability = fuzzy_similarity(name, value)

        # Если текущая вероятность выше, обновляем наилучшее совпадение
        if probability > highest_probability:
            highest_probability = probability
            best_match = value
    if filter_keys == 'Color':
        if highest_probability != 1:
            # Преобразуем df_grouped.iterrows() строку со списком значений
            grouped_values = df_grouped[filter_keys].tolist()
            # Преобразуем список grouped_values в строку через запятую
            grouped_values_str = ', '.join(grouped_values)
            result = ai_agent(name, grouped_values_str)
            if isinstance(result, str):
                return {'error': result}
            try:
                if int(result.get('Your confidence level')) > 5:
                    return {'avito_color': result.get('Most appropriate')}
                else:
                    return {'error': 'нет уверенности в ответе'}
            except:
                return {'error': 'Ошибка при определении наиболее вероятного совпадения модели'}
        else:
            return {'avito_color': best_match}

    return best_match

def fuzzy_similarity(str1: str, str2: str) -> float:
    """
    Вычисляет схожесть строк с использованием библиотеки FuzzyWuzzy.

    :param str1: Первая строка
    :param str2: Вторая строка
    :return: Вероятность совпадения в виде числа от 0 до 1
    """
    return fuzz.ratio(str1.lower(), str2.lower()) / 100.0


if __name__ == '__main__':
    # Пример использования
    test_data = {
        'Бренд': 'apple',
        'Объем встроенной памяти': '128 ГБ',
        'Цвет_avito': 'черный'
    }
    test_filter_keys = ['Объем встроенной памяти', 'Цвет_avito']
    df = avito_models(test_data, test_filter_keys)
    print(df)
