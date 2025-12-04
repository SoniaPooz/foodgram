from django.contrib import admin
from .models import (
    Tag, Ingredient, Recipe, RecipeIngredient, Favorite, ShoppingCart
)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('name',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('measurement_unit',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'favorite_count', 'cooking_time', 'pub_date')
    search_fields = ('name', 'author__username', 'author__email', 'text')
    list_filter = ('tags', 'pub_date')
    inlines = (RecipeIngredientInline,)
    
    def get_queryset(self, request):
        from django.db.models import Count
        queryset = super().get_queryset(request)
        return queryset.annotate(favorite_count_value=Count('favorites'))
    
    def favorite_count(self, obj):
        return obj.favorite_count_value
    favorite_count.admin_order_field = 'favorite_count_value'
    favorite_count.short_description = 'В избранном'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user__username', 'recipe__name')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user__username', 'recipe__name')
