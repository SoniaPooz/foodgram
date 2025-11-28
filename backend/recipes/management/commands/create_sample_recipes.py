from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from recipes.models import Recipe, Tag, Ingredient, RecipeIngredient

User = get_user_model()


class Command(BaseCommand):
    help = 'Создает тестовые рецепты для сайта'

    def handle(self, *args, **kwargs):
        self.stdout.write('Создаем тестовые рецепты...')

        user, created = User.objects.get_or_create(
            username='testchef',
            defaults={
                'email': 'chef@foodgram.com',
                'first_name': 'Мария',
                'last_name': 'Иванова'
            }
        )
        if created:
            user.set_password('testpassword123')
            user.save()

        try:
            breakfast_tag = Tag.objects.get(slug='breakfast')
            lunch_tag = Tag.objects.get(slug='lunch')
            dinner_tag = Tag.objects.get(slug='dinner')
            hot_tag = Tag.objects.get(slug='hot')
        except Tag.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                'Сначала создайте теги! Запустите load_data'
            ))
            return

        try:
            flour = Ingredient.objects.get(name__icontains='мука')
            eggs = Ingredient.objects.get(name__icontains='яйцо')
            milk = Ingredient.objects.get(name__icontains='молоко')
            sugar = Ingredient.objects.get(name__icontains='сахар')
            tomato = Ingredient.objects.get(name__icontains='помидор')
            cheese = Ingredient.objects.get(name__icontains='сыр')
            chicken = Ingredient.objects.get(name__icontains='куриное филе')
            rice = Ingredient.objects.get(name__icontains='рис')
            onion = Ingredient.objects.get(name__icontains='лук репчатый')
        except Ingredient.DoesNotExist as e:
            self.stdout.write(self.style.ERROR(f'Не найден ингредиент: {e}'))
            return

        pancake_recipe, created = Recipe.objects.get_or_create(
            name='Блины с вареньем',
            author=user,
            defaults={
                'text': 'Вкусные тонкие блины с вареньем - идеальный завтрак!',
                'cooking_time': 30
            }
        )

        if created:
            pancake_recipe.tags.add(breakfast_tag, hot_tag)
            RecipeIngredient.objects.create(
                recipe=pancake_recipe, ingredient=flour, amount=200
            )
            RecipeIngredient.objects.create(
                recipe=pancake_recipe, ingredient=eggs, amount=2
            )
            RecipeIngredient.objects.create(
                recipe=pancake_recipe, ingredient=milk, amount=500
            )
            RecipeIngredient.objects.create(
                recipe=pancake_recipe, ingredient=sugar, amount=30
            )
            self.stdout.write('Создан рецепт: Блины с вареньем')

        omelette_recipe, created = Recipe.objects.get_or_create(
            name='Омлет с сыром',
            author=user,
            defaults={
                'text': 'Пышный омлет с сыром - быстро, просто и вкусно!',
                'cooking_time': 15
            }
        )

        if created:
            omelette_recipe.tags.add(breakfast_tag, lunch_tag, hot_tag)
            RecipeIngredient(
                recipe=omelette_recipe, ingredient=eggs, amount=3
            )
            RecipeIngredient.objects.create(
                recipe=omelette_recipe, ingredient=cheese, amount=100
            )
            RecipeIngredient.objects.create(
                recipe=omelette_recipe, ingredient=milk, amount=50
            )
            self.stdout.write('Создан рецепт: Омлет с сыром')

        salad_recipe, created = Recipe.objects.get_or_create(
            name='Салат из помидоров',
            author=user,
            defaults={
                'text': 'Свежий и легкий салат из спелых помидоров.',
                'cooking_time': 10
            }
        )

        if created:
            salad_recipe.tags.add(lunch_tag, dinner_tag)
            RecipeIngredient.objects.create(
                recipe=salad_recipe, ingredient=tomato, amount=300
            )
            RecipeIngredient.objects.create(
                recipe=salad_recipe, ingredient=onion, amount=1
            )
            self.stdout.write('Создан рецепт: Салат из помидоров')

        chicken_recipe, created = Recipe.objects.get_or_create(
            name='Курица с рисом',
            author=user,
            defaults={
                'text': 'Сытное и полезное блюдо - курица с рисом.',
                'cooking_time': 40
            }
        )

        if created:
            chicken_recipe.tags.add(lunch_tag, dinner_tag, hot_tag)
            RecipeIngredient.objects.create(
                recipe=chicken_recipe, ingredient=chicken, amount=500
            )
            RecipeIngredient.objects.create(
                recipe=chicken_recipe, ingredient=rice, amount=200
            )
            RecipeIngredient.objects.create(
                recipe=chicken_recipe, ingredient=onion, amount=1
            )
            self.stdout.write('Создан рецепт: Курица с рисом')

        self.stdout.write(self.style.SUCCESS('Тестовые рецепты созданы!'))
