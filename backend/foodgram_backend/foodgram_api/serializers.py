from rest_framework import serializers
from djoser.serializers import UserSerializer, UserCreateSerializer
from django.core.validators import validate_email
# Картинки
from django.core.files.base import ContentFile
import base64

from recipes.models import (Tag, Ingredient, Recipe, RecipeIngredient,
                            ShoppingList, Favorite)
from users.models import Follower

from django.contrib.auth import get_user_model


User = get_user_model()


class UserMeSerializer(UserSerializer):
    """Серилизатор пользователя."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, obj):
        # Это повтоярется в коде три раза. Нужно ли от этого избавляться?
        if (self.context.get('request')
           and not self.context['request'].user.is_anonymous):

            return Follower.objects.filter(user=self.context['request'].user,
                                           author=obj
                                           ).exists()

        return False


class Base64ImageField(serializers.ImageField):
    """Серизиатор картинок."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


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
    id = serializers.PrimaryKeyRelatedField(source='ingredient.id',
                                            queryset=Ingredient.objects.all()
                                            )
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """Серелизатор рецептов."""
    tags = TagSerializer(many=True, read_only=True)
    ingredients = RecipeIngredientSerializer(many=True,
                                             source='recipe_ingredients',
                                             read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    author = UserMeSerializer(read_only=True)
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipe
        fields = ['id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time', ]

    def get_is_in_shopping_cart(self, instance):
        user = self.context.get('request').user

        return (not user.is_anonymous
                and ShoppingList.objects.filter(recipe=instance,
                                                user=user).exists())

    def get_is_favorited(self, instance):
        user = self.context.get('request').user

        return (not user.is_anonymous
                and Favorite.objects.filter(recipe=instance,
                                            user=user).exists())


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Серилизатор создания рецепта."""
    ingredients = RecipeIngredientSerializer(source='recipe_ingredients',
                                             many=True
                                             )
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                              many=True
                                              )
    image = Base64ImageField(allow_null=True, required=False)
    author = UserMeSerializer(read_only=True, required=False)

    class Meta:
        model = Recipe
        fields = ['id', 'ingredients', 'tags', 'image', 'name',
                  'text', 'author', 'cooking_time', ]

    def create(self, validated_data):
        author = self.context.get('request').user
        ingredients = validated_data.pop('recipe_ingredients')
        tags = validated_data.pop('tags')

        recipe = Recipe.objects.create(**validated_data, author=author)
        recipe.tags.add(*tags)

        ingredients_list = []

        # Надо как-то избавиться от цикла. Мб bulk_create?
        # Наставник говорил про это ~ на 2:11:00
        for ingredient_data in ingredients:
            ingredient_id = ingredient_data['ingredient']['id']
            current_amount = ingredient_data.get('amount')

            ingredients_list.append(RecipeIngredient(recipe=recipe,
                                                     ingredient=ingredient_id,
                                                     amount=current_amount
                                                     ))

        RecipeIngredient.objects.bulk_create(ingredients_list)

        return recipe

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('recipe_ingredients')
        tags = validated_data.pop('tags')

        instance.tags.clear()
        instance.tags.add(*tags)

        RecipeIngredient.objects.filter(recipe=instance).delete()

        ingredients_list = []

        for ingredient_data in ingredients:
            ingredient_id = ingredient_data['ingredient']['id']
            current_amount = ingredient_data.get('amount')

            ingredients_list.append(RecipeIngredient(recipe=instance,
                                                     ingredient=ingredient_id,
                                                     amount=current_amount
                                                     ))

        RecipeIngredient.objects.bulk_create(ingredients_list)

        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()

        return instance

    def to_representation(self, instance):
        # 2:23:00
        return RecipeSerializer(
            instance,
            context={'request': self.context.get('request')}).data


class RegistrarionSerializer(UserCreateSerializer):
    """Серилизатор регистрации."""
    email = serializers.EmailField(max_length=228,
                                   validators=[validate_email]
                                   )
    username = serializers.CharField(max_length=228)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'password')


class UserRecipeSerializer(serializers.ModelSerializer):
    """Серилизатор для фолловеров и фиш листа."""
    image = Base64ImageField(read_only=True)
    name = serializers.ReadOnlyField()
    cooking_time = serializers.ReadOnlyField()

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time', ]
        read_only_fields = ('__all__',)


class UserFollowersSerializer(UserMeSerializer):
    """Серилизатор НА КОГО ПОДПИСАН юзер."""
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count',)
        read_only_fields = ('__all__',)

    def get_recipes(self, author):
        limit = self.context.get('request').query_params.get('recipes_limit')

        try:
            recipes = (author.recipes.all()[:int(limit)]
                       if limit else author.recipes.all())

        except ValueError:
            raise serializers.ValidationError({'errors': 'Ошибка'})

        return UserRecipeSerializer(recipes, many=True).data

    def get_is_subscribed(self, instance):
        if (self.context.get('request')
           and not self.context['request'].user.is_anonymous):

            return Follower.objects.filter(user=self.context['request'].user,
                                           author=instance
                                           ).exists()

        return False

    def get_recipes_count(self, obj: User) -> int:

        return obj.recipes.count()


class AuthorFollowersSerializer(serializers.ModelSerializer):
    """Серилизатор КТО ПОДПИСАН на юзера."""
    email = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField()
    first_name = serializers.ReadOnlyField()
    last_name = serializers.ReadOnlyField()
    is_subscribed = serializers.SerializerMethodField()
    recipes = UserRecipeSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def validate(self, valid_data):
        if (self.context['request'].user == valid_data):
            raise serializers.ValidationError({'errors': 'Ошибка'})

        return valid_data

    def get_is_subscribed(self, instance):
        if (self.context.get('request')
           and not self.context['request'].user.is_anonymous):

            return Follower.objects.filter(user=self.context['request'].user,
                                           author=instance
                                           ).exists()

        return False

    def get_recipes_count(self, valid_data):
        return valid_data.recipes.count()
