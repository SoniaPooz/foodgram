import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/users"
headers = {"Authorization": "Token 58cb43038b282e236b63b5c15b243c048db67bca"}

print("ДЕБАГ: Смотрим структуру ответа")
response = requests.get(f"{BASE_URL}/", headers=headers)
print("Статус:", response.status_code)
print("Полный ответ:")
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
