import pandas as pd
from article_properties import MobicomAPI
from sql_goods import fetch_products, avito_models
from fuzzywuzzy import fuzz

mobicom_api = MobicomAPI()

def product_list(stores: list) -> list:
    '''
    """
    Функция для получения списка товаров из базы данных.

    :param stores: Список магазинов, по которым нужно отфильтровать товары.
    :type stores: list
    :return: Список товаров, подготовленных для обновления данных в avito_models.
    :rtype: list

    Функция выполняет следующие шаги:
    1. Получает все товары из базы данных с помощью функции fetch_products().
    2. Фильтрует товары по списку магазинов, переданному в параметре stores.
    3. Группирует отфильтрованные товары по полям 'Название', 'Артикул', 'Цена', 'Бренд', 'Память', 'Цвет' и выбирает максимальное значение 'IMEI' для каждой группы.
    4. Для каждого товара в сгруппированном списке запрашивает дополнительную информацию по артикулу с помощью метода get_product_by_article() класса MobicomAPI.
    5. Извлекает необходимые ключи из полученной информации и добавляет их в результирующий словарь.
    6. Возвращает список словарей с информацией о товарах.
    """
    '''

    df = fetch_products()

    # Фильтрация по списку магазинов
    df_filtered = df[df['Магазин'].isin(stores)]
    
    # Группировка результата по полям Название, Артикул, Цена, Бренд, Память, Цвет и IMEI
    df_grouped = df_filtered.groupby(['Название', 'Артикул', 'Цена', 'Бренд', 'Память', 'Цвет']).agg({'IMEI': 'max'}).reset_index()
    
    result_list = []
    for index, row in df_grouped.iterrows():
        article = row['Артикул']
        result = mobicom_api.get_product_by_article(article)
        if result.get('status') == 'success':
            # Список ключей, которые нужно извлечь
            keys_to_extract = ['Бренд', 'Тип', 'Объем встроенной памяти', 'Объем оперативной памяти']

            # Создаём результирующий словарь
            result = {key: next((item['values'][0] for item in result['data'] if item['name'] == key), None) for key in keys_to_extract}
            result['Цвет'] = row['Цвет']
            result['Название'] = row['Название']
            result['Цена'] = row['Цена']
            result['Артикул'] = row['Артикул']
            result['IMEI'] = row['IMEI']

            result_list.append(result)

        # if index == 1:
        #     break
    return result_list

