from django.urls import path

from recipes.views import recipe_list,show_recipe,create_recipe, edit_recipe, create_rating, my_recipe_list, get_rating

urlpatterns =[
        path("", recipe_list, name="recipe_list"),
        path("<int:id>", show_recipe,  name="show_recipe"),
        path("create/", create_recipe, name="create_recipe"),
        path("<int:id>/edit/", edit_recipe, name="edit_recipe"),
        path("ratings/create/<int:recipe_id>/<int:user_id>", create_rating, name="create_rating"), 
        path("ratings/<int:recipe_id>", get_rating, name="get_rating"),
        path("mine/", my_recipe_list, name="my_recipe_list"),
        ]
