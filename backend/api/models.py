from django.db import models


# Represents single ingredient to be used in recipes
class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    is_organic = models.BooleanField(default=False)
    description = models.TextField()

    def __str__(self):
        return self.name


# Represents cooking recipe 
class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    servings = models.IntegerField()
    date_added = models.DateField(auto_now_add=True)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')

    def __str__(self):
        return self.title


# Through model that connects Recipe and Ingredient with quantity and unit as additional fields
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit = models.CharField(max_length=50)
