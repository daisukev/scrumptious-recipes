from django.forms import ModelForm
from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Recipe,Rating, Ingredient, RecipeStep

class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = (
                "title",
                "picture", 
                "description"
                )
        exclude = ['thumbnail']

class RatingForm(ModelForm):
    class Meta:
        model = Rating
        fields = (
                "value",
                "recipe",
                "author",
                )

class IngredientForm(ModelForm):
    class Meta:
        model = Ingredient
        fields = "__all__"
        exclude = ['recipe']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount'].required = False
        self.fields['food_item'].required = False


class RecipeStepForm(ModelForm):
    class Meta:
        model = RecipeStep
        fields = "__all__"
        exclude = ['recipe']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['step_number'].required = False
        self.fields['instruction'].required = False
