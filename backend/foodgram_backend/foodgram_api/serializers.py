from rest_framework import serializers

from recipes.models import Tag, Ingredient, Recipe
from django.contrib.auth import get_user_model


User = get_user_model()


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = "__all__"


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = "__all__"


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)  # чтобы в API тег был раскрыт

    class Meta:
        model = Recipe
        fields = "__all__"
