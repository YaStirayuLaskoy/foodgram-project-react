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
    # id = serializers.ReadOnlyField(source='ingredient.id')
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
    ingredients = serializers.SerializerMethodField()
    # тоже самое:
    # ingredients = RecipeIngredientSerializer(many=True,
    #                                          source='recipe_ingredients')
    is_in_shopping_cart = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

    def get_ingredients(self, instance):
        return RecipeIngredientSerializer(instance.recipe_ingredients.all(),
                                          many=True).data

    def get_is_in_shopping_cart(self, instance):
        result = (not self.context.get('request').user.is_anonymous
                  and ShoppingList.objects.filter(
                      recipe=instance,
                      user=self.context.get('request').user
                  ))

        return result

    def get_is_favorited(self, instance):
        result = (not self.context.get('request').user.is_anonymous
                  and Favorite.objects.filter(
                      recipe=instance,
                      user=self.context.get('request').user
                  ))

        return result


'''class RecipeIngredientCreateSerializer(serializers.ModelSerializer):
    """Кастомный серилизатор создания рецепта для валидации доп полей."""
    """
    Не совсем понял, зачем наставник советовал для id делать целый серилизатор.
    Разве мы не можем переопределить id в RecipeIngredientSerializer?
    """
    id = serializers.PrimaryKeyRelatedField(source='ingredient',
                                            queryset=Ingredient.objects.all()
                                            )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')'''


class UserMeSerializer(UserSerializer):
    """Серилизатор пользователя."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, instance):
        """Это повтоярется в коде три раза. Нужно ли от этого избавляться?"""
        result = Follower.objects.filter(user=self.context('request').user,
                                         author=instance
                                         ).exists()

        if (not self.context('request').user.is_anonymous
            and self.context.get('request')):

            return result

        return False


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Серилизатор создания рецепта."""
    ingredients = RecipeIngredientSerializer(source='ingredientsRecipes',
                                             many=True
                                             )
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                              many=True
                                              )
    image = Base64ImageField(allow_null=True)
    author = UserMeSerializer(read_only=True, required=False)

    class Meta:
        model = Recipe
        fields = ('ingredients', 'tags', 'image', 'name', 'text', 'author',
                  'cooking_time')

    def create(self, validated_data):
        """Создание рецепта."""
        author = self.context.get('request').user
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data, author=author)

        Recipe.objects.create(**validated_data, author=author).tags.add(*tags)

        # Надо как-то избавиться от цикла. Мб bulk_create?
        # Наставник говорил про это ~ на 2:11:00
        for ingredient_data in ingredients:
            ingredient_id = ingredient_data['id']
            amount = ingredient_data['amount']

            RecipeIngredient.objects.create(ingredient=ingredient_id,
                                            recipe=recipe,
                                            amount=amount)

        return recipe

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, instance, validated_data):
        """Обновление рецепта."""
        author = self.context.get('request').user
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')

        instance.tags.clear()
        instance.tags.add(*tags)

        RecipeIngredient.objects.filter(recipe=instance).delete()

        for ingredient_data in ingredients:
            ingredient_id = ingredient_data['id']
            amount = ingredient_data['amount']

        RecipeIngredient.objects.create(ingredient=ingredient_id,
                                        recipe=instance,
                                        amount=amount)

        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save

        return instance

    def to_representation(self, instance):
        """2:23:00"""
        result = RecipeSerializer(instance,
                                  context={
                                      'request': self.context.get('request')
                                      }).data
        # return super().to_representation(instance)
        return result


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

    def validate(self, attrs):
        email = attrs.get('email')
        username = attrs.get('username')

        if User.objects.filter(username=username, email=email).exists():
            return attrs
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email занят.')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Имя пользователя занято.')

        return attrs


'''class UserMeSerializer(UserSerializer):
    """Серилизатор пользователя."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, instance):
        """Это повтоярется в коде три раза. Нужно ли от этого избавляться?"""
        result = Follower.objects.filter(user=self.context('request').user,
                                         author=instance
                                         ).exists()

        if (not self.context('request').user.is_anonymous
            and self.context.get('request')):

            return result

        return False'''


class UserRecipeSerializer(serializers.ModelSerializer):
    """Серилизатор для фолловеров и фиш листа."""
    image = Base64ImageField(read_only=True)
    name = serializers.ReadOnlyField()
    cooking_time = serializers.ReadOnlyField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = '__all__'


class UserFollowersSerializer(UserMeSerializer):
    """Серилизатор НА КОГО ПОДПИСАН юзер."""
    recipes = UserRecipeSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')
        read_only_fields = '__all__'

    def get_is_subscribed(self, instance):
        """Это повтоярется в коде три раза. Нужно ли от этого избавляться?"""
        result = Follower.objects.filter(user=self.context('request').user,
                                         author=instance
                                         ).exists()

        if (not self.context('request').user.is_anonymous
            and self.context.get('request')):

            return result

        return False

    def get_recipes_count(self, instance):
        return instance.recipes.count()


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
        if (self.context('request').user == valid_data):
            raise serializers.ValidationError({'errors': 'Ошибка'})

        return valid_data

    def get_is_subscribed(self, instance):
        """Это повтоярется в коде три раза. Нужно ли от этого избавляться?"""
        result = Follower.objects.filter(user=self.context('request').user,
                                         author=instance
                                         ).exists()

        if (not self.context('request').user.is_anonymous
            and self.context.get('request')):

            return result

    def get_recipes_count(self, instance):
        return instance.recipes.count()