def update_avito_models(data: list):

    """
    Функция для обновления данных словаря по атрибутам таблицы avito_models.

    :param data: Список словарей с данными о товарах.
    :type data: list
    :return: Обновленный список словарей с добавленными атрибутами из таблицы avito_models.
    :rtype: list

    Функция выполняет следующие шаги:
    1. Проходит по каждому элементу в списке data.
    2. Проверяет, является ли тип товара 'смартфон'.
    3. Извлекает и преобразует необходимые атрибуты (бренд, объем встроенной памяти, объем оперативной памяти, цвет, название, артикул, цена).
    4. Формирует модель товара, удаляя из названия бренда, объем памяти, оперативную память и цвет.
    5. В зависимости от бренда (Apple или другой), выполняет запросы к базе данных для получения моделей и цветов товаров.
    6. Ищет наилучшее совпадение модели и цвета в базе данных.
    7. Обновляет словарь товара новыми атрибутами (модель и цвет).
    8. Возвращает обновленный список словарей с добавленными атрибутами.
    """

    new_data = []
    for item in data:
        if item.get('Тип') == 'смартфон':
            try:
                brand = item.get('Бренд').lower()
                memory = item.get('Объем встроенной памяти').lower()
                ram = item.get('Объем оперативной памяти')
                if ram:
                    ram = ram.lower()
                else:
                    ram = ''
                color = item.get('Цвет').lower()
                name = item.get('Название').lower()
                article = item.get('Артикул').lower()
                price = item.get('Цена')
                model_not_ram = name.split('(')[0].strip()
                name_model = model_not_ram.replace(brand, '').replace(memory, '').replace(ram, '').replace(color, '').strip()
                if brand == 'samsung':
                    name_model = name_model.split(' ', 1)[1] if ' ' in name_model else name_model

                if brand == 'apple':
                    models_df = avito_models(item, ['Бренд', 'Объем встроенной памяти'])
                else:
                    models_df = avito_models(item, ['Бренд', 'Объем встроенной памяти', 'Объем оперативной памяти'])

                best_match_model = model_search(models_df, 'Model', name_model)
                item['Модель'] = best_match_model

                if brand == 'apple':
                    models_df = avito_models(item, ['Бренд', 'Модель', 'Объем встроенной памяти'])
                else:
                    models_df = avito_models(item, ['Бренд', 'Модель', 'Объем встроенной памяти', 'Объем оперативной памяти'])

                best_match_color = model_search(models_df, 'Color', color)
                item['Цвет_avito'] = best_match_color

                if brand == 'apple':
                    color_df = avito_models(item, ['Бренд', 'Модель', 'Объем встроенной памяти', 'Цвет_avito'])
                else:
                    color_df = avito_models(item, ['Бренд', 'Модель', 'Объем встроенной памяти', 'Объем оперативной памяти', 'Цвет_avito'])

                # Преобразуем DataFrame в список, где каждое значение - это сумма всех строк через пробел
                all_dict = color_df.to_dict(orient='records')

                model_avito = all_dict[0]['Vendor'] + ' ' + all_dict[0]['Model'] + ' ' + all_dict[0]['MemorySize']
                if ',' in all_dict[0]['RamSize']: # содержит запятую
                    ram_size = item.get('Объем оперативной памяти')
                else:
                    ram_size = all_dict[0]['RamSize']
                model_avito += '/' + ram_size + ' ' + all_dict[0]['Color']

                final_dict = {
                    'Название': model_avito,
                    'Артикул': item.get('Артикул'),
                    'Цена': item.get('Цена'),
                    'Бренд': all_dict[0]['Vendor'],
                    'Модель': all_dict[0]['Model'],
                    'MemorySize': all_dict[0]['MemorySize'],
                    'RamSize': ram_size,
                    'Цвет': all_dict[0]['Color'],
                    'IMEI': item.get('IMEI')
                }

                new_data.append(final_dict)
            except Exception as e:
                print(item.get('Название'), e)
                continue
    return new_data
        
def model_search(df: pd.DataFrame, filter_keys: str, name: str) -> str:
    """
    Функция для поиска наиболее вероятного совпадения модели в DataFrame.

    :param df: DataFrame, содержащий столбец 'Model'.
    :param name_model: Строка, представляющая модель, для которой нужно найти совпадение.
    :return: Наиболее вероятное значение модели из DataFrame.
    """
    # Проверяем, что DataFrame содержит столбец 'Model'
    if filter_keys not in df.columns:
        raise ValueError(f"DataFrame должен содержать столбец '{filter_keys}'")

    # Инициализируем переменные для хранения наилучшего совпадения и его вероятности
    best_match = None
    highest_probability = 0.0

    # Проходим по каждой строке DataFrame
    for index, row in df.iterrows():
        value = row[filter_keys]
        
        # Вычисляем вероятность совпадения (например, используя простое сравнение строк)
        # Здесь можно использовать более сложные алгоритмы, такие как Levenshtein distance
        probability = fuzzy_similarity(name, value)

        # Если текущая вероятность выше, чем ранее найденная, обновляем наилучшее совпадение
        if probability > highest_probability:
            highest_probability = probability
            best_match = value

    # Возвращаем наилучшее совпадение
    return best_match

def fuzzy_similarity(str1: str, str2: str) -> float:
    """
    Вычисляет схожесть строк с использованием библиотеки FuzzyWuzzy.

    :param str1: Первая строка.
    :param str2: Вторая строка.
    :return: Вероятность совпадения в виде числа от 0 до 1.
    """
    return fuzz.ratio(str1, str2) / 100.0

def update_mobicom_data(stores: list):
    """
    Функция для обновления данных Mobicom.

    :param stores: Список магазинов, для которых необходимо обновить данные.
    :return: Обновленные данные Avito.
    """
    list_data = product_list(stores)
    avito_data = update_avito_models(list_data)
    return avito_data

if __name__ == '__main__':
    stores = ['Чита Склад Макси 4 iSmart', 'Иркутск Ангарск iSmart']
    avito_data = update_mobicom_data(stores)
    print(avito_data)




