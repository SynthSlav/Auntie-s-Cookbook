from django import forms
from .models import Recipe


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
