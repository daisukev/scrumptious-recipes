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
    paginator = Paginator(recipes, 9, orphans=3)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    page_range = paginator.get_elided_page_range(number=page_number)
    context = {
            "recipe_list": page_obj,
            "view": "all_recipes",
            "page_range": page_range,
            }
    return render(request, "recipes/list.html", context)

@login_required
def my_recipe_list(request):
    recipes = Recipe.objects.filter(author= request.user)
    paginator = Paginator(recipes, 9, orphans=3)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    page_range = paginator.get_elided_page_range(number=page_number)
    context = {
            "recipe_list": page_obj,
            "view": "all_recipes",
            "page_range": page_range,
            }
    return render(request, "recipes/list.html", context)

def recipes_by_author(request, author_id):
    recipes = Recipe.objects.filter(author=author_id)
    paginator = Paginator(recipes, 9, orphans=3)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    page_range = paginator.get_elided_page_range(number=page_number)
    context = {
            "recipe_list": page_obj,
            "view": "author_recipe_list",
            "page_range": page_range,
            "author": f"{recipes[0].author.first_name} {recipes[0].author.last_name}"
            }
    return render(request, "recipes/list.html", context)


def get_rating(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return JsonResponse({
        "recipe": recipe.title,
        "average_rating": recipe.average_rating,
        "num_ratings": recipe.num_ratings,
        })
    

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
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id) 

    # TODO: Things like this should probably show an error to the user trying to perform the operation rather than silently failing.
    if request.user != recipe.author:
        return redirect('show_recipe', recipe_id)
    else:
        if request.method=="POST":
            recipe.delete()
            return redirect('recipe_list')
    context = {
            "recipe": recipe
            }
    return render(request, "recipes/delete.html", context)


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
    if recipe.author != request.user:
        return redirect("show_recipe", id=id)

    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        ingredients_formset = IngredientFormSet(request.POST, prefix="ingredients")
        recipe_steps_formset = RecipeStepFormSet(request.POST, prefix="recipe_steps")
        print('ingredient formset is bound: ', ingredients_formset.is_bound)
        print('recipe formset is bound: ', recipe_steps_formset.is_bound)

        if form.is_valid() and ingredients_formset.is_valid() and recipe_steps_formset.is_valid():

            # This should not be necessary as the author is already set in creation.
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()


            recipe.ingredients.all().delete()
            print('ingredients deleted!')
            for i_form in ingredients_formset:
                ingredient = i_form.save(commit=False)
                if i_form.is_valid():
                    print("Validated! here ist he form: ",i_form)

                print(i_form.cleaned_data)

                if ingredient.amount and ingredient.food_item:
                    ingredient.recipe = recipe
                    ingredient.save()
                    print("This is supposed to have saved!")
                else:
                    print("something ain't right this ain't saving")

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

