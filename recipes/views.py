from django.shortcuts import render, get_object_or_404, render, redirect
from django.views.generic import ListView
from django.core.paginator import Paginator
from .models import Recipe, Rating
from .forms import RecipeForm, RatingForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# Given an id number, this shows the corresponding recipe
# from the database.
def show_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    print('recipe: ', recipe.title)
    # print(vars(recipe))
    # print(vars(recipe.ratings.all()))
    context = {
        "recipe": recipe,
        }

    return render(request, "recipes/detail.html",context)

def recipe_list(request):
    recipes = Recipe.objects.all()
    paginator = Paginator(recipes, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
            "recipe_list": page_obj,
            "view": "all_recipes"
            }
    return render(request, "recipes/list.html", context)

@login_required
def my_recipe_list(request):
    recipes = Recipe.objects.filter(author= request.user)
    paginator = Paginator(recipes, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
            "recipe_list": page_obj,
            "view": "my_recipe_list"
            }
    return render(request, "recipes/list.html", context)


# This handles creation and editing of ratings.
@login_required
def create_rating(request,recipe_id, user_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    author = get_object_or_404(User, id = user_id) # This is the creator of the rating, not the author of the recipe. recipe.author is the recipe author.


    # if author == recipe.author, reject
    try:
        if author.id == recipe.author.id:
            return JsonResponse({
                "success": False,
                "message":"You cannot create a rating for your own recipe"
                })
    except AttributeError: # We don't care if there is no recipe author. 
        pass


    request.POST = request.POST.copy()
    request.POST['recipe'] = recipe_id  # append the recipe_id to the post request.
    request.POST['author'] = user_id

    if request.method=="POST":
        form = RatingForm(request.POST)
        if form.is_valid():

            ## check if the user already has a rating and update if they do
            ratings = Rating.objects.filter(author= author, recipe=recipe)
            if ratings:
                form = RatingForm(request.POST, instance=ratings[0])
                form.save()
                return JsonResponse({
                    "success": True,
                    "message": "Updated Rating"})
                # if there is a rating, then update it
                # if not, it'll continue down the rest of the method
            form.save()
            return JsonResponse({
                "success": True,
                "message": "Rating added successfully."})
        else:
            return JsonResponse({
                "success": False,
                "message": "Could not add rating."})

@login_required
def create_recipe(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            # don't save immediately
            recipe = form.save(False)
            # edit field 
            recipe.author = request.user
            # save entry
            recipe.save()
            # form.save()
        return redirect(recipe_list)
    else:
        form = RecipeForm()
    context = {
        "form": form
    }
    return render(request, "recipes/create.html", context)

@login_required
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
