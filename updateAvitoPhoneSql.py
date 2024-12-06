# Парсинг XML файла и вставка данных в базу данных
# файл phones.xml должен быть в корне проекта
# вставляет данные в таблицу avito_phones

import os
import dotenv

import xml.etree.ElementTree as ET
import pyodbc

dotenv.load_dotenv()

db_server = os.getenv('DB_SERVER')
db_database = os.getenv('DB_DATABASE')
db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
db_driver = os.getenv('DB_DRIVER')

def parse_xml(file_path):
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

def setup_database(connection_string):
    # Подключение к базе данных
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    
    # Проверка и создание таблицы, если она не существует
    cursor.execute('''
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='avito_phones' AND xtype='U')
        CREATE TABLE avito_phones (
            Vendor NVARCHAR(255),
            Model NVARCHAR(255),
            MemorySize NVARCHAR(255),
            Color NVARCHAR(255),
            RamSize NVARCHAR(MAX)
        )
    ''')
    conn.commit()
    
    # Очистка таблицы
    cursor.execute('DELETE FROM avito_phones')
    conn.commit()
    
    return conn, cursor

def insert_data(cursor, data):
    # Вставка данных в таблицу
    for vendor, model, memory, color, ram_sizes in data:
        ram_sizes_str = ', '.join(ram_sizes)
        cursor.execute('''
            INSERT INTO avito_phones (Vendor, Model, MemorySize, Color, RamSize)
            VALUES (?, ?, ?, ?, ?)
        ''', (vendor, model, memory, color, ram_sizes_str))
    cursor.connection.commit()

def main():
    file_path = 'phones.xml'  # Путь к вашему XML файлу
    connection_string = f'DRIVER={db_driver};SERVER={db_server};DATABASE={db_database};UID={db_username};PWD={db_password}'
    
    data = parse_xml(file_path)
    conn, cursor = setup_database(connection_string)
    insert_data(cursor, data)
    
    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()