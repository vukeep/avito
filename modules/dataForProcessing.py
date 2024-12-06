import pandas as pd
from modules import MobicomAPI
from modules import fetch_products, avito_models
from fuzzywuzzy import fuzz

mobicom_api = MobicomAPI()

def stock_stores(stores: list) -> pd.DataFrame:

    '''
    :param stores: Список магазинов, по которым нужно отфильтровать товары.
    :type stores: list
    :return: DataFrame с отфильтрованными и сгруппированными данными.
    :rtype: pd.DataFrame

    Функция выполняет следующие шаги:
    1. Получает все товары из базы данных с помощью функции fetch_products().
    2. Фильтрует товары по списку магазинов, переданному в параметре stores.
    3. Группирует результат по полям Название, Артикул, Цена, Бренд, Память, Цвет и IMEI.
    4. Возвращает DataFrame с отфильтрованными и сгруппированными данными.
    '''

    df = fetch_products() # Получаем данные из базы в DataFrame

    # Фильтрация по списку магазинов
    df_filtered = df[df['Магазин'].isin(stores)]

    # Заполнение NaN значениями по умолчанию
    df_filtered = df_filtered.fillna({
        'Название': '',
        'Код': '',
        'Цена Mobicom': 0,
        'Цена iSmart': 0,
        'Бренд': '',
        'Память': '',
        'Цвет': ''
    })

    df_filtered['IMEI'] = df_filtered['IMEI'].astype(str)
    
    # Группировка результата по полям Название, Артикул, Код, Цена Mobicom, Цена iSmart, Бренд, Память, Цвет и IMEI
    df_grouped = df_filtered.groupby(['Название', 'Артикул', 'Код', 'Цена Mobicom', 'Цена iSmart', 'Бренд', 'Память', 'Цвет']).agg({'IMEI': 'max'}).reset_index()
    

    return df_grouped

def product_list(df: pd.DataFrame) -> list:
    '''
    Функция для получения списка товаров из базы данных.

    :param df: DataFrame, содержащий данные о товарах.
    :type df: pd.DataFrame
    :return: Список товаров, подготовленных для обновления данных в avito_models.
    :rtype: list

    1. Группирует отфильтрованные товары по полям 'Название', 'Артикул', 'Цена', 'Бренд', 'Память', 'Цвет' и выбирает максимальное значение 'IMEI' для каждой группы.
    2. Для каждого товара в сгруппированном списке запрашивает дополнительную информацию по артикулу с помощью метода get_product_by_article() класса MobicomAPI.
    3. Извлекает необходимые ключи из полученной информации и добавляет их в результирующий словарь.
    4. Возвращает список словарей с информацией о товарах.
    '''


    
    result_list = []
    for index, row in df.iterrows():
        article = row['Артикул']
        result = mobicom_api.get_product_by_article(article)
        if result.get('status') == 'success':
            # Список ключей, которые нужно извлечь
            keys_to_extract = ['Бренд', 'Тип', 'Объем встроенной памяти', 'Объем оперативной памяти']

            # Создаём результирующий словарь
            result = {key: next((item['values'][0] for item in result['data'] if item['name'] == key), None) for key in keys_to_extract}
            result['Цвет'] = row.get('Цвет')
            result['Название'] = row.get('Название')
            result['Цена'] = row.get('Цена iSmart')
            result['Артикул'] = row.get('Артикул')
            result['IMEI'] = row.get('IMEI')

            result_list.append(result)
        else:
            print(f'{row.get("Название")}, {article}, {row.get("Тип")} - нет данных')

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
            new_data.append(smart_phone_function(item))
        elif item.get('Тип') == 'умные часы' and item.get('Бренд') == 'Apple':
            new_data.append(smart_watch_function(item))
        elif item.get('Тип') in ['беспроводные наушники', 'полноразмерные наушники'] and item.get('Бренд') == 'Apple':
            new_data.append(wireless_headphones_function(item))
        else:
            # 'Бренд', 'Тип', 'Название'
            print(f'{item.get("Бренд")}, {item.get("Тип")}, {item.get("Название")} - не принимаемый товар')
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

def smart_watch_function(item: dict) -> dict:
    try:    
        brand = item.get('Бренд')
        name = item.get('Название')
        color = item.get('Цвет')
        price = item.get('Цена')
        article = item.get('Артикул')

        final_dict = {
            'Title': name,
            'Id': article,
            'Price': price,
            'Vendor': brand,
            'Color': color,
            'GoodsType': 'Часы', # в api avito это поле имеет значение 'Наушники'
            'Category': 'Часы и украшения',
            'ProductType': 'Смарт-часы или браслет',
            'ProductSubType': 'Смарт-часы',
            'Gender': 'Унисекс',
            'StrapType': 'Силикон',
            'Brand': brand,
        }
        return final_dict


    except:
        print(f'{item} - не понятные умные часы')

def wireless_headphones_function(item: dict) -> dict:
    try:    
        brand = item.get('Бренд')
        name = item.get('Название')
        color = item.get('Цвет')
        price = item.get('Цена')
        article = item.get('Артикул')

        final_dict = {
            'Title': name,
            'Id': article,
            'Price': price,
            'Vendor': brand,
            'Color': color,
            'GoodsType': 'Наушники', # в api avito это поле имеет значение 'Наушники'
            'Category': 'Аудио и видео',
        }
        return final_dict


    except:
        print(f'{item} - не понятные беспроводные наушники')

def smart_phone_function(item: dict) -> dict:
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
            'Title': model_avito,
            'Id': item.get('Артикул'),
            'Price': item.get('Цена'),
            'Vendor': all_dict[0]['Vendor'],
            'Model': all_dict[0]['Model'],
            'MemorySize': all_dict[0]['MemorySize'],
            'RamSize': ram_size,
            'Color': all_dict[0]['Color'],
            'IMEI': item.get('IMEI'),
            'GoodsType': 'Мобильные телефоны', # в api avito это поле имеет значение 'Мобильные телефоны'
            'Category': 'Телефоны',
        }

        return final_dict
    except Exception as e:
        print(item.get('Название'), e)

def fuzzy_similarity(str1: str, str2: str) -> float:
    """
    Вычисляет схожесть строк с использованием библиотеки FuzzyWuzzy.

    :param str1: Первая строка.
    :param str2: Вторая строка.
    :return: Вероятность совпадения в виде числа от 0 до 1.
    """
    return fuzz.ratio(str1, str2) / 100.0

def update_mobicom_data(df: pd.DataFrame):
    """
    Функция для обновления данных Mobicom.

    :param df: DataFrame, содержащий данные о товарах.
    :return: Обновленные данные Avito.
    """
    list_data = product_list(df) # получение списка словарей с данными о товарах
    avito_data = update_avito_models(list_data) # обновление данных словаря по атрибутам таблицы avito_models
    return avito_data

if __name__ == '__main__':
    df = stock_stores(['Чита Склад Макси 4 iSmart', 'Иркутск Ангарск iSmart'])
    avito_data = update_mobicom_data(df)
    for item in avito_data:
        print(item)