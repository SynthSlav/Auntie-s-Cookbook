from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.text import slugify
from .forms import RecipeForm, IngredientFormSet

# Create your views here.


def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, "recipes/recipe_list.html", {"recipes": recipes})


def recipe_detail(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    return render(request, "recipes/recipe_detail.html", {"recipe": recipe})


@login_required
def add_recipe(request):
    if request.method == "POST":
        recipe_form = RecipeForm(request.POST)
        ingredient_formset = IngredientFormSet(request.POST)

        if recipe_form.is_valid() and ingredient_formset.is_valid():
            # Save the recipe with the current user as the author
            recipe = recipe_form.save(commit=False)
            recipe.author = request.user
            recipe.slug = slugify(recipe.title)
            recipe.save()

            ingredient_formset.instance = recipe
            ingredient_formset.save()

            messages.success(request, "Recipe {recipe.title} added successfully!")
            return redirect("recipe_detail", slug=recipe.slug)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        recipe_form = RecipeForm()
        ingredient_formset = ingredient_formset()

    return render(
        request,
        "recipes/add_recipe.html",
        {"form": recipe_form, "ingredient_formset": ingredient_formset},
    )
