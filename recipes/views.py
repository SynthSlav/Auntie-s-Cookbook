from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe, Ingredient
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.text import slugify
from .forms import RecipeForm, IngredientFormSet
from django.forms import formset_factory

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
        ingredient_formset = IngredientFormSet(request.POST, prefix="ingredients")

        if recipe_form.is_valid() and ingredient_formset.is_valid():
            try:
                # Save the recipe with the current user as the author
                recipe = recipe_form.save(commit=False)
                recipe.author = request.user

                # Generate unique slug
                base_slug = slugify(recipe.title)
                slug = base_slug
                counter = 1
                while Recipe.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                recipe.slug = slug

                recipe.save()

                # Save ingredients with proper ordering
                ingredient_formset.instance = recipe
                ingredients = ingredient_formset.save(commit=False)

                # Set order for ingredients and save them
                for i, ingredient in enumerate(ingredients):
                    if ingredient.ingredient_name:  # Only save non-empty ingredients
                        ingredient.order = i + 1
                        ingredient.save()

                # Handle deleted ingredients
                for ingredient in ingredient_formset.deleted_objects:
                    ingredient.delete()

                messages.success(
                    request, f"Recipe '{recipe.title}' added successfully!"
                )
                return redirect("recipe_detail", slug=recipe.slug)

            except Exception as e:
                messages.error(
                    request,
                    "Oops! Something went wrong while saving your recipe. Please try again.",
                )
        else:
            # Add detailed error messages
            if not recipe_form.is_valid():
                messages.error(request, "Please fix the recipe details errors.")
            if not ingredient_formset.is_valid():
                messages.error(request, "Please fix the ingredients errors.")
    else:
        recipe_form = RecipeForm()
        # Initialize the formset with no initial data
        # This allows the formset to be empty initially
        ingredient_formset = IngredientFormSet(
            prefix="ingredients", queryset=Ingredient.objects.none()
        )

    return render(
        request,
        "recipes/add_recipe.html",
        {
            "recipe_form": recipe_form,
            "ingredient_formset": ingredient_formset,
        },
    )
