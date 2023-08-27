from rest_framework import serializers
# from djoser.serializers import UserSerializer, UserCreateSerializer

from recipes.models import Tag, Ingredient, Recipe, RecipeIngredient
from django.contrib.auth import get_user_model


User = get_user_model()


'''class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'password')


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name')
'''


class TagSerializer(serializers.ModelSerializer):
    """Серилизатор тегов."""

    class Meta:
        model = Tag
        fields = "__all__"


class IngredientSerializer(serializers.ModelSerializer):
    """Серилизатор ингредиентов."""

    class Meta:
        model = Ingredient
        fields = "__all__"


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Серилизатор ингредиентов в рецепте."""
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """Серелизатор рецептов."""
    tags = TagSerializer(many=True)  # чтобы в API тег был раскрыт
    ingredients = RecipeIngredientSerializer(many=True,
                                             source='recipeingredient_set')

    class Meta:
        model = Recipe
        fields = "__all__"


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Серилизатор создания рецепта."""

    class Meta:
        model = Recipe
        fields = ('name', 'cooking_time', 'text', 'tags')
