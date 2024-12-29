-- Schema for the SQLite database
CREATE TABLE IF NOT EXISTS stores (
    key INTEGER PRIMARY KEY AUTOINCREMENT,
    store TEXT,
    AvitoId TEXT, 
    Id TEXT UNIQUE,
    Title TEXT, 
    Vendor TEXT, 
    ImageUrls TEXT,
    VideoURL TEXT,
    Price REAL, 
    GoodsType TEXT, 
    Color TEXT, 
    Description TEXT, 
    Condition TEXT, 
    ContactPhone TEXT, 
    AdType TEXT, 
    Model TEXT, 
    Category TEXT, 
    Address TEXT, 
    RamSize TEXT, 
    MemorySize TEXT, 
    ManagerName TEXT, 
    Box_Sealed TEXT,
    ProductType TEXT,
    ProductSubType TEXT,
    Brand TEXT,
    Gender TEXT,
    StrapType TEXT
);

CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_code TEXT UNIQUE NOT NULL,
    product_article TEXT UNIQUE NOT NULL,
    brand TEXT,
    type TEXT
);

CREATE TABLE IF NOT EXISTS product_properties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    value TEXT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE
);

-- Таблица для телефонов Avito
CREATE TABLE IF NOT EXISTS avito_phones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Vendor TEXT,
    Model TEXT,
    MemorySize TEXT,
    Color TEXT,
    RamSize TEXT
);

-- Таблица для планшетов Avito
CREATE TABLE IF NOT EXISTS avito_tablets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Brand TEXT,
    Model TEXT,
    MemorySize TEXT,
    SimSlot TEXT,
    RamSize TEXT,
    Color TEXT
);
