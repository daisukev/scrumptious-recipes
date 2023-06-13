from django.db import models
from PIL import Image
import os
from django.core.files import File
from io import BytesIO
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg
from .helpers.average_rating import average_rating
from django.conf import settings

class Rating(models.Model):
    # Ensure that the rating is at most a 5 and at least a 1 (1-5 star rating)
    value = models.IntegerField(validators=[MaxValueValidator(5),MinValueValidator(1)])
    # rating would have a value, an author, and a Recipe
    # It would be 1 rating to 1 author. It would be 1 rating to 1 Recipe
    # It would be 1 Recipe to many Ratings

    recipe = models.ForeignKey('Recipe', related_name="ratings", on_delete=models.CASCADE)
    author = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            related_name="ratings",
            on_delete = models.CASCADE,
            # this wasn't present originally so this is use setting the default value
            null = True,)
    def __str__(self):
        return str(self.value)

class RecipeStep(models.Model):
    instruction = models.TextField()
    step_number = models.PositiveIntegerField()
    recipe = models.ForeignKey("Recipe", related_name="steps", on_delete=models.CASCADE)
    def __str__(self):
        return self.instruction
    def recipe_title(self):
        return self.recipe.title
    class Meta:
        # Default is to order list by ID, this overrides it to make it order by the order attribute
        ordering = ["step_number"]

class Ingredient(models.Model):
    amount = models.CharField(max_length=100)
    food_item=  models.CharField(max_length=100)
    recipe = models.ForeignKey(
            "Recipe", related_name="ingredients", on_delete=models.CASCADE,)
    class Meta:
        ordering= ["food_item"]
    def __str__(self):
        return self.food_item

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    picture = models.ImageField(upload_to="images/")
    thumbnail = models.ImageField(upload_to="thumbnails/", default ='https://placehold.co/300x225')
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            related_name="recipes",
            on_delete = models.CASCADE,
            # this wasn't present originally so this is use setting the default value
            null = True,
            )

    def __str__(self):
        return self.title

    @property 
    def average_rating(self):
        ratings = self.ratings.all()
        avg = average_rating(ratings)
        return avg
    @property
    def num_ratings(self):
        return len(self.ratings.all())
    @property
    def ratings_breakdown(self):
        ratings = self.ratings.all()
        ratings_list = [0,0,0,0,0]
        if ratings:
            for rating in ratings:
                ratings_list[rating.value-1] += 1
        return ratings_list

    def save(self, *args, **kwargs):

        thumb_data = BytesIO() # create binary stream to store the thumbnail 
        thumb_img = Image.open(self.picture) #open a copy  of the picture
        thumb_height = 285
        thumb_width =  380

        # check dimensions of the picture
        if thumb_img.height >= thumb_img.width: # if it's a tall image, we want the thumbnail size  to adhere to the width, so the height is set arbitrarily large
            # height * thumbnail width / img_width
            target_height  = int(thumb_img.height * thumb_width / thumb_img.width)
            thumbnail_size = (thumb_width, target_height)
        else:
            target_width = int((thumb_height * thumb_img.width) / thumb_img.height)
            thumbnail_size = (target_width, thumb_height)


        thumb_img.thumbnail(thumbnail_size) # shrink it


        # file formats 
        thumb_img.save(thumb_data, format=thumb_img.format)   # save the thumbnail same filetype as the original
        thumb_img.close() # close the image
        stripped_picture_path = os.path.basename(os.path.splitext(str(self.picture))[0])

        print(stripped_picture_path)
        thumb_path = f"{stripped_picture_path}_thumbnail.{thumb_img.format.lower()}" # thumbnail should be the picture, but with _thumbnail.EXT added to it
        thumb_file_path= os.path.join('thumbnails', thumb_path)
        thumb_file = File(thumb_data)
        file_path = os.path.join('media', thumb_file_path)

        # with open(file_path, 'wb') as destination:
        #     for chunk in thumb_file.chunks():
        #         destination.write(chunk)
        
        self.thumbnail.save(thumb_path, thumb_file, save=False)


        super(Recipe, self).save(*args, **kwargs)

