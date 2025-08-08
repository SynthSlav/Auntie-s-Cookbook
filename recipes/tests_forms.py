from django.test import TestCase
from recipes.forms import RecipeForm, IngredientForm, IngredientFormSet
from recipes.models import Recipe, Ingredient
from django.contrib.auth.models import User


class RecipeFormTest(TestCase):
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

        self.valid_recipe_data = {
            "title": "Test Recipe",
            "description": "A delicious test recipe",
            "servings": 4,
            "prep_time": 15,
            "cook_time": 30,
            "prep_instructions": "Prepare the ingredients carefully",
            "cook_instructions": "Cook according to instructions",
            "difficulty": "easy",
            "meal_type": "dinner",
            "dietary_restrictions": "none",
        }

    def test_recipe_form_valid_data(self):
        """Test form with valid data."""
        form = RecipeForm(data=self.valid_recipe_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.errors, {})

    def test_recipe_form_missing_required_fields(self):
        """Test form validation for required fields."""
        # Test each required field individually
        required_fields = [
            "title",
            "description",
            "prep_instructions",
            "cook_instructions",
            "difficulty",
            "meal_type",
        ]

        for field in required_fields:
            with self.subTest(field=field):
                data = self.valid_recipe_data.copy()
                del data[field]

                form = RecipeForm(data=data)
                self.assertFalse(form.is_valid())
                self.assertIn(field, form.errors)

    def test_recipe_form_invalid_choice_fields(self):
        """Test choice field validation."""
        choice_tests = [
            ("difficulty", "impossible"),
            ("meal_type", "midnight_snack"),
            ("dietary_restrictions", "carnivore"),
        ]

        for field, invalid_value in choice_tests:
            with self.subTest(field=field, value=invalid_value):
                data = self.valid_recipe_data.copy()
                data[field] = invalid_value

                form = RecipeForm(data=data)
                self.assertFalse(form.is_valid())
                self.assertIn(field, form.errors)


class IngredientFormTest(TestCase):
    def setUp(self):
        """Set up test data."""
        self.valid_ingredient_data = {
            "ingredient_name": "Flour",
            "quantity": 2.5,
            "unit": "cup",
            "notes": "All-purpose flour",
        }

    def test_ingredient_form_valid_data(self):
        """Test ingredient form with valid data."""
        form = IngredientForm(data=self.valid_ingredient_data)
        self.assertTrue(form.is_valid())

    def test_ingredient_form_missing_name_fails(self):
        """Test validation, ingredient_name is required."""
        data = self.valid_ingredient_data.copy()
        del data["ingredient_name"]

        form = IngredientForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("ingredient_name", form.errors)

    def test_ingredient_form_unit_empty_option_for_new_ingredients(self):
        """Test custom __init__ logic for unit choices."""
        form = IngredientForm()  # New ingredient

        # Check that form adds the empty "--- Select Unit ---" option
        unit_choices = form.fields["unit"].choices
        first_choice = unit_choices[0]
        self.assertEqual(first_choice[0], "")  # Empty value
        self.assertIn("Select Unit", first_choice[1])
