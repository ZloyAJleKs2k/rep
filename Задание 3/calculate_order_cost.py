"""
Модуль 3: Расчет стоимости заказа
Запуск: python calculate_order_cost.py

РАСЧЕТЫ:
1. Себестоимость продукции = SUM(материал.quantity × material.purchase_price)
2. Сумма заказа = SUM(order_item.quantity × order_item.sale_price)
3. Прибыль = Сумма заказа - Себестоимость
"""

import sqlite3


def calculate_product_cost(product_id):
    """
    Расчет СЕБЕСТОИМОСТИ продукции
    на основе стоимости материалов и нормы расхода
    """

    conn = sqlite3.connect('../Задание 2/enterprise.db')
    cursor = conn.cursor()

    query = """
    SELECT 
        p.id,
        p.name,
        SUM(s.quantity * m.purchase_price) as cost
    FROM products p
    JOIN specifications s ON p.id = s.product_id
    JOIN materials m ON s.material_id = m.id
    WHERE p.id = ?
    GROUP BY p.id
    """

    cursor.execute(query, (product_id,))
    result = cursor.fetchone()
    conn.close()

    return result


def get_order_with_costs(order_id):
    """
    Получение заказа с расчетом:
    - Сумма заказа (по ценам продажи)
    - Себестоимость продукции
    - Прибыль
    """

    conn = sqlite3.connect('../Задание 2/enterprise.db')
    cursor = conn.cursor()

    # Основная информация о заказе
    query_order = """
    SELECT 
        o.id,
        o.order_number,
        o.order_date,
        c.name as customer_name
    FROM orders o
    JOIN customers c ON o.customer_id = c.id
    WHERE o.id = ?
    """

    cursor.execute(query_order, (order_id,))
    order_info = cursor.fetchone()

    # Позиции заказа с ценами продажи
    query_items = """
    SELECT 
        oi.id,
        p.name as product_name,
        oi.quantity,
        oi.sale_price,
        (oi.quantity * oi.sale_price) as item_total
    FROM order_items oi
    JOIN products p ON oi.product_id = p.id
    WHERE oi.order_id = ?
    """

    cursor.execute(query_items, (order_id,))
    order_items = cursor.fetchall()

    # Себестоимость каждой позиции
    query_costs = """
    SELECT 
        p.id as product_id,
        p.name,
        SUM(s.quantity * m.purchase_price) as unit_cost
    FROM products p
    JOIN specifications s ON p.id = s.product_id
    JOIN materials m ON s.material_id = m.id
    GROUP BY p.id
    """

    cursor.execute(query_costs)
    product_costs = {row[0]: {'name': row[1], 'unit_cost': row[2]} for row in cursor.fetchall()}

    conn.close()

    return order_info, order_items, product_costs


def display_order_report(order_id):
    """Отображение полного отчета по заказу"""

    print(f"\n{'=' * 100}")
    print(f"ОТЧЕТ ПО ЗАКАЗУ №{order_id}")
    print(f"{'=' * 100}\n")

    order_info, order_items, product_costs = get_order_with_costs(order_id)

    if not order_info:
        print("Заказ не найден!")
        return

    order_id_db, order_number, order_date, customer = order_info

    print(f"№ заказа: {order_number}")
    print(f"Дата: {order_date}")
    print(f"Заказчик: {customer}")
    print(f"\n{'=' * 100}\n")

    print(f"{'№':<5} {'Продукция':<35} {'Кол-во':<10} {'Цена прод.':<12} {'Сумма':<12} {'Себест.':<12} {'Прибыль':<12}")
    print("-" * 100)

    total_sale = 0
    total_cost = 0
    total_profit = 0

    for item in order_items:
        item_id, product_name, qty, sale_price, item_total = item

        # Получаем себестоимость
        cost_info = product_costs.get(item_id, {'unit_cost': 0})
        unit_cost = cost_info['unit_cost']
        item_cost = qty * unit_cost
        item_profit = item_total - item_cost

        print(
            f"{item_id:<5} {product_name:<35} {qty:<10} {sale_price:<12.2f} {item_total:<12.2f} {item_cost:<12.2f} {item_profit:<12.2f}")

        total_sale += item_total
        total_cost += item_cost
        total_profit += item_profit

    print(f"{'ИТОГО:':<50} {total_sale:<12.2f} {total_cost:<12.2f} {total_profit:<12.2f}")

    print(f" ВЫРУЧКА: {total_sale:.2f} руб.")
    print(f" СЕБЕСТОИМОСТЬ: {total_cost:.2f} руб.")
    print(f" ПРИБЫЛЬ: {total_profit:.2f} руб.")



if __name__ == "__main__":
    # Тестовый запуск
    order_id = input("Введите ID заказа: ")
    try:
        display_order_report(int(order_id))
    except ValueError:
        print("✗ Ошибка: введите корректный номер заказа (число)")