from django.contrib import admin
from .models import Recipe, RecipeIngredient, Ingredient


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1  # Number of empty forms to display


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'servings', 'date_added')
    search_fields = ('title', 'description', 'servings')
    inlines = (RecipeIngredientInline,)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Display the name of the ingredient
    search_fields = ('name',)  # Allow searching by name
