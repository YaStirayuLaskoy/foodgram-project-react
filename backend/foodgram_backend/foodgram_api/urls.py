from rest_framework import routers
from django.urls import path, include

from .views import (CustomUserViewSet, TagViewSet,
                    RecipeViewSet, IngredientViewSet)


# http://localhost/api/docs/ - docks
# http://127.0.0.1:8000/swagger-ui/ - docs swagger
# http://localhost - foodgram front
# https://www.figma.com/file/HHEJ68zF1bCa7Dx8ZsGxFh/ - figma


app_name = 'foodgram_api'

router = routers.DefaultRouter()
router.register('users', CustomUserViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
