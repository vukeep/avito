from modules.dataForProcessing import update_mobicom_data
from info.accountData import accounts, stores
from avito_api import AvitoAPIClient
from datetime import datetime, timedelta
from bd import DatabaseHandler
from modules.dataForProcessing import stock_stores
from modules import CloudinaryClient
from modules import price_stores, update_price_avito

# Вычисляем текущую дату в формате гггг-мм-ддTчч:мм:сс
current_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
db_handler = DatabaseHandler()
cloudinary_client = CloudinaryClient()


def id_last_successful_download(data: dict):
    '''
    Функция для получения последнего файла загрузки Avito
    - получаем список всех загрузок из api avito
    - забираем id последней загрузки
    '''
    client = AvitoAPIClient(data['client_id'], data['client_secret'])
    reports_data = client.autoload.get_reports(
        date_from=(datetime.now() - timedelta(days=14)).strftime('%Y-%m-%dT%H:%M:%S'),
        date_to=current_date
    )
    # Фильтруем отчеты с 'status': 'success'
    success_reports = [report for report in reports_data['reports'] if report['status'] == 'success']

    # Сортируем по 'started_at' в обратном порядке (от последнего к первому)
    success_reports.sort(key=lambda x: x['started_at'], reverse=True)

    # Получаем id последнего отчета
    last_success_id = success_reports[0]['id']

    return client, last_success_id


def get_last_report_data(client: AvitoAPIClient, id : int):
    '''
    Функция для получения данных последней загрузки Avito
    - получаем данные по id загрузки
    - возвращаем данные в виде списка словарей {'ad_id': '194252169544', 'avito_id': 4303760546, 'avito_date_end': '2024-11-19T08:37:05.107000+03:00', 'avito_status': 'old'}
    '''
    # Получаем данные последнего отчета
    last_report_data = client.autoload.get_report_items(id)
    for item in last_report_data:
        item.pop('section')
        item.pop('url')
        item.pop('messages')
    return last_report_data

def update_avito_id(db_handler: DatabaseHandler, record_list: list):
    # Преобразуем список словарей вида {'ad_id': '194252169544', 'avito_id': 4303760546, 'avito_date_end': '2024-11-19T08:37:05.107000+03:00', 'avito_status': 'old'}
    # в список словарей вида {'Id': '194252169544', 'AvitoId': '4303760546'}
    transformed_records = [{'Id': item['ad_id'], 'AvitoId': item['avito_id']} for item in record_list]
    
    # Обновляем значение AvitoId в базе по ключу Id
    db_handler.update_avito_id(transformed_records)

def update_mobicom_data_db(account: dict): 
    '''
    Обновляем имеющиеся id, добавляя к ним avito id
    '''
    store = list(account.keys())[0] # Получаем название магазина
    client = AvitoAPIClient(account[store]['client_id'], account[store]['client_secret'])
    # получаем все id не имеющие avito id
    id_without_avito_id = db_handler.get_id_mobicom(store)
    
    if id_without_avito_id:
        str_id_mobicom = ','.join(str(id[0]) for id in id_without_avito_id) # преобразуем список в строку
        report_items = client.autoload.get_report_items_idMobicom(str_id_mobicom) # получаем данные по id avito для id mobicom
        record_dict = [{'Id': item.get('ad_id'), 'AvitoId': item.get('avito_id')} for item in report_items.get('items')] # преобразуем данные в словарь
        db_handler.update_avito_id(record_dict, store) # обновляем avito id в базе

def creation_exchange_file(account: dict):
    '''
    Обновляем базу данных, добавляя новые записи о товарах
    '''
    update_mobicom_data_db(account) # Обновляем имеющиеся id, добавляя к ним avito id

    account_key = list(account.keys())[0] # Получаем название магазина

    records_df = db_handler.get_records_by_store(account_key) # Получаем список карточек для магазина
    stock = stock_stores(account[account_key]['stores']) # Получаем остатки из базы по магазину
    # Фильтруем DataFrame stock по столбцу 'Артикул', исключая значения из столбца 'id' DataFrame records_df
    if records_df is not None and len(records_df) > 0:
        filtered_stock = stock[~stock['Артикул'].isin(records_df['Id'])]
    else:
        filtered_stock = stock
    # Ограничиваем filtered_stock двумя строками для повышения производительности
    # filtered_stock = filtered_stock.head(2)
    avito_data = update_mobicom_data(filtered_stock)

    # убираем все строки None
    avito_data = [item for item in avito_data if item is not None]

    # Обновляем данные в базе
    for item in avito_data:
        try:
            article = item.get('Id')
        except:
            print(f'{item} - не понятно что это')
            continue
        url = cloudinary_client.url_to_string(article)
        if "http://res.cloudinary.com/avitophoto/image" not in url: # проверяем есть ли в строке текст http://res.cloudinary.com/avitophoto/image
            print(f'{item} - нет изображения')
            continue
        item['ImageUrls'] = url
        item['store'] = account_key
        data_details = account[account_key]['data_details']
        for key, value in data_details.items():
            item[key] = value

        db_handler.add_record(item)
    # Сохраняем данные в файл с указанием кодировки UTF-8
    update_price_mobicom(account) # Обновляем цены в базе данных
    new_records_df = db_handler.get_records_by_store(account_key) # Получаем обновленный список карточек для магазина
    # фильтруем карточки по столбцу 'Артикул', оставляя только те, которые есть в остатках
    filtered_records_df = new_records_df[new_records_df['Id'].isin(stock['Артикул'])]
    filtered_records_df.to_csv(f'{account_key}.csv', index=False, encoding='utf-8')

def update_price_mobicom(account: dict):
    '''
    Обновляем цены в базе данных
    '''
    store = list(account.keys())[0] # Получаем название магазина
    name_store = account[store]['stores']
    store_code = []
    price_list = []
    for name in name_store:
        store_code.append(stores[name]['Ссылка'])
    # Получаем DataFrame с ценами для магазинов
    price_df = price_stores(store_code)
    
    # Обновляем цены в базе данных
    for index, row in price_df.iterrows():
        article_id = row['Артикул']
        new_price = row['Цена']
        
        # Обновляем цену в базе данных для данного id
        db_handler.update_price(article_id, new_price, store)
        price_list.append((article_id, new_price))
    return price_list



def update_price_avito_store(account: dict):
    '''
    Обновляем цены на avito
    '''
    price_list = update_price_mobicom(account)
    update_price_avito(price_list, account) 

        


if __name__ == "__main__":

    for account in accounts:
        
        creation_exchange_file(account) 
        # update_price_avito_store(account)


