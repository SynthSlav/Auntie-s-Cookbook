from django.urls import path
from . import views

urlpatterns = [
    path("", views.recipe_list, name="recipe_list"),  # URL for the recipe list view
    path(
        "recipe/<slug:slug>/", views.recipe_detail, name="recipe_detail"
    ),  # URL for the recipe detail view
]
