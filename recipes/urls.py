from django.urls import path
from . import views

urlpatterns = [
    path("", views.recipe_list, name="recipe_list"),  # URL for the recipe list view
    path(
        "add-recipe/", views.add_recipe, name="add_recipe"
    ),  # URL for adding a new recipe
    path(
        "<slug:slug>/", views.recipe_detail, name="recipe_detail"
    ),  # URL for the recipe detail view
]
