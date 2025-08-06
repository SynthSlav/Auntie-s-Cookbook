from django.test import TestCase
from django.contrib.auth.models import User
from recipes.models import Recipe, Ingredient
from django.core.exceptions import ValidationError

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

    def test_recipe_get_absolute_url(self):
        """Test get absolute url method"""
        recipe = Recipe.objects.create(**self.recipe_data)
        expected_url = f"/recipes/{recipe.slug}/"
        self.assertEqual(recipe.get_absolute_url(), expected_url)

    def test_recipe_difficulty_choices(self):
        """Test difficulty field choices"""
        valid_difficulties = ["easy", "medium", "hard"]
        for difficulty in valid_difficulties:
            recipe_data = self.recipe_data.copy()
            recipe_data["difficulty"] = difficulty
            recipe_data["title"] = (
                f"Test Recipe {difficulty.title()}"  # Unique titles due to failing test
            )
            recipe_data["slug"] = (
                f"test-recipe-{difficulty}"  # Unique slugs due to failing test
            )
            recipe = Recipe.objects.create(**recipe_data)
            self.assertEqual(recipe.difficulty, difficulty)

    def test_positive_integer_fields(self):
        """Test that negative values are rejected"""
        recipe_data = self.recipe_data.copy()

        # Test servings
        recipe_data["servings"] = -1
        recipe = Recipe(**recipe_data)
        with self.assertRaises(ValidationError):
            recipe.full_clean()

        # Test prep_time
        recipe_data["servings"] = 4  # Reset to valid positive integer
        recipe_data["prep_time"] = -5
        recipe = Recipe(**recipe_data)
        with self.assertRaises(ValidationError):
            recipe.full_clean()

    def test_positive_integer_fields_reject_zero(self):
        """Test that zero values are rejected"""
        recipe_data = self.recipe_data.copy()
        recipe_data["servings"] = 0
        recipe = Recipe(**recipe_data)
        with self.assertRaises(ValidationError):
            recipe.full_clean()
