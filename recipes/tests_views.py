from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from recipes.models import Recipe, Ingredient


class RecipeViewTest(TestCase):
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

        self.other_user = User.objects.create_user(
            username="otheruser", email="other@example.com", password="testpass123"
        )

        self.recipe = Recipe.objects.create(
            title="Test Recipe",
            slug="test-recipe",
            description="A test recipe",
            servings=4,
            prep_time=15,
            cook_time=30,
            prep_instructions="Prep instructions",
            cook_instructions="Cook instructions",
            difficulty="easy",
            meal_type="dinner",
            dietary_restrictions="none",
            author=self.user,
        )

    # AUTHENTICATION & PERMISSIONS TESTS

    def test_add_recipe_requires_login(self):
        """Test that anonymous users can't add recipes"""
        response = self.client.get(reverse("add_recipe"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_edit_recipe_owner_only(self):
        """Test that only recipe owner can edit"""
        self.client.login(username="otheruser", password="testpass123")
        response = self.client.get(
            reverse("edit_recipe", kwargs={"slug": self.recipe.slug})
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_recipe_owner_only(self):
        """Test that only recipe owner can delete"""
        self.client.login(username="otheruser", password="testpass123")
        response = self.client.post(
            reverse("delete_recipe", kwargs={"slug": self.recipe.slug})
        )
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Recipe.objects.filter(id=self.recipe.id).exists())
