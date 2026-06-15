#!/usr/bin/env python3
"""
Модуль 2: Импорт заказчиков из JSON
Запуск: python import_customers.py
"""

import sqlite3
import json
import os


def import_customers():
    """Импорт данных из customers.json"""

    json_file = 'data/Заказчики.json'

    if not os.path.exists(json_file):
        print(f"✗ Файл {json_file} не найден!")
        return

    # Чтение JSON
    with open(json_file, 'r', encoding='utf-8') as f:
        customers = json.load(f)

    # Подключение к БД
    conn = sqlite3.connect('enterprise.db')
    cursor = conn.cursor()

    # Импорт
    count_added = 0
    count_skipped = 0

    for customer in customers:
        name = customer.get('name')

        # ПРОВЕРКА: существует ли уже заказчик с таким именем
        cursor.execute("""
            SELECT id FROM customers WHERE name = ?
        """, (name,))

        existing = cursor.fetchone()

        if existing:
            print(f" Заказчик '{name}' уже существует (ID={existing[0]}). Пропущен.")
            count_skipped += 1
            continue

        # Вставка нового заказчика
        try:
            cursor.execute("""
                INSERT INTO customers (name, inn, address, phone, email)
                VALUES (?, ?, ?, ?, ?)
            """, (
                name,
                customer.get('inn', ''),
                customer.get('addres', ''),  # В JSON поле называется 'addres' (с одной 's')
                customer.get('phone', ''),
                customer.get('email', '')  # В JSON может не быть email
            ))
            count_added += 1
            print(f"✓ Добавлен: {name}")

        except sqlite3.IntegrityError as e:
            print(f"✗ Ошибка при добавлении '{name}': {e}")
            count_skipped += 1

    conn.commit()
    conn.close()

    print("\n" + "=" * 60)
    print(f"✓ Импортировано: {count_added} заказчиков")
    print(f"⊘ Пропущено (дубликаты): {count_skipped}")
    print("=" * 60)


if __name__ == "__main__":
    import_customers()