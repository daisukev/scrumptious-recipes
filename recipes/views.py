from django.shortcuts import render, get_object_or_404, render, redirect
from django.views.generic import ListView
from django.core.paginator import Paginator
from .models import Recipe, Rating
from .forms import RecipeForm, RatingForm, RecipeStepForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms import formset_factory
from .forms import IngredientForm
from .models import Ingredient

def can_edit_object(user, obj): # obj being any model in this app. i.e. recipe or rating
    return user.is_authenticated and (user.is_staff or user == obj.author)

def user_can_edit_recipe(function):
    pass

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
    IngredientFormSet = formset_factory(IngredientForm, extra=1)
    # it should exclude the recipe in the formset as it should automatically save to the one we're working on right now.
    RecipeStepFormSet = formset_factory(RecipeStepForm, extra=1)


    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        ingredients_formset = IngredientFormSet(request.POST, prefix="ingredients")
        recipe_steps_formset = RecipeStepFormSet(request.POST, prefix="recipe-steps")

        # TODO: Rename formset to IngredientFormSet here and in the create.html template
        # https://docs.djangoproject.com/en/4.2/topics/forms/formsets/#using-more-than-one-formset-in-a-view

        if form.is_valid():
            # don't save immediately
            recipe = form.save(commit=False)
            # edit field 
            recipe.author = request.user
            print(recipe)
            # save entry
            recipe.save()
            if ingredients_formset.is_valid():
                for form in ingredients_formset:
                    print(form)
                    ingredient_form = form.save(commit=False)
                    print('cleaned data: ',form.cleaned_data)
                    ingredient_form.recipe = recipe
                    ingredient_form.save()
            if recipe_steps_formset.is_valid():
                for form in recipe_steps_formset:
                    recipe_steps_form = form.save(commit=False)
                    print('cleaned data: ',form.cleaned_data)
                    recipe_steps_form.recipe = recipe
                    recipe_steps_form.save()
            # form.save()
        return redirect('recipe_list')
    else:
        form = RecipeForm()
        ingredients = IngredientFormSet(prefix="ingredients")
        recipe_steps = RecipeStepFormSet(prefix="recipe-steps")
    context = {
        "form": form,
        "ingredients": ingredients,
        "recipe_steps": recipe_steps,
    }
    return render(request, "recipes/create.html", context)

## TODO: Views like this should be gated by the user. Only the user who is 
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
