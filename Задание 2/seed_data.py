"""
Модуль 2: Заполнение базы данных тестовыми данными
Запуск: python seed_data.py

ВАЖНО:
- materials.purchase_price - цена ЗАКУПКИ материала
- products.sale_price - цена ПРОДАЖИ продукции
- Себестоимость рассчитывается из specifications + materials.purchase_price
"""

import sqlite3
import os


def seed_data():
    """Заполнение БД данными из Excel файлов"""

    # Проверка наличия БД
    if not os.path.exists('enterprise.db'):
        print("✗ База данных enterprise.db не найдена!")
        print("  Сначала запустите: python create_database.py")
        return

    conn = sqlite3.connect('enterprise.db')
    cursor = conn.cursor()

    print("Заполнение базы данных...\n")

    # ==================== МАТЕРИАЛЫ (ЦЕНЫ ЗАКУПКИ) ====================
    # Из файла "Расчет стоимости продукции.xlsx"
    materials = [
        ('НФ-00000009', 'Булочка', 'шт', 25.00),  # Цена закупки
        ('НФ-00000010', 'Фарш говяжий', 'кг', 450.00),
        ('НФ-00000011', 'Помидор', 'кг', 300.00),
        ('НФ-00000012', 'Сыр чеддер', 'кг', 970.00),
        ('НФ-00000013', 'Кетчуп', 'кг', 80.00),
        ('НФ-00000014', 'Молоко нормализованное', 'кг', 34.00),
        ('НФ-00000015', 'Закваска сметанная', 'кг', 45.00),
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO materials (code, name, unit, purchase_price)
        VALUES (?, ?, ?, ?)
    """, materials)
    print(f"✓ Добавлено {len(materials)} материалов (с ценами закупки)")

    # ==================== ПРОДУКЦИЯ (ЦЕНЫ ПРОДАЖИ) ====================
    # Из файла "Заказ покупателя.xlsx" - цены продажи
    products = [
        ('НФ-00000001', 'Бургер "Двойной позитив"', 'шт', 440.00),  # Цена продажи из заказа
        ('НФ-00000002', 'Бургер "Душевный"', 'шт', 370.00),
        ('НФ-00000003', 'Бургер "Полная дичь"', 'шт', 440.00),
        ('НФ-00000004', 'Морс клюквенный 0,5л.', 'шт', 70.00),
        ('НФ-00000005', 'Латте "Ваниль" 250г.', 'шт', 210.00),
        ('НФ-00000006', 'Сок апельсиновый 1л.', 'шт', 270.00),
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO products (code, name, unit, sale_price)
        VALUES (?, ?, ?, ?)
    """, products)
    print(f"✓ Добавлено {len(products)} позиций продукции (с ценами продажи)")

    # ==================== СПЕЦИФИКАЦИИ ====================
    # Получаем ID материалов и продукции
    cursor.execute("SELECT id, code FROM materials")
    materials_dict = {code: id for id, code in cursor.fetchall()}

    cursor.execute("SELECT id, code FROM products")
    products_dict = {code: id for id, code in cursor.fetchall()}

    # Спецификация для Бургера "Двойной позитив" (НФ-00000001)
    # Из файла "Спецификация.xlsx" и "Расчет стоимости продукции.xlsx"
    specifications = [
        (products_dict['НФ-00000001'], materials_dict['НФ-00000009'], 2.0),  # Булочка - 2 шт
        (products_dict['НФ-00000001'], materials_dict['НФ-00000010'], 0.4),  # Фарш - 0.4 кг
        (products_dict['НФ-00000001'], materials_dict['НФ-00000011'], 0.06),  # Помидор - 0.06 кг
        (products_dict['НФ-00000001'], materials_dict['НФ-00000012'], 0.02),  # Сыр - 0.02 кг
        (products_dict['НФ-00000001'], materials_dict['НФ-00000013'], 0.04),  # Кетчуп - 0.04 кг
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO specifications (product_id, material_id, quantity)
        VALUES (?, ?, ?)
    """, specifications)
    print(f"✓ Добавлено {len(specifications)} спецификаций для Бургер 'Двойной позитив'")

    # ==================== ЗАКАЗЧИКИ ====================
    cursor.execute("""
        INSERT OR IGNORE INTO customers (name, inn, address, phone, email)
        VALUES (?, ?, ?, ?, ?)
    """, ('ООО "Аква-сервис"', '7701234567', 'г. Москва, ул. Водная, 15', '+7(495)123-45-67', 'info@aqua-service.ru'))
    print("✓ Добавлен заказчик ООО 'Аква-сервис'")

    # ==================== ЗАКАЗЫ ====================
    # Заказ №2 от 6 июня 2025 г.
    cursor.execute("SELECT id FROM customers WHERE name LIKE '%Аква-сервис%'")
    customer_result = cursor.fetchone()
    customer_id = customer_result[0] if customer_result else 1

    # Создаем заказ
    cursor.execute("""
        INSERT INTO orders (order_number, order_date, customer_id)
        VALUES (?, ?, ?)
    """, ('2', '2025-06-06', customer_id))

    order_id = cursor.lastrowid
    print(f"✓ Создан заказ №{order_id}")

    # Позиции заказа из файла "Заказ покупателя.xlsx"
    # sale_price - цена продажи на момент заказа
    order_items = [
        (order_id, products_dict['НФ-00000001'], 4, 440.00),  # Бургер "Двойной позитив" - 4 шт × 440
        (order_id, products_dict['НФ-00000002'], 2, 370.00),  # Бургер "Душевный" - 2 шт × 370
        (order_id, products_dict['НФ-00000004'], 6, 70.00),  # Морс клюквенный - 6 шт × 70
    ]

    cursor.executemany("""
        INSERT INTO order_items (order_id, product_id, quantity, sale_price)
        VALUES (?, ?, ?, ?)
    """, order_items)
    print(f"✓ Добавлено {len(order_items)} позиций в заказ")

    # ==================== ПРОИЗВОДСТВО ====================
    cursor.execute("""
        INSERT INTO production (doc_number, doc_date, product_id, quantity)
        VALUES (?, ?, ?, ?)
    """, ('1', '2025-06-09', products_dict['НФ-00000001'], 1.0))

    production_id = cursor.lastrowid
    print(f"✓ Создан документ производства №{production_id}")

    conn.commit()
    conn.close()

    print("\n" + "=" * 60)
    print("✓ База данных успешно заполнена!")
    print("=" * 60)
    print("\nПРИМЕР РАСЧЕТА:")
    print("Бургер 'Двойной позитив':")
    print("  - Себестоимость: 270.60 руб (из материалов)")
    print("  - Цена продажи: 440.00 руб (из прайса)")
    print("  - Прибыль: 169.40 руб")
    print("=" * 60)


if __name__ == "__main__":
    seed_data()