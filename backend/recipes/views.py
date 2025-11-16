from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import RecipePageNumberPagination
from django.shortcuts import get_object_or_404

from .models import Tag, Ingredient, Recipe, Favorite, ShoppingCart
from .serializers import (
    TagSerializer, IngredientSerializer, RecipeSerializer,
    ShoppingCartSerializer
)
from .filters import RecipeFilter, IngredientFilter


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = RecipePageNumberPagination

    def get_queryset(self):
        """Оптимизированный queryset с prefetch_related и select_related"""
        queryset = Recipe.objects.select_related('author').prefetch_related(
            'tags',
            'ingredients',
            'recipe_ingredients__ingredient'
        )
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk=None):
        recipe = self.get_object()

        if request.method == 'POST':
            favorite, created = Favorite.objects.get_or_create(
                user=request.user,
                recipe=recipe
            )
            if created:
                from .serializers import RecipeShortSerializer
                serializer = RecipeShortSerializer(recipe)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            return Response(
                {'errors': 'Рецепт уже в избранном'},
                status=status.HTTP_400_BAD_REQUEST
            )

        elif request.method == 'DELETE':
            favorite = Favorite.objects.filter(
                user=request.user,
                recipe=recipe
            )
            if favorite.exists():
                favorite.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'errors': 'Рецепт не в избранном'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)

        if request.method == 'POST':
            cart_item, created = ShoppingCart.objects.get_or_create(
                user=request.user,
                recipe=recipe
            )
            if created:
                serializer = ShoppingCartSerializer(
                    cart_item,
                    context={'request': request}
                )
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            return Response(
                {'errors': 'Рецепт уже в списке покупок'},
                status=status.HTTP_400_BAD_REQUEST
            )

        elif request.method == 'DELETE':
            cart_item = get_object_or_404(
                ShoppingCart,
                user=request.user,
                recipe=recipe
            )
            cart_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        from django.http import HttpResponse
        from .models import ShoppingCart, RecipeIngredient
        from collections import defaultdict

        user_cart = ShoppingCart.objects.filter(user=request.user)

        if not user_cart.exists():
            return HttpResponse(
                "Ваш список покупок пуст!\n"
                "Добавьте рецепты в список покупок.",
                content_type='text/plain; charset=utf-8'
            )

        ingredient_totals = defaultdict(float)
        ingredient_units = {}

        for cart_item in user_cart:
            recipe = cart_item.recipe
            recipe_ingredients = RecipeIngredient.objects.filter(
                recipe=recipe
            )

            for ri in recipe_ingredients:
                ingredient_name = ri.ingredient.name
                ingredient_totals[ingredient_name] += ri.amount
                ingredient_units[ingredient_name] = (
                    ri.ingredient.measurement_unit
                )

        shopping_list = "СПИСОК ПОКУПОК\n\n"
        for i, (ingredient, amount) in enumerate(
            ingredient_totals.items(), 1
        ):
            unit = ingredient_units[ingredient]
            shopping_list += f"{i}. {ingredient} - {amount} {unit}\n"

        shopping_list += (
            f"\nИтого: {len(ingredient_totals)} позиций\n"
            f"Сгенерировано: {timezone.now().strftime('%d.%m.%Y %H:%M')}"
        )

        response = HttpResponse(
            shopping_list,
            content_type='text/plain; charset=utf-8'
        )
        response['Content-Disposition'] = (
            'attachment; filename="shopping_list.txt"'
        )

        return response
