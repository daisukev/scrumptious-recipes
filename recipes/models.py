from django.db import models
# from django.forms import ModelForm


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    picture = models.URLField()
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.title + " - " + self.description


# class RecipeForm(ModelForm):
#     class Meta:
#         model = Recipe
#         fields = {
#                 "title",
#                 "picture",
#                 "description",
#                 "under_30"
#                 }
