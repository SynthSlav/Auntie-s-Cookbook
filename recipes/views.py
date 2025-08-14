from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe, Ingredient
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.text import slugify
from .forms import RecipeForm, IngredientFormSet
from django.core.paginator import Paginator


# Create your views here.


def recipe_list(request):
    """Display a list of all recipes."""
    # Fetch all recipes from the database
    recipes = Recipe.objects.all()

    # Get filter parameters from URL
    meal_type = request.GET.get("meal_type")
    difficulty = request.GET.get("difficulty")
    dietary = request.GET.get("dietary")

    # Apply filters
    if meal_type:
        meal_types = meal_type.split(",")
        recipes = recipes.filter(meal_type__in=meal_types)

    if difficulty:
        difficulties = difficulty.split(",")
        recipes = recipes.filter(difficulty__in=difficulties)

    if dietary:
        dietary_restrictions = dietary.split(",")
        recipes = recipes.filter(dietary_restrictions__in=dietary_restrictions)

    # Paginate the filtered results
    paginator = Paginator(recipes, 10)  # 10 recipes per page
    page_number = request.GET.get(
        "page"
    )  # Get the current page number from the request
    page_obj = paginator.get_page(
        page_number
    )  # Get the page object for the current page
    return render(request, "recipes/recipe_list.html", {"page_obj": page_obj})


def recipe_detail(request, slug):
    """Display the details of a specific recipe."""
    # Fetch the recipe by slug, or return a 404 if not found
    recipe = get_object_or_404(Recipe, slug=slug)
    return render(request, "recipes/recipe_detail.html", {"recipe": recipe})


@login_required
def add_recipe(request):
    """Add a new recipe with ingredients."""
    if request.method == "POST":
        recipe_form = RecipeForm(request.POST, request.FILES)
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


@login_required
def edit_recipe(request, slug):
    """Edit an existing recipe if the user is the author."""
    recipe = get_object_or_404(Recipe, slug=slug, author=request.user)

    if request.method == "POST":
        recipe_form = RecipeForm(request.POST, request.FILES, instance=recipe)
        ingredient_formset = IngredientFormSet(
            request.POST, instance=recipe, prefix="ingredients"
        )

        if recipe_form.is_valid() and ingredient_formset.is_valid():
            try:
                # Save the recipe
                recipe = recipe_form.save(commit=False)

                # Handle slug regeneration if title changed
                if recipe_form.has_changed() and "title" in recipe_form.changed_data:
                    base_slug = slugify(recipe.title)
                    slug = base_slug
                    counter = 1
                    while (
                        Recipe.objects.filter(slug=slug).exclude(id=recipe.id).exists()
                    ):
                        slug = f"{base_slug}-{counter}"
                        counter += 1
                    recipe.slug = slug

                recipe.save()

                # Save ingredients with proper ordering
                ingredients = ingredient_formset.save(commit=False)
                for i, ingredient in enumerate(ingredients):
                    if ingredient.ingredient_name:
                        ingredient.order = i + 1
                        ingredient.save()

                # Handle deleted ingredients
                for ingredient in ingredient_formset.deleted_objects:
                    ingredient.delete()

                messages.success(
                    request, f"Recipe '{recipe.title}' updated successfully!"
                )
                return redirect("recipe_detail", slug=recipe.slug)

            except Exception as e:
                messages.error(
                    request,
                    "Something went wrong while updating your recipe. Please try again.",
                )
        else:
            if not recipe_form.is_valid():
                messages.error(request, "Please fix the recipe details errors.")
            if not ingredient_formset.is_valid():
                messages.error(request, "Please fix the ingredients errors.")
    else:
        recipe_form = RecipeForm(instance=recipe)
        ingredient_formset = IngredientFormSet(instance=recipe, prefix="ingredients")

    return render(
        request,
        "recipes/edit_recipe.html",
        {
            "recipe_form": recipe_form,
            "ingredient_formset": ingredient_formset,
            "recipe": recipe,
        },
    )


@login_required
def delete_recipe(request, slug):
    """Delete a recipe if the user is the author."""
    recipe = get_object_or_404(Recipe, slug=slug, author=request.user)

    # Confirm deletion
    if request.method == "POST":
        recipe_title = recipe.title
        recipe.delete()
        messages.success(request, f"Recipe '{recipe_title}' deleted successfully!")
        return redirect("recipe_list")

    return redirect("recipe_detail", slug=slug)
