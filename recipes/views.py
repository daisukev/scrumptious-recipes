from django.shortcuts import render, get_object_or_404, render, redirect
from .models import Recipe
from .forms import RecipeForm


# Given an id number, this shows the corresponding recipe
# from the database.
def show_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    print('recipe: ', recipe.title)
    context = {
        "recipe": recipe
        }

    return render(request, "recipes/detail.html",context)

def recipe_list(request):
    recipes = Recipe.objects.all()
    context = {
            "recipe_list": recipes,
            }
    return render(request, "recipes/list.html", context)

def create_recipe(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect(recipe_list)
    else:
        form = RecipeForm()
    context = {
        "form": form
    }
    return render(request, "recipes/create.html", context)

def edit_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    if request.method == "POST":
        form = RecipeForm(request.POST,request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
        return redirect("show_recipe", id=id)
    else:
        form = RecipeForm(instance=recipe)
        context ={
                "recipe_object": recipe,
                "form": form,
                }
        return render(request, "recipes/edit.html", context)


# def edit_post (request, id):
#     post = get_object_or_404(Post, id=id)
#     if request.method == "POST":
#         form = PostForm(request. POST, instance=post)
#         if form.is_valid():
#             form.save ()
# # redirect back to the page that shows
# # the post
#         return redirect ("show_post", id=id)
#     else:
#         form = PostForm (instance=post)
#         context = {
#             "post_object": post,
#             "post_form": form,
#         }
#     return render (request, "posts/edit.html", context)

from datetime import datetime
def show_exercise(request, id):
    # !!!!!
    # DO NOT CHANGE ANY OF THE FOLLOWING CODE
    # !!!!!

    # Add id to exercise template path to locate specific template
    template_name = "exercises/exercise-" + str(id) + ".html"

    # Store multiple context dictionaries in a single list for easy access
    context_list = [
        {
            "date": datetime.now(),
            "image": "", # LEAVE THIS STRING EMPTY
            "mangled_content": "tHiS mESsaGe Is iN A ruDe tOne",
        },
        {
            "numbers": [1, 2, 3, 4, 5],
            "attendees": [
                {
                    "first_name": "Mike",
                    "last_name": "Wazowski",
                },
                {
                    "first_name": "James",
                    "last_name": "Sullivan",
                },
                {
                    "first_name": "Randall",
                    "last_name": "Boggs",
                },
            ],
        },
        {
            "employees": [
                {
                    "first_name": "Roz",
                    "last_name": "",
                    "created_on": datetime.now(),
                    "roles": ["Key master of the scare floor", "Head of the CDA"],
                },
                {
                    "first_name": "Celia",
                    "last_name": "Mae",
                    "created_on": datetime.now(),
                    "roles": ["Receptionist", "Floor supervisor"],
                },
                {
                    "first_name": "Boo",
                    "last_name": "",
                    "created_on": datetime.now(),
                    "roles": [],
                },
            ],
        }
    ]

    # Render exercise and use correct context based on location in the context_list
    return render(request, template_name, context_list[id - 1])
