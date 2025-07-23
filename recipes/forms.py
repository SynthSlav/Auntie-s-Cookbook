from django import forms
from .models import Recipe, Ingredient


class RecipeForm(forms.ModelForm):
    """Form for creating and updating recipes."""

    class Meta:
        model = Recipe
        fields = [
            "title",
            "description",
            "servings",
            "prep_time",
            "cook_time",
            "prep_instructions",
            "cook_instructions",
            "difficulty",
            "meal_type",
            "dietary_restrictions",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your recipe title",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Brief description of your recipe",
                    "rows": 3,
                }
            ),
            "servings": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "4",
                    "min": "1",
                    "max": "100",
                }
            ),
            "prep_time": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Minutes",
                    "min": "0",
                }
            ),
            "cook_time": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Minutes",
                    "min": "0",
                }
            ),
            "prep_instructions": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "How to prepare the ingredients...",
                    "rows": 4,
                }
            ),
            "cook_instructions": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Cooking steps and instructions...",
                    "rows": 4,
                }
            ),
            "difficulty": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "meal_type": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "dietary_restrictions": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ["ingredient_name", "quantity", "unit", "notes"]

        widgets = {
            "ingredient_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ingredient name"}
            ),
            "quantity": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.25",
                    "min": "0",
                    "placeholder": "1",
                }
            ),
            "unit": forms.Select(attrs={"class": "form-select"}),
            "notes": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Optional notes"}
            ),
        }


IngredientFormSet = forms.inlineformset_factory(
    Recipe,
    Ingredient,
    form=IngredientForm,
    extra=1,
    can_delete=True,
    can_delete_extra=True,
)
