from modules import Data_1c
import pandas as pd


def price_stores(stores: list) -> pd.DataFrame:
    data = Data_1c()
    goods = []
    for store in stores:
        goods.extend(data.stock(store))
    df = pd.DataFrame(goods)
    # Создаем DataFrame с уникальными Артикул и максимальной ценой
    # Фильтруем DataFrame, чтобы исключить строки, где 'Артикул' равен null или ''
    df_filtered = df[df['Артикул'].notnull() & (df['Артикул'] != '')]
    # Создаем DataFrame с уникальными Артикул и максимальной ценой
    df_unique = df_filtered.groupby('Артикул', as_index=False)['Цена'].max()
    return df_unique
