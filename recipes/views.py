from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe, Ingredient
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.text import slugify
from .forms import RecipeForm, IngredientFormSet
from django.core.paginator import Paginator


# Create your views here.


def recipe_list(request):
    """Display paginated list of recipes with filtering."""
    # Start with all recipes
    recipes = Recipe.objects.all()

    # Get filter parameters from request
    meal_types = request.GET.getlist("meal_type")
    difficulties = request.GET.getlist("difficulty")
    dietary_restrictions = request.GET.getlist("dietary")

    # Apply filters if any are selected
    if meal_types:
        recipes = recipes.filter(meal_type__in=meal_types)

    if difficulties:
        recipes = recipes.filter(difficulty__in=difficulties)

    if dietary_restrictions:
        recipes = recipes.filter(dietary_restrictions__in=dietary_restrictions)

    # Paginate the filtered recipes, showing 10 per page
    paginator = Paginator(recipes, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Prepare active filters for template
    active_filters = {
        "meal_types": meal_types,
        "difficulties": difficulties,
        "dietary_restrictions": dietary_restrictions,
    }

    # Build query string for pagination links
    filter_query_string = ""
    for meal_type in meal_types:
        filter_query_string += f"&meal_type={meal_type}"
    for difficulty in difficulties:
        filter_query_string += f"&difficulty={difficulty}"
    for dietary in dietary_restrictions:
        filter_query_string += f"&dietary={dietary}"

    return render(
        request,
        "recipes/recipe_list.html",
        {
            "page_obj": page_obj,
            "active_filters": active_filters,
            "filter_query_string": filter_query_string,
            "total_recipes": recipes.count(),
        },
    )


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
