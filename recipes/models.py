from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class Recipe(models.Model):
    # Constant choices for recipe difficulty
    DIFFICULTY_CHOICES = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    ]

    # Constant choices for meal type
    MEAL_TYPE_CHOICES = [
        ("breakfast", "Breakfast"),
        ("lunch", "Lunch"),
        ("dinner", "Dinner"),
        ("snack", "Snack"),
        ("dessert", "Dessert"),
        ("appetizer", "Appetizer"),
    ]

    DIETARY_CHOICES = [
        ("none", "No Restrictions"),
        ("vegetarian", "Vegetarian"),
        ("vegan", "Vegan"),
        ("gluten_free", "Gluten Free"),
        ("dairy_free", "Dairy Free"),
        ("keto", "Keto"),
        ("paleo", "Paleo"),
    ]

    # Model fields for recipe attributes
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipes")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    servings = models.PositiveIntegerField(default=4, help_text="Number of servings")
    prep_time = models.PositiveIntegerField(help_text="Preparation time in minutes")
    prep_instructions = models.TextField()
    cook_time = models.PositiveIntegerField(help_text="Cooking time in minutes")
    cook_instructions = models.TextField()
    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
    )
    meal_type = models.CharField(
        max_length=20,
        choices=MEAL_TYPE_CHOICES,
    )
    dietary_restrictions = models.CharField(
        max_length=20,
        choices=DIETARY_CHOICES,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        # Automatically set the slug field based on the title if not provided
        if not self.slug:
            self.slug = self.title.lower().replace(" ", "-")
        super().save(*args, **kwargs)

    def __str__(self):
        # Returns the title of the recipe when the object is printed
        return self.title

    def get_absolute_url(self):
        return reverse("recipe_detail", kwargs={"slug": self.slug})

    @property  # Total time for the recipe
    def total_time(self):
        """Calculate total time for recipe."""
        return self.prep_time + self.cook_time


class Ingredient(models.Model):
    # Model fields for ingredient attributes
    UNIT_CHOICES = [
        ("whole", "Whole"),
        ("cup", "Cup"),
        ("tablespoon", "Tablespoon"),
        ("teaspoon", "Teaspoon"),
        ("gram", "Gram"),
        ("kilogram", "Kilogram"),
        ("liter", "Liter"),
        ("milliliter", "Milliliter"),
        ("piece", "Piece"),
        ("pinch", "Pinch"),
        ("to taste", "To Taste"),
        ("clove", "Clove"),
    ]

    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="ingredients"
    )
    ingredient_name = models.CharField(max_length=100)
    quantity = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, blank=True)
    notes = models.CharField(blank=True, max_length=200)
    order = models.PositiveIntegerField(default=0, help_text="Order of the ingredient")

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        if self.quantity and self.unit:
            return f"{self.quantity} {self.unit} {self.ingredient_name}"
        elif self.quantity:
            return f"{self.quantity} {self.ingredient_name}"
        else:
            return self.ingredient_name
