from django.contrib import admin

from .models import (Tag, Ingredient, Recipe, RecipeIngredient,
                     Favorite, ShoppingList)


admin.site.register(Tag)
admin.site.register(Ingredient)
# admin.site.register(Recipe)
admin.site.register(Favorite)
admin.site.register(ShoppingList)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline, )
