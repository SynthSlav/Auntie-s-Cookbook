from django import forms
from .models import Recipe, Ingredient


class RecipeForm(forms.ModelForm):
    """Form for creating and updating recipes."""

    class Meta:
        model = Recipe
        fields = [
            "title",
            "description",
            "recipe_image",
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
                    "required": True,
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Brief description of your recipe",
                    "rows": 3,
                    "required": True,
                }
            ),
            "recipe_image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*",
                }
            ),
            "servings": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "4",
                    "min": "1",
                    "max": "100",
                    "required": True,
                }
            ),
            "prep_time": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Minutes",
                    "min": "0",
                    "required": True,
                }
            ),
            "cook_time": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Minutes",
                    "min": "0",
                    "required": True,
                }
            ),
            "prep_instructions": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "How to prepare the ingredients...",
                    "rows": 4,
                    "required": True,
                }
            ),
            "cook_instructions": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Cooking steps and instructions...",
                    "rows": 4,
                    "required": True,
                }
            ),
            "difficulty": forms.Select(
                attrs={
                    "class": "form-select",
                    "required": True,
                }
            ),
            "meal_type": forms.Select(
                attrs={
                    "class": "form-select",
                    "required": True,
                }
            ),
            "dietary_restrictions": forms.Select(
                attrs={
                    "class": "form-select",
                    "required": True,
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add bootstrap classes and requirements
        for field_name, field in self.fields.items():
            if field.required:
                field.widget.attrs["required"] = True


class IngredientForm(forms.ModelForm):
    """Form for creating and updating ingredients."""

    class Meta:
        model = Ingredient
        fields = ["ingredient_name", "quantity", "unit", "notes"]

        widgets = {
            "ingredient_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g., all-purpose flour",
                }
            ),
            "quantity": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                    "placeholder": "1.5",
                }
            ),
            "unit": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "notes": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g., sifted, room temperature",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make ingredient_name required
        self.fields["ingredient_name"].required = True

        # Add empty option for unit if not set
        if not self.instance.pk:
            unit_choices = [("", "--- Select Unit ---")] + list(
                self.fields["unit"].choices
            )[1:]
            self.fields["unit"].choices = unit_choices


# Create the formset with better configuration
IngredientFormSet = forms.inlineformset_factory(
    Recipe,
    Ingredient,
    form=IngredientForm,
    extra=3,  # Start with 3 empty forms, its not working for some reason
    min_num=1,  # At least 1 ingredient required
    max_num=25,  # Maximum 25 ingredients
    can_delete=True,
    can_delete_extra=True,
    validate_min=True,  # Validate minimum number
)
