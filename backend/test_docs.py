import requests

print("=== ТЕСТИРУЕМ ДОКУМЕНТАЦИЮ API ===")

docs_urls = [
    "http://127.0.0.1:8000/swagger/",
    "http://127.0.0.1:8000/redoc/",
    "http://127.0.0.1:8000/swagger.json",
]

for url in docs_urls:
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            status = " Доступен"
        else:
            status = f" Код: {response.status_code}"
        print(f"{url}: {status}")
    except Exception as e:
        print(f"{url}: Ошибка - {e}")

print("\n=== ИНСТРУКЦИЯ ===")
print("1. Откройте http://127.0.0.1:8000/swagger/ в браузере")
print("2. Должны увидеть все эндпоинты API")
print("3. Можно тестировать API прямо в Swagger UI")
