from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from recipes.models import Recipe, Ingredient
from django.core.files.uploadedfile import SimpleUploadedFile


class RecipeViewTest(TestCase):
    def setUp(self):
        """Set up test data."""
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
        """Test that anonymous users can't add recipes."""
        response = self.client.get(reverse("add_recipe"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_edit_recipe_owner_only(self):
        """Test that only recipe owner can edit."""
        self.client.login(username="otheruser", password="testpass123")
        response = self.client.get(
            reverse("edit_recipe", kwargs={"slug": self.recipe.slug})
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_recipe_owner_only(self):
        """Test that only recipe owner can delete."""
        self.client.login(username="otheruser", password="testpass123")
        response = self.client.post(
            reverse("delete_recipe", kwargs={"slug": self.recipe.slug})
        )
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Recipe.objects.filter(id=self.recipe.id).exists())

    # RECIPE CREATION WORKFLOW (form processing)

    def test_add_recipe_with_ingredients_success(self):
        """Test complete recipe creation with ingredients."""
        self.client.login(username="testuser", password="testpass123")

        recipe_data = {
            "title": "New Recipe",
            "description": "A new test recipe",
            "servings": 2,
            "prep_time": 10,
            "cook_time": 20,
            "prep_instructions": "Prep the ingredients",
            "cook_instructions": "Cook the food",
            "difficulty": "medium",
            "meal_type": "lunch",
            "dietary_restrictions": "vegetarian",
            # Test ingredient formset handling
            "ingredients-TOTAL_FORMS": "2",
            "ingredients-INITIAL_FORMS": "0",
            "ingredients-MIN_NUM_FORMS": "1",
            "ingredients-MAX_NUM_FORMS": "25",
            "ingredients-0-ingredient_name": "Flour",
            "ingredients-0-quantity": "1",
            "ingredients-0-unit": "cup",
            "ingredients-1-ingredient_name": "Sugar",
            "ingredients-1-quantity": "0.5",
            "ingredients-1-unit": "cup",
        }

        response = self.client.post(reverse("add_recipe"), data=recipe_data)

        # Should redirect to recipe detail
        self.assertEqual(response.status_code, 302)

        # Verify slug generation logic works (uses Django's slugify + uniqueness)
        new_recipe = Recipe.objects.get(title="New Recipe")
        self.assertEqual(new_recipe.slug, "new-recipe")  # logic uses slugify()
        self.assertEqual(new_recipe.author, self.user)

        # Verify ingredient ordering logic works
        self.assertEqual(new_recipe.ingredients.count(), 2)
        flour = new_recipe.ingredients.get(ingredient_name="Flour")
        self.assertEqual(str(flour.quantity), "1.00")
        self.assertEqual(flour.order, 1)  # view sets order = i + 1

    def test_add_recipe_missing_ingredients(self):
        """Test error handling for invalid ingredient data."""
        self.client.login(username="testuser", password="testpass123")

        recipe_data = {
            "title": "Recipe Without Ingredients",
            "description": "This should show error messages",
            "servings": 2,
            "prep_time": 10,
            "cook_time": 20,
            "prep_instructions": "Prep",
            "cook_instructions": "Cook",
            "difficulty": "easy",
            "meal_type": "lunch",
            "dietary_restrictions": "none",
            "ingredients-TOTAL_FORMS": "1",
            "ingredients-INITIAL_FORMS": "0",
            "ingredients-MIN_NUM_FORMS": "1",
            "ingredients-MAX_NUM_FORMS": "25",
            "ingredients-0-ingredient_name": "",  # Empty name
        }

        response = self.client.post(reverse("add_recipe"), data=recipe_data)

        # Should stay on add_recipe page (not redirect)
        self.assertEqual(response.status_code, 200)

        # Should NOT create recipe
        self.assertFalse(
            Recipe.objects.filter(title="Recipe Without Ingredients").exists()
        )

    # RECIPE EDITING WORKFLOW

    def test_edit_recipe_updates_correctly(self):
        """Test recipe editing logic."""
        self.client.login(username="testuser", password="testpass123")

        # Add an ingredient first
        ingredient = Ingredient.objects.create(
            recipe=self.recipe,
            ingredient_name="Original Ingredient",
            quantity=1,
            unit="cup",
        )

        edit_data = {
            "title": "Updated Recipe Title",
            "description": "Updated description",
            "servings": 6,
            "prep_time": 20,
            "cook_time": 40,
            "prep_instructions": "Updated prep",
            "cook_instructions": "Updated cooking",
            "difficulty": "hard",
            "meal_type": "breakfast",
            "dietary_restrictions": "vegan",
            "ingredients-TOTAL_FORMS": "1",
            "ingredients-INITIAL_FORMS": "1",
            "ingredients-MIN_NUM_FORMS": "1",
            "ingredients-MAX_NUM_FORMS": "25",
            "ingredients-0-id": ingredient.id,
            "ingredients-0-ingredient_name": "Updated Ingredient",
            "ingredients-0-quantity": "2",
            "ingredients-0-unit": "tablespoon",
        }

        response = self.client.post(
            reverse("edit_recipe", kwargs={"slug": self.recipe.slug}), data=edit_data
        )

        self.assertEqual(response.status_code, 302)

        # Verify update logic worked
        updated_recipe = Recipe.objects.get(id=self.recipe.id)
        self.assertEqual(updated_recipe.title, "Updated Recipe Title")
        self.assertEqual(updated_recipe.servings, 6)

        # Verify slug regeneration logic worked (only when title changed)
        self.assertEqual(updated_recipe.slug, "updated-recipe-title")

        updated_ingredient = updated_recipe.ingredients.first()
        self.assertEqual(updated_ingredient.ingredient_name, "Updated Ingredient")
        self.assertEqual(updated_ingredient.order, 1)

    def test_delete_recipe(self):
        """Test cascade delete logic."""
        Ingredient.objects.create(
            recipe=self.recipe, ingredient_name="Test Ingredient 1"
        )
        Ingredient.objects.create(
            recipe=self.recipe, ingredient_name="Test Ingredient 2"
        )

        ingredient_count_before = Ingredient.objects.filter(recipe=self.recipe).count()
        self.assertEqual(ingredient_count_before, 2)

        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(
            reverse("delete_recipe", kwargs={"slug": self.recipe.slug})
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("recipe_list"))

        # Recipe should be deleted
        self.assertFalse(Recipe.objects.filter(id=self.recipe.id).exists())

        # Ingredients should be deleted too
        ingredient_count_after = Ingredient.objects.filter(recipe=self.recipe).count()
        self.assertEqual(ingredient_count_after, 0)
