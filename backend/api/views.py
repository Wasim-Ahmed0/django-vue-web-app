from .models import Recipe, RecipeIngredient, Ingredient
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


def test_api_view(request):
    return JsonResponse({
        'message': 'Good response!'
    })

# list all recipes or get a single recipe
@csrf_exempt
def get_recipe(recipe_id=None):
    if recipe_id:
        recipe = Recipe.objects.filter(id=recipe_id).first()
        if recipe:
            ingredients = [
                {"name": ri.ingredient.name, "quantity": ri.quantity, "unit": ri.unit}
                for ri in RecipeIngredient.objects.filter(recipe=recipe)
            ]
            return JsonResponse({
                "id": recipe.id,
                "title": recipe.title,
                "description": recipe.description,
                "servings": recipe.servings,
                "date_added": recipe.date_added,
                "ingredients": ingredients
            })
        return JsonResponse({"error": "Recipe not found"}, status=404)
    recipes = list(Recipe.objects.all().values())
    return JsonResponse(recipes, safe=False)

# create new recipe with ingredients
@csrf_exempt
def create_recipe(request):
    data = json.loads(request.body)
    recipe = Recipe.objects.create(
        title=data.get("title"),
        description=data.get("description"),
        servings=data.get("servings")
    )
    for ing in data.get("ingredients", []):
        ingredient, created = Ingredient.objects.get_or_create(name=ing["name"])
        RecipeIngredient.objects.create(
            recipe=recipe,
            ingredient=ingredient,
            quantity=ing["quantity"],
            unit=ing["unit"]
        )
    return JsonResponse({"id": recipe.id, "message": "Recipe created successfully"})

# update existing recipe details
@csrf_exempt
def update_recipe(request, recipe_id):
    data = json.loads(request.body)
    recipe = Recipe.objects.filter(id=recipe_id).first()
    if recipe:
        recipe.title = data.get("title", recipe.title)
        recipe.description = data.get("description", recipe.description)
        recipe.servings = data.get("servings", recipe.servings)
        recipe.save()
        
        return JsonResponse({
            "id": recipe.id,
            "title": recipe.title,
            "description": recipe.description,
            "servings": recipe.servings,
            "date_added": recipe.date_added.isoformat() if recipe.date_added else None
        })
    return JsonResponse({"error": "Recipe not found"}, status=404)


# delete recipe by id
@csrf_exempt
def delete_recipe(recipe_id):
    recipe = Recipe.objects.filter(id=recipe_id).first()
    if recipe:
        recipe.delete()
        return JsonResponse({"message": "Recipe deleted successfully"})
    return JsonResponse({"error": "Recipe not found"}, status=404)


# list all ingredients or get single ingredient by id
@csrf_exempt
def get_ingredients(ingredient_id):
    if ingredient_id:
        ingredient = Ingredient.objects.filter(id=ingredient_id).first()
        if ingredient:
            return JsonResponse({
                "id": ingredient.id,
                "name": ingredient.name,
                "is_organic": ingredient.is_organic,
                "description": ingredient.description
            })
        return JsonResponse({"error": "Ingredient not found"}, status=404)
    ingredients = list(Ingredient.objects.all().values('id', 'name', 'is_organic', 'description'))
    return JsonResponse(ingredients, safe=False)


# create new ingredient
@csrf_exempt
def create_ingredient(request):
    data = json.loads(request.body)
    ingredient = Ingredient.objects.create(
        name=data.get("name"),
        description=data.get("description", ""),
        is_organic=data.get("is_organic", False)
    )
    return JsonResponse({
        "id": ingredient.id,
        "name": ingredient.name,
        "description": ingredient.description,
        "is_organic": ingredient.is_organic,
        "message": "Ingredient created successfully"
    })


# update existing ingredient details
@csrf_exempt
def update_ingredient(request, ingredient_id):
    data = json.loads(request.body)
    ingredient = Ingredient.objects.filter(id=ingredient_id).first()
    if ingredient:
        ingredient.name = data.get("name", ingredient.name)
        ingredient.description = data.get("description", ingredient.description)
        ingredient.is_organic = data.get("is_organic", ingredient.is_organic)
        ingredient.save()
        return JsonResponse({
            "id": ingredient.id,
            "name": ingredient.name,
            "description": ingredient.description,
            "is_organic": ingredient.is_organic
        })
    return JsonResponse({"error": "Ingredient not found"}, status=404)


