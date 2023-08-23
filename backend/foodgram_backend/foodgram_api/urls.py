from django.urls import path

from .views import RecipeApiList


app_name = 'foodgram_api'


urlpatterns = [
    path('recipes/', RecipeApiList.as_view()),
    path('recipes/<int:pk>', RecipeApiList.as_view())
]
