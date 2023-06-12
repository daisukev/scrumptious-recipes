from django.urls import path

from recipes.views import recipe_list,show_recipe,create_recipe, edit_recipe, create_rating, my_recipe_list, get_rating, recipes_by_author, delete_recipe

urlpatterns =[
        path("", recipe_list, name="recipe_list"),
        path("<int:id>", show_recipe,  name="show_recipe"),
        path("author/<int:author_id>", recipes_by_author,  name="recipes_by_author"),
        path("create/", create_recipe, name="create_recipe"),
        path("<int:id>/edit/", edit_recipe, name="edit_recipe"),
        path("ratings/create/<int:recipe_id>/<int:user_id>", create_rating, name="create_rating"), 
        path("ratings/<int:recipe_id>", get_rating, name="get_rating"),
        path("delete/<int:recipe_id>", delete_recipe, name="delete_recipe"),
        path("mine/", my_recipe_list, name="my_recipe_list"),
        ]
