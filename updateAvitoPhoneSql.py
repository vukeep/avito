# Парсинг XML файла и вставка данных в базу данных
# файл phones.xml должен быть в корне проекта
# вставляет данные в таблицу avito_phones

import os
import xml.etree.ElementTree as ET
import requests
import sqlite3
from db.db_handler import DatabaseHandler

def save_xml_to_file(url, output_file):
    # Загружаем XML-данные
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Ошибка загрузки данных: {response.status_code}")
    
    # Сохраняем содержимое в файл
    with open(output_file, "wb") as f:
        f.write(response.content)
    print(f"Данные успешно сохранены в {output_file}")



def phones_parse_xml(file_path):
    # Парсинг XML файла
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    data = []
    for vendor in root.findall('Vendor'):
        vendor_name = vendor.get('name')
        for model in vendor.findall('Model'):
            model_name = model.get('name')
            for memory in model.findall('MemorySize'):
                memory_size = memory.get('name')
                for color in memory.findall('Color'):
                    color_name = color.get('name')
                    ram_sizes = [ram.get('name') for ram in color.findall('RamSize')]
                    data.append((vendor_name, model_name, memory_size, color_name, ram_sizes))
    return data

def phones_setup_database(db_handler):
    # Подключение к базе данных через наш handler
    conn = sqlite3.connect(db_handler.db_path)
    cursor = conn.cursor()
    
    # Создаем таблицу avito_phones, если она не существует
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS avito_phones (
            Vendor TEXT,
            Model TEXT,
            MemorySize TEXT,
            Color TEXT,
            RamSize TEXT
        )
    ''')
    conn.commit()
    
    # Очистка таблицы
    cursor.execute('DELETE FROM avito_phones')
    conn.commit()
    
    return conn, cursor

def phones_insert_data(cursor, data):
    # Вставка данных в таблицу
    for vendor, model, memory, color, ram_sizes in data:
        ram_sizes_str = ', '.join(ram_sizes)
        cursor.execute('''
            INSERT INTO avito_phones (Vendor, Model, MemorySize, Color, RamSize)
            VALUES (?, ?, ?, ?, ?)
        ''', (vendor, model, memory, color, ram_sizes_str))
    cursor.connection.commit()

def phones_main():
    file_name = 'phones.xml'
    url = "https://autoload.avito.ru/format/phone_catalog.xml"

    save_xml_to_file(url, file_name)
    
    # Создаем экземпляр DatabaseHandler
    db_handler = DatabaseHandler()
    
    data = phones_parse_xml(file_name)
    conn, cursor = phones_setup_database(db_handler)
    phones_insert_data(cursor, data)
    
    cursor.close()
    conn.close()


def tablets_parse_xml(file_path):
    # Парсинг XML файла
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    data = []
    for brand in root.findall('Brand'):
        brand_name = brand.get('name')
        for model in brand.findall('Model'):
            model_name = model.get('name')
            for memory in model.findall('MemorySize'):
                memory_size = memory.get('name')
                for sim in memory.findall('SimSlot'):
                    sim_slot = sim.get('name')
                    for ram in sim.findall('RamSize'):
                        ram_size = ram.get('name')
                        for color in ram.findall('Color'):
                            color_name = color.get('name')
                            data.append((brand_name, model_name, memory_size, sim_slot, ram_size, color_name))
    return data

def tablets_setup_database(db_handler):
    conn = sqlite3.connect(db_handler.db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS avito_tablets (
            Brand TEXT,
            Model TEXT,
            MemorySize TEXT,
            SimSlot TEXT,
            RamSize TEXT,
            Color TEXT
        )
    ''')
    conn.commit()
    
    cursor.execute('DELETE FROM avito_tablets')
    conn.commit()
    
    return conn, cursor

def tablets_insert_data(cursor, data):
    # Вставка данных в таблицу
    for brand, model, memory, sim_slot, ram_size, color in data:
        cursor.execute('''
            INSERT INTO avito_tablets (Brand, Model, MemorySize, SimSlot, RamSize, Color)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (brand, model, memory, sim_slot, ram_size, color))
    cursor.connection.commit()

def tablets_main():
    file_name = 'tablets.xml'
    url = "https://autoload.avito.ru/format/tablets.xml"

    save_xml_to_file(url, file_name)
    
    # Создаем экземпляр DatabaseHandler
    db_handler = DatabaseHandler()
    
    data = tablets_parse_xml(file_name)
    conn, cursor = tablets_setup_database(db_handler)
    tablets_insert_data(cursor, data)
    
    cursor.close()
    conn.close()

def main():
    phones_main()
    tablets_main()

if __name__ == '__main__':
    main()