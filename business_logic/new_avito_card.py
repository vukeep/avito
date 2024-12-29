import pandas as pd
from business_logic.avito_data import avito_models, model_search
from utils.logger import get_logger

logger = get_logger("Дополнение карточек")

def new_avito_card(account: dict, stock_item: pd.DataFrame, properties_dict: dict):
    stock_item_dict = stock_item.to_dict()
    if properties_dict.get('Тип') == 'смартфон':
        result = smart_phone_card(account, stock_item_dict, properties_dict)
        return result
    elif properties_dict.get('Тип') == 'планшет':
        result = tablet_card(account, stock_item_dict, properties_dict)
        return None
    elif properties_dict.get('Тип') == 'умные часы':
        result = smart_watch_card(account, stock_item_dict, properties_dict)
        return result
    elif properties_dict.get('Тип') == 'беспроводные наушники':
        result = wireless_headphones_card(account, stock_item_dict, properties_dict)
        return result
    elif properties_dict.get('Тип') == 'полноразмерные наушники':
        result = wireless_headphones_card(account, stock_item_dict, properties_dict)
        return result
    elif properties_dict.get('Тип') == 'геймпад':
        result = gamepad_card(account, stock_item_dict, properties_dict)
        return None
    elif properties_dict.get('Тип') == 'игровая консоль':
        result = console_card(account, stock_item_dict, properties_dict)
        return None
    elif properties_dict.get('Тип') == 'фен':
        result = hair_dryer_card(account, stock_item_dict, properties_dict)
        return None
    elif properties_dict.get('Тип') == 'фен-стайлер':
        result = hair_dryer_card(account, stock_item_dict, properties_dict)
        return None
    else:
        return None



def smart_phone_card(account: dict, stock_item_dict: dict, properties_dict: dict):
    try:
        brand = properties_dict.get('Бренд').lower()
        memory = properties_dict.get('Объем встроенной памяти')
        ram = properties_dict.get('Объем оперативной памяти')
        if ram:
            ram = ram.lower()
        else:
            ram = ''
        color = stock_item_dict.get('НоменклатураНаименование').split(' ')[-1].lower()
        name = stock_item_dict.get('НоменклатураНаименование').lower()
        article = stock_item_dict.get('Артикул')
        price = stock_item_dict.get('Цена')
        model_not_ram = name.split('(')[0].strip()
        name_model = model_not_ram.replace(brand, '').replace(memory.lower(), '').replace(ram, '').replace('1 тб', '').replace(color, '').strip()

        
        if brand == 'samsung':
            name_model = name_model.split(' ', 1)[1] if ' ' in name_model else name_model

        if brand == 'apple':
            models_df = avito_models(properties_dict, ['Бренд', 'Объем встроенной памяти'])
        else:
            models_df = avito_models(properties_dict, ['Бренд', 'Объем встроенной памяти', 'Объем оперативной памяти'])


        best_match_model = model_search(models_df, 'Model', name_model)
        stock_item_dict['Модель'] = best_match_model
        stock_item_dict['Бренд'] = brand
        stock_item_dict['Объем встроенной памяти'] = memory
        stock_item_dict['Объем оперативной памяти'] = ram

        if brand == 'apple':
            models_df = avito_models(stock_item_dict, ['Бренд', 'Модель', 'Объем встроенной памяти'])
        else:
            models_df = avito_models(stock_item_dict, ['Бренд', 'Модель', 'Объем встроенной памяти', 'Объем оперативной памяти'])

        # ищем цвет
        best_match_color = model_search(models_df, 'Color', color)
        if isinstance(best_match_color, str):
            logger.error(f"ошибка при определении цвета, вернулась строка - {best_match_color}")
            return None
        if 'error' in best_match_color:
            logger.error(f"ошибка при определении цвета - {best_match_color}")
            return None
        else:
            stock_item_dict['Цвет_avito'] = best_match_color.get('avito_color')

        
        if brand == 'apple':
            color_df = avito_models(stock_item_dict, ['Бренд', 'Модель', 'Объем встроенной памяти', 'Цвет_avito'])
        else:
            color_df = avito_models(stock_item_dict, ['Бренд', 'Модель', 'Объем встроенной памяти', 'Цвет_avito', 'Объем оперативной памяти'])

        # Преобразуем DataFrame в список, где каждое значение - это сумма всех строк через пробел
        all_dict = color_df.to_dict(orient='records')

        model_avito = all_dict[0]['Vendor'] + ' ' + all_dict[0]['Model'] + ' ' + all_dict[0]['MemorySize']
        if ',' in all_dict[0]['RamSize']: # содержит запятую
            ram_size = properties_dict.get('Объем оперативной памяти')
        else:
            ram_size = all_dict[0]['RamSize']
        model_avito += '/' + ram_size + ' ' + all_dict[0]['Color']

        final_dict = {
            'Title': model_avito,
            'Id': article,
            'Price': price,
            'Vendor': brand,
            'Model': all_dict[0]['Model'],
            'MemorySize': all_dict[0]['MemorySize'],
            'RamSize': ram_size,
            'Color': all_dict[0]['Color'],
            'GoodsType': 'Мобильные телефоны', # в api avito это поле имеет значение 'Мобильные телефоны'
            'Category': 'Телефоны',
        }

        return final_dict
    except Exception as e:
        logger.error(f'не понятный телефон - {stock_item_dict} - {e}')

def tablet_card(account: dict, stock_item_dict: dict, properties_dict: dict):
    pass

def smart_watch_card(account: dict, stock_item_dict: dict, properties_dict: dict):
    try:    
        brand = properties_dict.get('Бренд')
        name = stock_item_dict.get('НоменклатураНаименование')
        color = stock_item_dict.get('НоменклатураНаименование').split(' ')[-1].lower()
        price = stock_item_dict.get('Цена')
        article = stock_item_dict.get('Артикул')

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


    except Exception as e:
        logger.error(f'не понятные умные часы - {stock_item_dict} - {e}')

def wireless_headphones_card(account: dict, stock_item_dict: dict, properties_dict: dict):
    try:    
        brand = properties_dict.get('Бренд')
        name = stock_item_dict.get('НоменклатураНаименование')
        color = stock_item_dict.get('НоменклатураНаименование').split(' ')[-1].lower()
        price = stock_item_dict.get('Цена')
        article = stock_item_dict.get('Артикул')

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


    except Exception as e:
        logger.error(f'не понятные беспроводные наушники - {stock_item_dict} - {e}')

def gamepad_card(account: dict, stock_item_dict: dict, properties_dict: dict):
    pass

def console_card(account: dict, stock_item_dict: dict, properties_dict: dict):
    pass

def hair_dryer_card(account: dict, stock_item_dict: dict, properties_dict: dict):
    pass

