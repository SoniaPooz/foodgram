"""Manual API subscription tests."""
import requests

BASE_URL = "http://127.0.0.1:8000/api/users"
headers = {
    "Authorization": "Token 58cb43038b282e236b63b5c15b243c048db67bca"
}


print("=== ТЕСТИРУЕМ ПОДПИСКИ ===")

print("1. ПОЛУЧАЕМ СПИСОК ПОЛЬЗОВАТЕЛЕЙ")
response = requests.get(f"{BASE_URL}/", headers=headers)

if response.status_code == 200:
    users = response.json().get("results", [])
    print(f"Найдено пользователей: {len(users)}")

    if len(users) > 1:
        author_username = users[1]["username"]
        print(f"Автор для подписки: {author_username}")

        print("2. ПОДПИСЫВАЕМСЯ НА ДРУГОГО АВТОРА")
        subscribe_url = f"{BASE_URL}/{author_username}/subscribe/"
        response = requests.post(subscribe_url, headers=headers)
        print("Статус:", response.status_code)
        if response.status_code == 201:
            print("Успешно подписались!")
            print("Данные:", response.json())
        elif response.status_code == 400:
            print("Ошибка:", response.json())
        else:
            print("Текст ответа:", response.text)

        print("3. ПОЛУЧАЕМ СПИСОК ПОДПИСОК")
        response = requests.get(f"{BASE_URL}/subscriptions/", headers=headers)
        print("Статус:", response.status_code)
        if response.status_code == 200:
            subscriptions = response.json()
            results = subscriptions.get("results", [])
            print(f"Количество подписок: {len(results)}")

        print("4. ОТПИСЫВАЕМСЯ ОТ АВТОРА")
        response = requests.delete(subscribe_url, headers=headers)
        print("Статус:", response.status_code)
        if response.status_code == 204:
            print("Успешно отписались!")
        else:
            print("Текст ответа:", response.text)

    else:
        print("Не найдено других пользователей для подписки")
else:
    print("Ошибка при получении пользователей:", response.status_code)
