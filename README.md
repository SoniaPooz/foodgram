### Адрес сайта: https://fooodgram.ddns.net/recipes

## Описание проекта

**Foodgram** - веб-приложение для публикации кулинарных рецептов. Пользователи могут создавать рецепты, добавлять их в избранное, подписываться на других авторов и формировать список покупок для выбранных рецептов.

## Основные функции

### Публичная часть
- **Главная страница** - список рецептов с пагинацией
- **Страница рецепта** - полное описание с ингредиентами и шагами приготовления
- **Страница автора** - все рецепты конкретного пользователя
- **Фильтрация** - по тегам (завтрак, обед, ужин)

### Личный кабинет
- **Создание рецептов** - с добавлением фото, ингредиентов и шагов приготовления
- **Редактирование** - изменение собственных рецептов
- **Избранное** - сохранение понравившихся рецептов
- **Список покупок** - генерация PDF-файла с необходимыми ингредиентами
- **Подписки** - лента рецептов от авторов, на которых подписан пользователь

## Технологический стек

### Backend
- **Python 3.9+** - основной язык программирования
- **Django 3.2+** - веб-фреймворк
- **Django REST Framework** - API
- **PostgreSQL** - база данных
- **Docker** - контейнеризация
- **Nginx** - веб-сервер и прокси
- **Gunicorn** - WSGI-сервер

### Frontend
- **React** - пользовательский интерфейс
- **JavaScript (ES6+)** 
- **HTML5/CSS3**
- **Webpack** - сборка проекта

## Развертывание проекта

### Предварительные требования
- Docker
- Docker Compose
- Доменное имя (для HTTPS)

### 1. Клонирование репозитория
```bash
git clone <URL-репозитория>
cd foodgram

##  как заполнить env

# Django
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=your-domain.com,localhost,127.0.0.1

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=foodgram
POSTGRES_USER=foodgram_user
POSTGRES_PASSWORD=your-password
DB_HOST=db
DB_PORT=5432

# Static files
STATIC_URL=/static/
STATIC_ROOT=/app/staticfiles
MEDIA_URL=/media/
MEDIA_ROOT=/app/media

# SSL
SSL_CERT_PATH=/etc/letsencrypt/live/your-domain.com/fullchain.pem
SSL_KEY_PATH=/etc/letsencrypt/live/your-domain.com/privkey.pem

## Автор
[Софья Пузикова](https://github.com/SoniaPooz)