import requests
import json


def get_email_data():
    """Получение данных от эмулятора"""
    url = "http://localhost:4444/TransferSimulator/email"

    try:
        response = requests.get(url, timeout=5)

        if response.status_code == 500:
            print(" Ошибка 500: Internal Server Error")
            print("Обратитесь к эксперту!")
            return None

        response.raise_for_status()
        data = response.json()

        print("=" * 60)
        print("Полученные данные от эмулятора:")
        print("=" * 60)
        print(f"Сырой JSON: {json.dumps(data, ensure_ascii=False, indent=2)}")
        print(f"\nЗначение поля 'value': {data.get('value', '')}")
        print("=" * 60)

        return data

    except requests.exceptions.ConnectionError:
        print(" Не удалось подключиться к эмулятору")
        print("Убедитесь, что TransferSimulator.exe запущен")
    except Exception as e:
        print(f" Ошибка: {e}")

    return None


if __name__ == "__main__":
    print("Тестирование API эмулятора\n")

    # Запрашиваем данные несколько раз
    for i in range(50):
        print(f"\n--- Запрос #{i + 1} ---")
        get_email_data()
        # input("\nНажмите Enter для следующего запроса...")