from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Tag(models.Model):
    """Теги. Все поля обязательны для заполнения и уникальны."""
    title = models.CharField(max_length=50,
                             blank=False,
                             verbose_name="Название тега",
                             help_text="Введите название тега",
                             unique=True,
                             )
    collor = pass  # Мб ChoiceField? Что за «Цветовой код #49B64E.»?
    slug = models.SlugField(max_lenght=50,
                            blank=False,
                            verbose_name="Какое-то слаг значение",
                            help_text="Введите какое-то слаг значение",
                            unique=True,
                            )


class Ingredient(models.Model):
    """
    Ингридиенты.
    Данные об ингредиентах должны храниться в нескольких связанных таблицах.
    Все поля обязательны для заполнения.
    """
    pass


class Recipe(models.Model):
    """Рецепт. Все поля обязательны для заполнения."""
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               blank=False,
                               verbose_name="Автор рецепта",
                               related_name="recipes",
                               )
    title = models.CharField(max_lenght=90,
                             blank=False,
                             verbose_name="Название рецепта",
                             help_text="Введите название рецепта",
                             unique=False,
                             )
    image = models.ImageField(upload_to="backend/foodgram_backend/",
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
                            # db_index=True,
                            )
    # У ингридиентов один рецепт?
    '''ingredients = models.ForeignKey(Ingredients,
                                    on_delete=models.SET_NULL,
                                    blank=False,
                                    verbose_name="Ингредиенты рецепта",
                                    related_name="recipes",
                                    )'''
    # Или у ингридиантов много рецептов?
    # Какая-то чепуха... >:\
    ingredient = models.ManyToManyField(Ingredient)
    # Почему в ТЗ говорят создать отдельную модель для тегов?
    # Неужели нельзя так?:
    # tags = models.Choices(max_length=3, choices=TAGS)
    tag = models.ManyToManyField(Tag)
    cooking_time = models.PositiveIntegerField()
