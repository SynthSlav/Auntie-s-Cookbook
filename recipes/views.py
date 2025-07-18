from django.shortcuts import render, get_object_or_404
from .models import Recipe

# Create your views here.


def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, "recipes/recipe_list.html", {"recipes": recipes})


def recipe_detail(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    return render(request, "recipes/recipe_detail.html", {"recipe": recipe})
