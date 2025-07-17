from django.contrib import admin
from .models import Recipe, Ingredient

# Register your models here.


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "difficulty", "meal_type", "created_at")
    list_filter = ("difficulty", "meal_type", "dietary_restrictions")
    search_fields = ("title", "description", "ingredients__ingredient_name")
    prepopulated_fields = {"slug": ("title",)}


# @admin.register(Ingredient)
# class IngredientAdmin(admin.ModelAdmin):
#     list_display = ("ingredient_name", "quantity", "unit", "recipe")
#     list_filter = ("unit",)
#     search_fields = ("ingredient_name",)
