from django.urls import path

app_name = 'api'

urlpatterns = [
    path('', lambda request: {"message": "Foodgram API is working!"}),
]
