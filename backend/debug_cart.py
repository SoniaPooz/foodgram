import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"
headers = {"Authorization": "Token 58cb43038b282e236b63b5c15b243c048db67bca"}

print("=== ДИАГНОСТИКА КОРЗИНЫ ===")

# 1. Получаем рецепт
print("1. ПОЛУЧАЕМ РЕЦЕПТЫ")
response = requests.get(f"{BASE_URL}/recipes/", headers=headers)
if response.status_code == 200:
    recipes = response.json().get("results", [])
    if recipes:
        recipe_id = recipes[0]["id"]
        recipe_name = recipes[0]["name"]
        print(f"Рецепт: {recipe_name} (ID: {recipe_id})")
        
        # 2. Пробуем добавить в корзину
        print("\n2. ДОБАВЛЯЕМ В КОРЗИНУ")
        response = requests.post(f"{BASE_URL}/recipes/{recipe_id}/shopping_cart/", headers=headers)
        print(f"Статус: {response.status_code}")
        print(f"Ответ: {response.text}")
        
        if response.status_code == 400:
            print("\n3. ДЕТАЛИ ОШИБКИ:")
            try:
                error_data = response.json()
                print(json.dumps(error_data, indent=2, ensure_ascii=False))
            except:
                print("Не удалось распарсить JSON ошибки")
    else:
        print("Нет рецептов для тестирования")
else:
    print(f"Ошибка получения рецептов: {response.status_code}")
