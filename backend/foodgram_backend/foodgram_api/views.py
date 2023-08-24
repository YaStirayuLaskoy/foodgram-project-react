from rest_framework import generics, viewsets
from djoser.views import UserViewSet

from recipes.models import Tag, Ingredient, Recipe
from .serializers import (TagSerializer,
                          IngredientSerializer,
                          RecipeSerializer)


class CustomUserViewSet(UserViewSet):
    """
    Странный Вьюсет, даже не ясно, почему это работает.
    https://disk.yandex.ru/d/1klrXEVJcEoTIg/16%20%D0%B2%D0%B5%D0%B1%D0%B8%D0%BD%D0%B0%D1%80%20-%20%D0%94%D0%B8%D0%BF%D0%BB%D0%BE%D0%BC%D0%BD%D1%8B%D0%B9%20%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%20-%20%D0%92%D0%BB%D0%B0%D0%B4%D0%B8%D0%BC%D0%B8%D1%80%20%D0%A1%D0%BE%D0%BB%D0%BE%D0%B2%D1%8C%D1%91%D0%B2/%D0%94%D0%B8%D0%BF%D0%BB%D0%BE%D0%BC%D0%BD%D1%8B%D0%B9%20%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%20-%20%D0%92%D0%BB%D0%B0%D0%B4%D0%B8%D0%BC%D0%B8%D1%80%20%D0%A1%D0%BE%D0%BB%D0%BE%D0%B2%D1%8C%D1%91%D0%B2.mp4
    На 20-той минуте он что-то про это говорит.
    """
    pass


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


'''class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer'''


'''class TagApiList(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientApiList(generics.ListCreateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeApiList(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer'''
