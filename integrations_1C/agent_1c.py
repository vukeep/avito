import pandas as pd
from integrations_1C import Data_1c

class Client_1c:
    def __init__(self):
        self.data = Data_1c()

    def get_stock(self, id_stores: list) -> pd.DataFrame:
        '''
        Внимание << Установлено ограничение на цену в 4000 рублей >>

        Получение остатков и цен на товары
        :param id_stores: Список ID складов
        :return: DataFrame с Номенклатура, НоменклатураНаименование, Артикул, НоменклатураКод, КоличествоОстаток, Цена
        '''
        all_df = pd.DataFrame()

        for id_store in id_stores:
            result = self.data.stock(id_store)
            df = pd.DataFrame(result)
            all_df = pd.concat([all_df, df], ignore_index=True)

        # Удаляем все строки, где Артикул равен None или пустой строке
        all_df = all_df[all_df['Артикул'].notna() & (all_df['Артикул'] != '')]

        # Удаляем все строки, где цена меньше 4000
        all_df = all_df[all_df['Цена'] >= 4000]
        
        # Группируем по Номенклатуре и суммируем КоличествоОстаток, если цена одинаковая
        all_df = all_df.groupby(['Номенклатура', 'Цена'], as_index=False).agg({
            'КоличествоОстаток': 'sum',
            'НоменклатураНаименование': 'first',
            'Артикул': 'first',
            'НоменклатураКод': 'first'
        })

        return all_df

    def get_goods_stock(self, id_goods: list, id_stores: list) -> pd.DataFrame:
        '''
        Получение остатков товаров по складам
        :param id_goods: Список ID товаров
        :param id_stores: Список ID складов
        :return: DataFrame с ID товара, Количество, Наименование товара
        '''

        result = self.data.goods_stock(id_goods)
        # Преобразуем результат в DataFrame
        df = pd.DataFrame(result)

        # Разворачиваем вложенные словари в столбце 'Остатки'
        df = df.explode('Остатки').reset_index(drop=True)

        # Преобразуем столбец 'Остатки' из словарей в отдельные столбцы
        df = pd.concat([df.drop(['Остатки'], axis=1), df['Остатки'].apply(pd.Series)], axis=1)

        # Фильтруем результат по списку складов
        df = df[df['Склад'].isin(id_stores)]

        # Переименовываем столбцы для удобства
        df.rename(columns={
            'Номенклатура': 'ID товара',
            'НоменклатураНаименование': 'Наименование товара',
            'Склад': 'ID склада',
            'СкладНаименование': 'Наименование склада',
            'Остаток': 'Количество'
        }, inplace=True)

        

        # Группируем по ID товара и суммируем количество, не учитывая склады
        df = df.groupby('ID товара', as_index=False).agg({
            'Количество': 'sum',
            'Наименование товара': 'first'
        })

        return df


if __name__ == '__main__':
    from data.accounts import accounts
    from data.stores import stores  

    client_1c = Client_1c()

    store_name = accounts[0]['iSmartChita']['stores']
    # Получаем значения словаря из списка store_name, используя их как ключи в stores
    id_stores = [stores[store]['Ссылка'] for store in store_name]
    df = client_1c.get_stock(id_stores)
    # Получаем статистику по датафрейму
    id_goods =[ '01b9e385-5b75-11ef-9194-005056012869', '0242ac1e-8d32-11ec-9fe7-005056011012', '02734ac8-e8be-11e4-8c42-005056b4177e', 'ff2bcfd8-fb8c-11ee-9191-005056012869']
    #df = client_1c.get_goods_stock(id_goods, id_stores)
    
    # Фильтруем DataFrame по значению в колонке 'Артикул'
    df = df[df['Артикул'] == 'MPUD3AH-A']
    
    result = df

    print(df)