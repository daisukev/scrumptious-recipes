from django.urls import path

from recipes.views import recipe_list,show_recipe,create_recipe, show_exercise, edit_recipe, create_rating

urlpatterns =[
        path("", recipe_list, name="recipe_list"),
        path("<int:id>", show_recipe,  name="show_recipe"),
        path("create/", create_recipe, name="create_recipe"),
        path("<int:id>/edit", edit_recipe, name="edit_recipe"),
        path("exercises/<int:id>/", show_exercise, name="exercise"),
        path("ratings/create/<int:id>", create_rating, name="create_rating")
        ]
