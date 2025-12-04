"""Manual API favorite tests."""
import requests

BASE_URL = "http://127.0.0.1:8000/api/recipes"
headers = {
    "Authorization": "Token 58cb43038b282e236b63b5c15b243c048db67bca"
}


print("=== ТЕСТИРУЕМ ФИЛЬТРАЦИЮ РЕЦЕПТОВ ===")

# 1. Все рецепты
print("1. ВСЕ РЕЦЕПТЫ")
response = requests.get(f"{BASE_URL}/", headers=headers)
if response.status_code == 200:
    data = response.json()
    recipes = data.get("results", [])
    print(f"Всего рецептов: {len(recipes)}")
    for recipe in recipes:
        print(f"  - {recipe['name']} (ID: {recipe['id']})")

# 2. Рецепты в избранном
print("\n2. РЕЦЕПТЫ В ИЗБРАННОМ")
response = requests.get(f"{BASE_URL}/?is_favorited=1", headers=headers)
if response.status_code == 200:
    data = response.json()
    favorites = data.get("results", [])
    print(f"Рецептов в избранном: {len(favorites)}")
    for recipe in favorites:
        print(f"  - {recipe['name']}")

# 3. Рецепты в списке покупок
print("\n3. РЕЦЕПТЫ В СПИСКЕ ПОКУПОК")
response = requests.get(f"{BASE_URL}/?is_in_shopping_cart=1", headers=headers)
if response.status_code == 200:
    data = response.json()
    cart = data.get("results", [])
    print(f"Рецептов в списке покупок: {len(cart)}")
    for recipe in cart:
        print(f"  - {recipe['name']}")

# 4. Фильтр по автору
print("\n4. ФИЛЬТР ПО АВТОРУ")
response = requests.get(f"{BASE_URL}/?author=1", headers=headers)
if response.status_code == 200:
    data = response.json()
    author_recipes = data.get("results", [])
    print(f"Рецептов автора ID=1: {len(author_recipes)}")
    for recipe in author_recipes:
        print(f"  - {recipe['name']}")

# 5. Тестируем ингредиенты
print("\n5. ФИЛЬТРАЦИЯ ИНГРЕДИЕНТОВ")
ingredients_url = "http://127.0.0.1:8000/api/ingredients"
response = requests.get(f"{ingredients_url}/?name=му", headers=headers)
if response.status_code == 200:
    ingredients = response.json()
    print(f"Найдено ингредиентов: {len(ingredients)}")
    for ing in ingredients:
        print(f"  - {ing['name']} ({ing['measurement_unit']})")

print("\n=== ТЕСТ ЗАВЕРШЕН ===")
