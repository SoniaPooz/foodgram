import requests

BASE_URL = "http://127.0.0.1:8000/api/recipes"
headers = {"Authorization": "Token 58cb43038b282e236b63b5c15b243c048db67bca"}

print("=== ТЕСТИРУЕМ ПАГИНАЦИЮ ===")

# 1. Базовая пагинация
print("1. БАЗОВАЯ ПАГИНАЦИЯ")
response = requests.get(f"{BASE_URL}/", headers=headers)
if response.status_code == 200:
    data = response.json()
    print(f"Всего рецептов: {data.get('count', 'N/A')}")
    print(f"Страница: {data.get('current_page', 'N/A')}")
    print(f"Всего страниц: {data.get('total_pages', 'N/A')}")
    print(f"Рецептов на странице: {len(data.get('results', []))}")
    print(f"Следующая страница: {data.get('next', 'Нет')}")
    print(f"Предыдущая страница: {data.get('previous', 'Нет')}")

# 2. Пагинация с limit
print("\n2. ПАГИНАЦИЯ С LIMIT")
response = requests.get(f"{BASE_URL}/?limit=3", headers=headers)
if response.status_code == 200:
    data = response.json()
    print(f"Рецептов на странице: {len(data.get('results', []))}")
    print(f"Limit параметр работает: {'Да' if len(data.get('results', [])) <= 3 else 'Нет'}")

# 3. Теги без пагинации
print("\n3. ТЕГИ (БЕЗ ПАГИНАЦИИ)")
tags_url = "http://127.0.0.1:8000/api/tags"
response = requests.get(f"{tags_url}/", headers=headers)
if response.status_code == 200:
    tags = response.json()
    print(f"Тегов: {len(tags)} (должен быть список, не объект пагинации)")

# 4. Ингредиенты без пагинации
print("\n4. ИНГРЕДИЕНТЫ (БЕЗ ПАГИНАЦИИ)")
ingredients_url = "http://127.0.0.1:8000/api/ingredients"
response = requests.get(f"{ingredients_url}/", headers=headers)
if response.status_code == 200:
    ingredients = response.json()
    print(f"Ингредиентов: {len(ingredients)} (должен быть список, не объект пагинации)")

print("\n=== ТЕСТ ЗАВЕРШЕН ===")