# delete ingredient by id
@csrf_exempt
def delete_ingredient(ingredient_id):
    ingredient = Ingredient.objects.filter(id=ingredient_id).first()
    if ingredient:
        ingredient.delete()
        return JsonResponse({"message": "Ingredient deleted successfully"})
    return JsonResponse({"error": "Ingredient not found"}, status=404)


# list all ingredients associated with specific recipe
@csrf_exempt
def get_recipe_ingredients(recipe_id):
    recipe_ingredients = list(RecipeIngredient.objects.filter(recipe_id=recipe_id).values(
        'ingredient__name', 'quantity', 'unit'
    ))
    return JsonResponse(recipe_ingredients, safe=False)


# update all ingredients associated with specific recipe
@csrf_exempt
def update_recipe_ingredient(request, recipe_id):
    data = json.loads(request.body)
    recipe = Recipe.objects.filter(id=recipe_id).first()
    if recipe:
        RecipeIngredient.objects.filter(recipe=recipe).delete()
        for ing in data.get("ingredients", []):
            ingredient, _ = Ingredient.objects.get_or_create(name=ing["name"])
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                quantity=ing["quantity"],
                unit=ing["unit"]
            )
        return JsonResponse({"message": "Recipe ingredients updated successfully"})
    return JsonResponse({"error": "Recipe not found"}, status=404)


# delete ingredient associated with specific recipe
@csrf_exempt
def delete_recipe_ingredient(recipe_id, ingredient_name):
    recipe = Recipe.objects.filter(id=recipe_id).first()
    if recipe:
        ingredient = Ingredient.objects.filter(name=ingredient_name).first()
        if ingredient:
            recipe_ingredient = RecipeIngredient.objects.filter(
                recipe=recipe,
                ingredient=ingredient
            ).first()
            if recipe_ingredient:
                recipe_ingredient.delete()
                return JsonResponse({"message": "Recipe ingredient deleted successfully"})
            return JsonResponse({"error": "Recipe ingredient not found"}, status=404)
        return JsonResponse({"error": "Ingredient not found"}, status=404)
    return JsonResponse({"error": "Recipe not found"}, status=404)


# recipe view
@csrf_exempt
def recipe_view(request, recipe_id=None):
    if request.method == "GET":
        return get_recipe(recipe_id)
    elif request.method == "POST":
        return create_recipe(request)
    elif request.method == "PUT" and recipe_id:
        return update_recipe(request, recipe_id)
    elif request.method == "DELETE" and recipe_id:
        return delete_recipe(recipe_id)
    return JsonResponse({"error": "Invalid HTTP method"}, status=405)


# ingredient view
@csrf_exempt
def ingredient_view(request, ingredient_id=None):
    if request.method == "GET":
        return get_ingredients(ingredient_id)
    elif request.method == "POST":
        return create_ingredient(request)
    elif request.method == "PUT" and ingredient_id:
        return update_ingredient(request, ingredient_id)
    elif request.method == "DELETE" and ingredient_id:
        return delete_ingredient(ingredient_id)
    return JsonResponse({"error": "Invalid HTTP method"}, status=405)


# recipe ingredient view
@csrf_exempt
def recipe_ingredient_view(request, recipe_id):
    if request.method == "GET":
        return get_recipe_ingredients(recipe_id)
    elif request.method == "PUT":
        return update_recipe_ingredient(request, recipe_id)
    elif request.method == "DELETE":
        try:
            data = json.loads(request.body)
            ingredient_name = data.get('ingredient_name')
            if ingredient_name:
                return delete_recipe_ingredient(recipe_id, ingredient_name)
            return JsonResponse({"error": "Ingredient name is required"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON in request body"}, status=400)
    return JsonResponse({"error": "Invalid HTTP method"}, status=405)
