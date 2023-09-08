from rest_framework import viewsets, status
from djoser.views import UserViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import F, Sum
from django.http import HttpResponse

from recipes.models import (Tag, Ingredient, Recipe, Favorite, ShoppingList,
                            RecipeIngredient)
from users.models import Follower
from .serializers import (TagSerializer, IngredientSerializer,
                          RecipeSerializer, UserMeSerializer,
                          RecipeCreateSerializer, RegistrarionSerializer,
                          UserRecipeSerializer, UserFollowersSerializer,
                          AuthorFollowersSerializer)
from .pagination import PaginatorUser
from .permissions import AdminOrAuthorPermission
from .filters import RecipeFilter

from django.contrib.auth import get_user_model


User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """
    https://disk.yandex.ru/d/1klrXEVJcEoTIg/16%20%D0%B2%D0%B5%D0%B1%D0%B8%D0%BD%D0%B0%D1%80%20-%20%D0%94%D0%B8%D0%BF%D0%BB%D0%BE%D0%BC%D0%BD%D1%8B%D0%B9%20%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%20-%20%D0%92%D0%BB%D0%B0%D0%B4%D0%B8%D0%BC%D0%B8%D1%80%20%D0%A1%D0%BE%D0%BB%D0%BE%D0%B2%D1%8C%D1%91%D0%B2/%D0%94%D0%B8%D0%BF%D0%BB%D0%BE%D0%BC%D0%BD%D1%8B%D0%B9%20%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%20-%20%D0%92%D0%BB%D0%B0%D0%B4%D0%B8%D0%BC%D0%B8%D1%80%20%D0%A1%D0%BE%D0%BB%D0%BE%D0%B2%D1%8C%D1%91%D0%B2.mp4
    На 20-той минуте он что-то про это говорит.
    """
    queryset = User.objects.all()
    pagination_class = PaginatorUser
    http_method_names = ['get', 'post', 'delete']

    def get_permissions(self):
        if self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated, ]

        return super(self.__class__, self).get_permissions()

    def get_serializer_class(self):
        if self.action in ['subscriptions', 'subscribe']:
            return UserFollowersSerializer
        elif self.request.method == 'GET':
            return UserMeSerializer
        elif self.request.method == 'POST':
            return RegistrarionSerializer

    @action(detail=False, methods=['get'], pagination_class=PaginatorUser,
            permission_classes=(IsAuthenticated,)
            )
    def subscriptions(self, request):
        queryset = User.objects.filter(following__user=request.user)

        serializer = UserFollowersSerializer(
            self.paginate_queryset(queryset), many=True,
            context={'request': request}
        )

        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=(IsAuthenticated,)
            )
    def subscribe(self, request, **kwargs):
        author = get_object_or_404(User, id=kwargs['id'])

        if request.method == 'POST':
            serializer = AuthorFollowersSerializer(author,
                                                   data=request.data,
                                                   context={'request': request}
                                                   )
            serializer.is_valid(raise_exception=True)

            if author == request.user:
                return Response({'detail': 'Нельзя подписаться на себя.'},
                                status=status.HTTP_400_BAD_REQUEST)
            if Follower.objects.filter(user=request.user,
                                       author=author).exists():
                return Response({'detail': 'Вы уже подписались.'},
                                status=status.HTTP_400_BAD_REQUEST)

            Follower.objects.create(user=request.user, author=author)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            try:
                follow = Follower.objects.get(user=request.user, author=author)
            except Follower.DoesNotExist:
                return Response({'detail': 'Вы и не были подписаны.'},
                                status=status.HTTP_400_BAD_REQUEST)
            follow.delete()
            return Response({'detail': 'Вы отписались'},
                            status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], pagination_class=None,
            permission_classes=(IsAuthenticated,)
            )
    def me(self, request):
        serializer = UserMeSerializer(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)


class TagViewSet(viewsets.ModelViewSet):
    """Вью сет тегов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (AllowAny, )


class RecipeViewSet(viewsets.ModelViewSet):
    """Вью сет рецептов."""
    queryset = Recipe.objects.all()
    permission_classes = [AdminOrAuthorPermission, ]
    filter_backends = (DjangoFilterBackend, )
    filter_class = RecipeFilter
    pagination_class = PaginatorUser

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        elif self.action in ['favorite', 'shopping_cart', ]:
            return UserRecipeSerializer

        return RecipeCreateSerializer

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=(IsAuthenticated,))
    def favorite(self, request, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs['pk'])
        serializer = UserRecipeSerializer(recipe, context={"request": request})

        if request.method == 'POST':
            if Favorite.objects.filter(user=request.user,
                                       recipe=recipe).exists():
                return Response({'errors': 'Рецепт уже добавлен в избранное'},
                                status=status.HTTP_400_BAD_REQUEST)
            Favorite.objects.create(user=request.user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            if not Favorite.objects.filter(user=request.user,
                                           recipe=recipe).exists():
                return Response({'errors': 'Рецепт не в избранном'},
                                status=status.HTTP_400_BAD_REQUEST)
            favorite = get_object_or_404(Favorite, user=request.user,
                                         recipe=recipe)
            favorite.delete()
            return Response({'detail': 'Рецепт удален из избранного'},
                            status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=(IsAuthenticated,),
            pagination_class=None)
    def shopping_cart(self, request, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs['pk'])
        if request.method == 'POST':
            serializer = UserRecipeSerializer(recipe, data=request.data,
                                              context={"request": request})
            serializer.is_valid()
            if ShoppingList.objects.filter(user=request.user,
                                           recipe=recipe).exists():
                return Response(
                    {'errors': 'Рецепт уже добавлен в список покупок'},
                    status=status.HTTP_400_BAD_REQUEST)
            ShoppingList.objects.create(user=request.user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            if not ShoppingList.objects.filter(user=request.user,
                                               recipe=recipe).exists():
                return Response(
                    {'errors': 'Рецепта не было в списке покупок'},
                    status=status.HTTP_400_BAD_REQUEST)
            get_object_or_404(ShoppingList, user=request.user,
                              recipe=recipe).delete()
            return Response(
                {'detail': 'Рецепт удален из списка покупок'},
                status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        permission_classes=[IsAuthenticated, ]
    )
    def download_shopping_cart(self, request):
        user = request.user
        shopping_cart = RecipeIngredient.objects.filter(
            recipe__shopping_cart_recipe__user=user)
        ingredients = shopping_cart.values(
            name=F('ingredient__name'),
            measurement_unit=F('ingredient__measurement_unit')).annotate(
            amount=Sum('amount'))

        file_name = 'shopping_cart.txt'
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'

        for ingredient in ingredients:
            response.write(
                f"{ingredient['name']} - {ingredient['amount']}"
                f" {ingredient['measurement_unit']}\n")

        return response


class IngredientViewSet(viewsets.ModelViewSet):
    """Вью сет ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']
    lookup_field = 'name__istartswith'
    pagination_class = None

    def get_queryset(self):
        queryset = self.queryset
        name = self.request.query_params.get('name', None)

        if name is not None:
            queryset = queryset.filter(name__istartswith=name)

        return queryset
