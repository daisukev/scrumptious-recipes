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
    RecipeStepFormSet = formset_factory(RecipeStepForm, extra=1)


    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        ingredients_formset = IngredientFormSet(request.POST, prefix="ingredients")
        recipe_steps_formset = RecipeStepFormSet(request.POST, prefix="recipe_steps")


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
                    ingredient_form = form.save(commit=False)
                    if ingredient_form.amount and ingredient_form.food_item:
                        ingredient_form.recipe = recipe
                        ingredient_form.save()
            if recipe_steps_formset.is_valid():
                if recipe_steps_formset.is_valid():
                    for form in recipe_steps_formset:
                        recipe_steps_form = form.save(commit=False)
                        if recipe_steps_form.step_number and recipe_steps_form.instruction:
                            recipe_steps_form.recipe = recipe
                            recipe_steps_form.save()
            # form.save()
        return redirect('recipe_list')
    else:
        form = RecipeForm()
        ingredients = IngredientFormSet(prefix="ingredients")
        recipe_steps = RecipeStepFormSet(prefix="recipe_steps")
    context = {
        "form": form,
        "ingredients": ingredients,
        "recipe_steps": recipe_steps,
    }
    return render(request, "recipes/create.html", context)

@login_required
def edit_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    IngredientFormSet = formset_factory(IngredientForm, extra=0)
    RecipeStepFormSet = formset_factory(RecipeStepForm, extra=0)

    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        ingredients_formset = IngredientFormSet(request.POST, prefix="ingredients")
        recipe_steps_formset = RecipeStepFormSet(request.POST, prefix="recipe_steps")

        if form.is_valid() and ingredients_formset.is_valid() and recipe_steps_formset.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()

            # Update ingredients
            recipe.ingredients.all().delete()
            for ingredient_form in ingredients_formset:
                ingredient = ingredient_form.save(commit=False)
                if ingredient.amount and ingredient.food_item:
                    ingredient.recipe = recipe
                    ingredient.save()

            # Update recipe steps
            recipe.steps.all().delete()
            for recipe_step_form in recipe_steps_formset:
                recipe_steps_form = recipe_step_form.save(commit=False)
                if recipe_steps_form.step_number and recipe_steps_form.instruction:
                    recipe_steps_form.recipe = recipe
                    recipe_steps_form.save()
                # recipe_step.recipe = recipe
                # recipe_step.save()

            return redirect("show_recipe", id=id)
    else:
        form = RecipeForm(instance=recipe)
        ingredients_initial = [{"amount": ingredient.amount, "food_item": ingredient.food_item} for ingredient in recipe.ingredients.all()]
        recipe_steps_initial = [{"step_number": step.step_number, "instruction": step.instruction} for step in recipe.steps.all()]

        ingredients_formset = IngredientFormSet(prefix="ingredients", initial=ingredients_initial)
        recipe_steps_formset = RecipeStepFormSet(prefix="recipe_steps", initial=recipe_steps_initial)

    context = {
        "recipe_object": recipe,
        "form": form,
        "ingredients": ingredients_formset,
        "recipe_steps": recipe_steps_formset,
    }
    return render(request, "recipes/create.html", context)

# ## TODO: Views like this should be gated by the user. Only the user who is 
# @login_required
# def edit_recipe(request, id):
#     IngredientFormSet = formset_factory(IngredientForm, extra=1)
#     RecipeStepFormSet = formset_factory(RecipeStepForm, extra=1)
#     recipe = get_object_or_404(Recipe, id=id)
#     if request.method == "POST":
#         form = RecipeForm(request.POST,request.FILES, instance=recipe)
        
#         if form.is_valid():
#             ingredients_formset = IngredientFormSet(request.POST, prefix="ingredients")
#             recipe_steps_formset = RecipeStepFormSet(request.POST, prefix="recipe_steps")
        
#             # don't save immediately
#             recipe = form.save(commit=False)
#             # edit field 
#             recipe.author = request.user
#             print(recipe)
#             # save entry
#             recipe.save()
#             if ingredients_formset.is_valid():
#                 for form in ingredients_formset:
#                     print(form)
#                     ingredient_form = form.save(commit=False)
#                     print('cleaned data: ',form.cleaned_data)
#                     ingredient_form.recipe = recipe
#                     ingredient_form.save()
#             if recipe_steps_formset.is_valid():
#                 for form in recipe_steps_formset:
#                     recipe_steps_form = form.save(commit=False)
#                     print('cleaned data: ',form.cleaned_data)
#                     recipe_steps_form.recipe = recipe
#                     recipe_steps_form.save()
#         return redirect("show_recipe", id=id)
#     else:
#         form = RecipeForm(instance=recipe)
#         ingredients_data = [{"amount": i.amount, "food_item": i.food_item} for i in recipe.ingredients.all()]
#         ingredients = IngredientFormSet(prefix="ingredients", initial=ingredients_data)
#         print(recipe.steps.all())
#         recipe_steps = RecipeStepFormSet(prefix="recipe-steps", initial=recipe)
#         context ={
#                 "recipe_object": recipe,
#                 "form": form,
#                 "ingredients": ingredients,
#                 "recipe_steps": recipe_steps,
#                 }
#         return render(request, "recipes/create.html", context)
