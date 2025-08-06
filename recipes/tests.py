from django.test import TestCase
from django.contrib.auth.models import User
from recipes.models import Recipe, Ingredient


# Create your tests here.


class RecipeModelTest(TestCase):
    """Test case for the Recipe model."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser1", password="testpassword1", email="test@example.com"
        )
        self.recipe_data = {
            "title": "Test Recipe",
            "description": "A test recipe description",
            "servings": 4,
            "prep_time": 15,
            "cook_time": 30,
            "prep_instructions": "Prep the ingredients",
            "cook_instructions": "Cook the food",
            "difficulty": "easy",
            "meal_type": "dinner",
            "dietary_restrictions": "none",
            "author": self.user,
        }

    def test_recipe_creation(self):
        """Test basic recipe creation."""
        recipe = Recipe.objects.create(**self.recipe_data)

        self.assertEqual(recipe.title, "Test Recipe")
        self.assertEqual(recipe.description, "A test recipe description")
        self.assertEqual(recipe.servings, 4)
        self.assertIsNotNone(recipe.created_at)
        self.assertIsNotNone(recipe.updated_at)

    def test_recipe_slug_generation(self):
        """Test automatic slug generation."""
        recipe = Recipe.objects.create(**self.recipe_data)

        expected_slug = self.recipe_data["title"].lower().replace(" ", "-")
        self.assertEqual(recipe.slug, expected_slug)

    def test_recipe_manual_slug(self):
        """Test that slug can be set manually"""
        recipe_data = self.recipe_data.copy()
        recipe_data["slug"] = "custom-slug"
        recipe = Recipe.objects.create(**recipe_data)
        self.assertEqual(recipe.slug, "custom-slug")

    def test_recipe_str_method(self):
        """Verify that string method works correctly"""
        recipe = Recipe.objects.create(**self.recipe_data)
        self.assertEqual(str(recipe), "Test Recipe")

    def test_recipe_total_time_property(self):
        """Test total time calculated properly"""
        recipe = Recipe.objects.create(**self.recipe_data)
        self.assertEqual(recipe.total_time, 45)
