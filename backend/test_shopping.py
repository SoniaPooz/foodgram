import requests

url = "http://127.0.0.1:8000/api/recipes/download_shopping_cart/"
headers = {"Authorization": "Token 58cb43038b282e236b63b5c15b243c048db67bca"}

response = requests.get(url, headers=headers)
print("Status Code:", response.status_code)
print("Headers:", response.headers)
print("Content:")
print(response.text)
