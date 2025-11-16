import requests

BASE_URL = "http://127.0.0.1:8000/api/recipes"
headers = {"Authorization": "Token 58cb43038b282e236b63b5c15b243c048db67bca"}

# Получим список рецептов чтобы узнать ID
print("=== GET RECIPES ===")
response = requests.get(f"{BASE_URL}/", headers=headers)
if response.status_code == 200:
    recipes = response.json().get('results', [])
    if recipes:
        recipe_id = recipes[0]['id']
        print(f"Found recipe ID: {recipe_id}")
 
        # Добавить в избранное
        print("\n=== ADD TO FAVORITE ===")
        response = requests.post(f"{BASE_URL}/{recipe_id}/favorite/", headers=headers)
        print("Status:", response.status_code)
        if response.status_code in [200, 201]:
            print("Response:", response.json())

        # Удалить из избранного
        print("\n=== DELETE FROM FAVORITE ===")
        response = requests.delete(f"{BASE_URL}/{recipe_id}/favorite/", headers=headers)
        print("Status:", response.status_code)
    else:
        print("No recipes found!")
else:
    print("Error getting recipes:", response.status_code)
