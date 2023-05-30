from django.forms import ModelForm, formset_factory
from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Recipe,Rating

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

