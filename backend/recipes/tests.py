from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Recipe, Ingredient, Tag

User = get_user_model()


class RecipeAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.tag = Tag.objects.create(
            name='Тестовый тег',
            color='#FF0000',
            slug='test-tag'
        )

        self.ingredient = Ingredient.objects.create(
            name='Тестовый ингредиент',
            measurement_unit='г'
        )

        self.recipe = Recipe.objects.create(
            name='Тестовый рецепт',
            text='Описание тестового рецепта',
            cooking_time=30,
            author=self.user
        )
        self.recipe.tags.add(self.tag)

    def test_get_recipes_list(self):
        """Тест получения списка рецептов"""
        response = self.client.get('/api/recipes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_recipe(self):
        """Тест создания рецепта"""
        from django.core.files.uploadedfile import SimpleUploadedFile
        from PIL import Image
        import io

        image = io.BytesIO()
        img = Image.new('RGB', (100, 100), color='red')
        img.save(image, format='JPEG')
        image.name = 'test.jpg'
        image.seek(0)

        uploaded_image = SimpleUploadedFile(
            'test_image.jpg',
            image.getvalue(),
            content_type='image/jpeg'
        )

        data = {
            'name': 'Новый рецепт',
            'text': 'Описание нового рецепта',
            'cooking_time': 45,
            'tags': [self.tag.id],
            'ingredients': [
                {
                    'id': self.ingredient.id,
                    'amount': 100
                }
            ],
            'image': uploaded_image
        }

        response = self.client.post('/api/recipes/', data, format='multipart')

        if response.status_code != status.HTTP_201_CREATED:
            print("Ошибка создания рецепта:", response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_to_favorites(self):
        """Тест добавления в избранное"""
        response = self.client.post(f'/api/recipes/{self.recipe.id}/favorite/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_to_shopping_cart(self):
        """Тест добавления в список покупок"""
        response = self.client.post(
            f'/api/recipes/{self.recipe.id}/shopping_cart/'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class UserAPITestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)

    def test_subscribe(self):
        """Тест подписки на пользователя"""
        response = self.client.post(
            f'/api/users/{self.user2.username}/subscribe/'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
