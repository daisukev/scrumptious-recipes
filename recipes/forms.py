from PIL import Image
from django.forms import ModelForm
from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Recipe

class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = (
                "title",
                "picture", 
                "description"
                )
