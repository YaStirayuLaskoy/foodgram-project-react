from rest_framework import generics

from recipes.models import Tag, Ingredient, Recipe
from .serializers import (TagSerializer,
                          IngredientSerializer,
                          RecipeSerializer)


class TagApiList(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientApiList(generics.ListCreateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeApiList(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
