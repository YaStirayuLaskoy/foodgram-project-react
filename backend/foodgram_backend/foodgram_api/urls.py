from rest_framework import routers
from django.urls import path, include

from .views import CustomUserViewSet, TagViewSet, RecipeViewSet


app_name = 'foodgram_api'

router = routers.DefaultRouter()
router.register('users', CustomUserViewSet)
router.register('tags', TagViewSet)
router.register('recipes', RecipeViewSet)


urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
    # path('recipes/', RecipeApiList.as_view()),
    # path('recipes/<int:pk>', RecipeApiList.as_view()),
]


'''from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import TagViewSet, IngredientViewSet, RecipeViewSet


app_name = 'foodgram_api'

router = SimpleRouter() 
router.register('recipes', RecipeViewSet)


urlpatterns = [
    path('', include(router.urls)),
]'''
