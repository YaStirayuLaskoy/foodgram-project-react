from django.db import models
from django.contrib.auth import get_user_model

from .validators import validate_not_null


User = get_user_model()


class Tag(models.Model):
    """Теги. Все поля обязательны для заполнения и уникальны."""
    name = models.CharField(max_length=50,
                            blank=False,
                            verbose_name="Название тега",
                            help_text="Введите название тега",
                            unique=True,
                            )
    color = models.CharField(max_length=10,
                             blank=False,
                             verbose_name="Цвет тега",
                             help_text="Введите цвет тега",
                             unique=True,
                             )
    slug = models.SlugField(max_length=50,
                            blank=False,
                            verbose_name="slug",
                            help_text="Введите slug значение",
                            unique=True,
                            )

    class Meta:
        ordering = ["name"]
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """
    Ингридиенты.
    Данные об ингредиентах должны храниться в нескольких связанных таблицах.
    Все поля обязательны для заполнения.
    """
    name = models.CharField(max_length=50,
                            blank=False,
                            verbose_name="Название ингредиента",
                            help_text="Введите название Ингредиента",
                            unique=False,
                            )
    measurement_unit = models.CharField(max_length=200,
                                        blank=False,
                                        verbose_name="Единица измерения",
                                        help_text="Введите единицу измерения",
                                        unique=False,
                                        )


class Recipe(models.Model):
    """Рецепт. Все поля обязательны для заполнения."""
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               blank=False,
                               verbose_name="Автор рецепта",
                               related_name="recipes",
                               )
    name = models.CharField(max_length=90,
                            blank=False,
                            verbose_name="Название рецепта",
                            help_text="Введите название рецепта",
                            unique=False,
                            )
    image = models.ImageField(upload_to="images",
                              blank=False,
                              verbose_name="Изображение рецепта",
                              help_text="Загрузите изображение рецепта",
                              null=True,
                              )
    text = models.TextField(max_length=2500,
                            blank=False,
                            verbose_name="Описание рецепта",
                            help_text="Введите рецепт",
                            unique=True,
                            )
    ingredients = models.ManyToManyField(Ingredient,
                                         through='RecipeIngredient',
                                         through_fields=('recipe',
                                                         'ingredient',),
                                         )
    tags = models.ManyToManyField(Tag,
                                  through='RecipeTag',
                                  related_name='recipes')
    cooking_time = models.PositiveIntegerField(validators=[validate_not_null])


class RecipeIngredient(models.Model):
    """Связующая модель для кастомного поля amount."""
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name="recipe_ingredients",
                               )
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE,
                                   related_name="recipe_ingredients",
                                   )
    amount = models.PositiveIntegerField(validators=[validate_not_null])


class RecipeTag(models.Model):
    """Тег в рецепте."""
    tag = models.ForeignKey(Tag,
                            on_delete=models.CASCADE,
                            blank=False,
                            verbose_name="Тег в рецепте",
                            )
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               blank=False,
                               verbose_name="Рецепт с тегами",
                               )


class ShoppingList(models.Model):
    """Модель списка покупок."""
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               blank=False,
                               verbose_name="Рецепт в покупках",
                               related_name="shopping_list_recipe",
                               )
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             blank=False,
                             verbose_name='Пользователь',
                             related_name='shopping_list_user',
                             )


class Favorite(models.Model):
    """Модель избранного."""
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               blank=False,
                               verbose_name="Рецепт Еверчойзен",
                               related_name="favorite_recipe",
                               )
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             blank=False,
                             verbose_name='Пользователь',
                             related_name='favorite_user',
                             )
