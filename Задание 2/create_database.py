"""
Модуль 2: Создание базы данных
Запуск: python create_database.py
"""

import sqlite3
import os


def create_database():
    """Создание базы данных с таблицами"""

    # Создаем БД
    conn = sqlite3.connect('enterprise.db')
    cursor = conn.cursor()

    # Таблица: Материалы (с ЦЕНАМИ ЗАКУПКИ)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS materials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code VARCHAR(20) UNIQUE NOT NULL,
            name VARCHAR(100) NOT NULL,
            unit VARCHAR(10) NOT NULL,
            purchase_price DECIMAL(10, 2) NOT NULL  -- Цена закупки материала
        )
    """)

    # Таблица: Продукция (с ЦЕНАМИ ПРОДАЖИ)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code VARCHAR(20) UNIQUE NOT NULL,
            name VARCHAR(100) NOT NULL,
            unit VARCHAR(10) NOT NULL,
            sale_price DECIMAL(10, 2) NOT NULL  -- Цена продажи продукции
        )
    """)

    # Таблица: Спецификация (состав продукции - норма расхода материалов)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS specifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            material_id INTEGER NOT NULL,
            quantity DECIMAL(10, 3) NOT NULL,  -- Норма расхода материала
            FOREIGN KEY (product_id) REFERENCES products(id),
            FOREIGN KEY (material_id) REFERENCES materials(id),
            UNIQUE(product_id, material_id)
        )
    """)

    # Таблица: Заказчики
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(200) NOT NULL UNIQUE,
            inn VARCHAR(20),
            address TEXT,
            phone VARCHAR(20),
            email VARCHAR(100)
        )
    """)

    # Таблица: Заказы
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_number VARCHAR(20) NOT NULL,
            order_date DATE NOT NULL,
            customer_id INTEGER NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
    """)

    # Таблица: Позиции заказа (с ЦЕНОЙ ПРОДАЖИ на момент заказа)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            sale_price DECIMAL(10, 2) NOT NULL,  -- Цена продажи на момент заказа
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)

    # Таблица: Производство
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS production (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doc_number VARCHAR(20) NOT NULL,
            doc_date DATE NOT NULL,
            product_id INTEGER NOT NULL,
            quantity DECIMAL(10, 3) NOT NULL,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)

    conn.commit()
    conn.close()

    print("✓ База данных enterprise.db успешно создана!")
    print("✓ Созданы таблицы:")
    print("  - materials (с purchase_price)")
    print("  - products (с sale_price)")
    print("  - specifications")
    print("  - customers")
    print("  - orders")
    print("  - order_items")
    print("  - production")


if __name__ == "__main__":
    create_database()