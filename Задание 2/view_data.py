"""
Модуль 2: Просмотр всех данных в базе данных
Запуск: python view_data.py
"""

# !/usr/bin/env python3
"""
Модуль 2: Просмотр всех данных в базе данных
Запуск: python view_data.py
"""

import sqlite3
import os


def print_table_header(table_name):
    """Вывод заголовка таблицы"""
    print("\n" + "=" * 80)
    print(f"📋 ТАБЛИЦА: {table_name.upper()}")
    print("=" * 80)


def view_all_data():
    """Просмотр всех данных в БД"""

    if not os.path.exists('enterprise.db'):
        print("✗ База данных enterprise.db не найдена!")
        return

    conn = sqlite3.connect('enterprise.db')
    cursor = conn.cursor()

    print("\n" + "=" * 80)
    print("📊 ПРОСМОТР ВСЕХ ДАННЫХ В БАЗЕ ДАННЫХ")
    print("=" * 80)

    # ==================== МАТЕРИАЛЫ (ЦЕНЫ ЗАКУПКИ) ====================
    print_table_header("Материалы (цены закупки)")
    cursor.execute("SELECT * FROM materials")
    materials = cursor.fetchall()

    print(f"{'ID':<5} {'Код':<15} {'Наименование':<30} {'Ед.':<10} {'Цена закупки':<12}")
    print("-" * 80)
    for row in materials:
        print(f"{row[0]:<5} {row[1]:<15} {row[2]:<30} {row[3]:<10} {row[4]:<12.2f}")
    print(f"\nВсего записей: {len(materials)}")

    # ==================== ПРОДУКЦИЯ (ЦЕНЫ ПРОДАЖИ) ====================
    print_table_header("Продукция (цены продажи)")
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    print(f"{'ID':<5} {'Код':<15} {'Наименование':<30} {'Ед.':<10} {'Цена продажи':<12}")
    print("-" * 80)
    for row in products:
        print(f"{row[0]:<5} {row[1]:<15} {row[2]:<30} {row[3]:<10} {row[4]:<12.2f}")
    print(f"\nВсего записей: {len(products)}")

    # ==================== СПЕЦИФИКАЦИИ ====================
    print_table_header("Спецификации (состав продукции)")
    cursor.execute("""
        SELECT 
            s.id,
            p.name as product_name,
            m.name as material_name,
            s.quantity,
            m.purchase_price,
            (s.quantity * m.purchase_price) as material_cost
        FROM specifications s
        JOIN products p ON s.product_id = p.id
        JOIN materials m ON s.material_id = m.id
        ORDER BY p.name, m.name
    """)
    specs = cursor.fetchall()

    print(f"{'ID':<5} {'Продукция':<25} {'Материал':<25} {'Кол-во':<10} {'Цена':<12} {'Стоимость':<12}")
    print("-" * 80)
    for row in specs:
        print(f"{row[0]:<5} {row[1]:<25} {row[2]:<25} {row[3]:<10} {row[4]:<12.2f} {row[5]:<12.2f}")
    print(f"\nВсего записей: {len(specs)}")

    # Расчет себестоимости продукции
    print("\n" + "=" * 80)
    print("💰 СЕБЕСТОИМОСТЬ ПРОДУКЦИИ")
    print("=" * 80)

    # ИСПРАВЛЕНИЕ: используем COALESCE для обработки NULL значений
    cursor.execute("""
        SELECT 
            p.id,
            p.name,
            p.sale_price,
            COALESCE(SUM(s.quantity * m.purchase_price), 0) as cost_price,
            (p.sale_price - COALESCE(SUM(s.quantity * m.purchase_price), 0)) as profit
        FROM products p
        LEFT JOIN specifications s ON p.id = s.product_id
        LEFT JOIN materials m ON s.material_id = m.id
        GROUP BY p.id
    """)

    costs = cursor.fetchall()
    print(f"{'ID':<5} {'Продукция':<30} {'Цена прод.':<12} {'Себест.':<12} {'Прибыль':<12}")
    print("-" * 80)
    for row in costs:
        print(f"{row[0]:<5} {row[1]:<30} {row[2]:<12.2f} {row[3]:<12.2f} {row[4]:<12.2f}")

    # ==================== ЗАКАЗЧИКИ ====================
    print_table_header("Заказчики")
    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()

    print(f"{'ID':<5} {'Наименование':<30} {'ИНН':<15} {'Телефон':<20}")
    print("-" * 80)
    for row in customers:
        # Обработка возможных None значений
        inn = row[2] if row[2] else ""
        phone = row[4] if row[4] else ""
        print(f"{row[0]:<5} {row[1]:<30} {inn:<15} {phone:<20}")
    print(f"\nВсего записей: {len(customers)}")

    # ==================== ЗАКАЗЫ ====================
    print_table_header("Заказы")
    cursor.execute("""
        SELECT 
            o.id,
            o.order_number,
            o.order_date,
            c.name as customer_name
        FROM orders o
        JOIN customers c ON o.customer_id = c.id
        ORDER BY o.order_date
    """)
    orders = cursor.fetchall()

    print(f"{'ID':<5} {'№ заказа':<10} {'Дата':<15} {'Заказчик':<30}")
    print("-" * 80)
    for row in orders:
        print(f"{row[0]:<5} {row[1]:<10} {row[2]:<15} {row[3]:<30}")
    print(f"\nВсего записей: {len(orders)}")

    # ==================== ПОЗИЦИИ ЗАКАЗОВ ====================
    print_table_header("Позиции заказов")
    cursor.execute("""
        SELECT 
            oi.id,
            o.order_number,
            p.name as product_name,
            oi.quantity,
            oi.sale_price,
            (oi.quantity * oi.sale_price) as total
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.id
        JOIN products p ON oi.product_id = p.id
        ORDER BY o.order_number, oi.id
    """)
    order_items = cursor.fetchall()

    print(f"{'ID':<5} {'Заказ':<10} {'Продукция':<30} {'Кол-во':<10} {'Цена':<10} {'Сумма':<10}")
    print("-" * 80)
    for row in order_items:
        print(f"{row[0]:<5} {row[1]:<10} {row[2]:<30} {row[3]:<10} {row[4]:<10.2f} {row[5]:<10.2f}")
    print(f"\nВсего записей: {len(order_items)}")

    # ==================== ПРОИЗВОДСТВО ====================
    print_table_header("Производство")
    cursor.execute("""
        SELECT 
            p.id,
            p.doc_number,
            p.doc_date,
            pr.name as product_name,
            p.quantity
        FROM production p
        JOIN products pr ON p.product_id = pr.id
        ORDER BY p.doc_date
    """)
    production = cursor.fetchall()

    print(f"{'ID':<5} {'№ док.':<10} {'Дата':<15} {'Продукция':<30} {'Кол-во':<10}")
    print("-" * 80)
    for row in production:
        print(f"{row[0]:<5} {row[1]:<10} {row[2]:<15} {row[3]:<30} {row[4]:<10}")
    print(f"\nВсего записей: {len(production)}")

    conn.close()

    print("\n" + "=" * 80)
    print("✅ ПРОСМОТР ЗАВЕРШЕН")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    view_all_data()