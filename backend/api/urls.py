"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/stable/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import test_api_view, recipe_view, ingredient_view, recipe_ingredient_view


urlpatterns = [
    # API entry points should be defined here
    path('test.json', test_api_view, name='api test'),
    path('recipes/', recipe_view),
    path('recipes/<int:recipe_id>/', recipe_view),
    path('ingredients/', ingredient_view, name='ingredient_list'),
    path('ingredients/<int:ingredient_id>/', ingredient_view, name='ingredient_detail'),
    path('recipes/<int:recipe_id>/ingredients/', recipe_ingredient_view, name='recipe_ingredients'),
]

