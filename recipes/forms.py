from django.forms import ModelForm
from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Recipe,Rating, Ingredient

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


