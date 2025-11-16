import json
import os
from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Загрузка ингредиентов из JSON файла'

    def handle(self, *args, **options):
        file_path = 'data/ingredients.json'

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                ingredients_data = json.load(file)

                count = 0
                for item in ingredients_data:
                    ingredient, created = Ingredient.objects.get_or_create(
                        name=item['name'],
                        measurement_unit=item['measurement_unit']
                    )
                    if created:
                        count += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Успешно загружено {count} ингредиентов'
                    )
                )

        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'Файл {file_path} не найден')
            )
            self.stdout.write(
                self.style.ERROR('Текущая директория: ' + os.getcwd())
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка при загрузке: {e}')
            )
